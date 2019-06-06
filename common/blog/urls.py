from django.urls import path
from . import views

urlpatterns = [
    path('blogs/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('', views.wall, name='wall'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]