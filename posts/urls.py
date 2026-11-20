from django.urls import path
from posts.views import post_detail_view, post_list_view,post_create_view

urlpatterns = [
    path('', view=post_list_view, name='post-list'),
    path('post/<int:pk>/', view=post_detail_view, name='post-detail'),
    path('create_post/', view=post_create_view, name='post_create'),

]
