from django.urls import path
from posts.views import post_detail_view, post_list_view, post_create_view

app_name = 'posts'

urlpatterns = [
    path('', post_list_view, name='post_list'),
    path('post/<int:pk>/', post_detail_view, name='post_detail'),
    path('create_post/', post_create_view, name='post_create'),
]
