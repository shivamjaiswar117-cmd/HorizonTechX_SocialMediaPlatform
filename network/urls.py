from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("post/new/", views.post_create, name="post_create"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/<int:pk>/like/", views.like_toggle, name="like_toggle"),
    path("post/<int:pk>/comment/", views.comment_add, name="comment_add"),
    path("post/<int:pk>/delete/", views.post_delete, name="post_delete"),
    path("people/", views.people, name="people"),
    path("u/<str:username>/", views.profile, name="profile"),
    path("u/<str:username>/follow/", views.follow_toggle, name="follow_toggle"),
    path("settings/profile/", views.edit_profile, name="edit_profile"),
    path("register/", views.register, name="register"),
]
