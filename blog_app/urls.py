from django.urls import path

from blog_app.views import *


urlpatterns = [
    path('', index, name='index'),
    
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/detail/', post_detail, name='post-detail'),
    
    path('posts/create/', post_create, name='post-create'),
    path('posts/<int:pk>/delete/', post_delete, name='post-delete'),
    path('posts/<int:pk>/update/', post_update, name='post-update'),
    
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/create/', TagCreateView.as_view(), name='tag-create'),
    path('tags/<int:pk>/detail/', TagDetailView.as_view(), name='tag-detail'),
    
    # path('comments/<str:pk>/delete/', comment_delete, name='comment-delete'),
    
]