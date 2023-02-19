from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.index, name="index"),
    path("explore/", views.explore, name="explore"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("item/<int:item_id>/<slug:item_slug>/", views.item_page, name="item_page"),
    path("post/", views.post_item, name="post_item"),
    path("profile/<int:user_id>", views.user_profile, name="user_profile"),
    # path("me/", views.user_profile, name="profile_page"),
]
