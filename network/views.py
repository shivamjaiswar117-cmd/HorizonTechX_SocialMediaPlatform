from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from .forms import PostForm, ProfileForm, RegisterForm
from .models import Comment, Follow, Post


def _back(request, fallback):
    nxt = request.POST.get("next", "")
    if nxt and url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}):
        return redirect(nxt)
    return redirect(fallback)


def _decorate(request, qs):
    posts = list(qs.select_related("author__profile").annotate(
        n_likes=Count("likes", distinct=True), n_comments=Count("comments", distinct=True)))
    liked = set(request.user.liked_posts.values_list("id", flat=True)) if request.user.is_authenticated else set()
    for p in posts:
        p.liked = p.id in liked
    return posts


def home(request):
    feed = request.GET.get("feed", "following")
    if request.user.is_authenticated and feed != "all":
        ids = list(request.user.following_rel.values_list("following_id", flat=True)) + [request.user.id]
        qs = Post.objects.filter(author_id__in=ids)
    else:
        feed, qs = "all", Post.objects.all()
    return render(request, "network/home.html", {"posts": _decorate(request, qs), "feed": feed})


@login_required
@require_POST
def post_create(request):
    form = PostForm(request.POST)
    if form.is_valid():
        Post.objects.create(author=request.user, content=form.cleaned_data["content"])
    else:
        messages.error(request, "Posts must be 1 to 280 characters.")
    return redirect("home")


def post_detail(request, pk):
    post = _decorate(request, Post.objects.filter(pk=pk))
    if not post:
        return redirect("home")
    comments = Comment.objects.filter(post_id=pk).select_related("author__profile")
    return render(request, "network/post_detail.html", {"p": post[0], "comments": comments})


@login_required
@require_POST
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    messages.success(request, "Post deleted.")
    return _back(request, "home")


@login_required
@require_POST
def comment_add(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST)
    if form.is_valid():
        Comment.objects.create(post=post, author=request.user, content=form.cleaned_data["content"])
    else:
        messages.error(request, "Comments must be 1 to 280 characters.")
    return redirect("post_detail", pk=pk)


@login_required
@require_POST
def like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"liked": liked, "count": post.likes.count()})
    return _back(request, "home")


def profile(request, username):
    u = get_object_or_404(User.objects.select_related("profile"), username=username)
    is_following = request.user.is_authenticated and Follow.objects.filter(
        follower=request.user, following=u).exists()
    return render(request, "network/profile.html", {
        "u": u, "posts": _decorate(request, u.posts.all()), "is_following": is_following,
        "followers": Follow.objects.filter(following=u).count(),
        "following": Follow.objects.filter(follower=u).count()})


@login_required
@require_POST
def follow_toggle(request, username):
    target = get_object_or_404(User, username=username)
    if target != request.user:
        obj, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if not created:
            obj.delete()
    return _back(request, reverse("profile", args=[username]))


def people(request):
    users = User.objects.select_related("profile").order_by("username")
    followed = set()
    if request.user.is_authenticated:
        users = users.exclude(pk=request.user.pk)
        followed = set(request.user.following_rel.values_list("following_id", flat=True))
    users = list(users)
    for x in users:
        x.is_followed = x.id in followed
    return render(request, "network/people.html", {"users": users})


@login_required
def edit_profile(request):
    form = ProfileForm(request.POST or None, instance=request.user.profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect("profile", username=request.user.username)
    return render(request, "network/edit_profile.html", {"form": form})


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save())
        messages.success(request, "Welcome! Follow some people to fill your feed.")
        return redirect("people")
    return render(request, "registration/register.html", {"form": form})
