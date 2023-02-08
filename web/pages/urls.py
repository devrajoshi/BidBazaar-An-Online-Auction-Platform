from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('explore/', views.explore, name='explore'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('item/<int:item_id>/<slug:item_slug>/', views.item_page, name='item_page'),
    path('post/', views.Post, name='post'),
]
