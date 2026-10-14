from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from network.models import Comment, Follow, Post


class Command(BaseCommand):
    help = "Create demo users (password: demo12345), posts, comments, follows and likes"

    def handle(self, *args, **opts):
        names = {"alice": "Coffee, code and long walks.", "bob": "Building things in Django.",
                 "carol": "Photographer. Mumbai."}
        users = {}
        for n, bio in names.items():
            u, made = User.objects.get_or_create(username=n)
            if made:
                u.set_password("demo12345")
                u.save()
            u.profile.bio = bio
            u.profile.save()
            users[n] = u
        if not Post.objects.exists():
            p1 = Post.objects.create(author=users["alice"], content="Hello world! This is my first post.")
            p2 = Post.objects.create(author=users["bob"], content="Just shipped my first Django project.")
            p3 = Post.objects.create(author=users["carol"], content="Golden hour in Thane never disappoints.")
            p1.likes.add(users["bob"], users["carol"])
            p2.likes.add(users["alice"])
            Comment.objects.create(post=p2, author=users["alice"], content="Congrats! Looks great.")
            Comment.objects.create(post=p3, author=users["bob"], content="Beautiful shot.")
        Follow.objects.get_or_create(follower=users["alice"], following=users["bob"])
        Follow.objects.get_or_create(follower=users["bob"], following=users["alice"])
        self.stdout.write(self.style.SUCCESS("Demo data loaded. Log in as alice / bob / carol, password demo12345"))
