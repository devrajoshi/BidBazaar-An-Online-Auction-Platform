from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("item/<int:item_id>/<slug:item_slug>/", views.item_page, name="item_page"),
    path("bid/<int:item_id>/", views.bid, name='bid'),
    path("post/", views.post_item, name="post_item"),
    path("profile/<int:user_id>", views.user_profile, name="user_profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
