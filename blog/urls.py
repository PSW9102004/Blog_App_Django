from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    add_comment,
    TagPostListView,
    BookmarkListView,
    toggle_like,
    toggle_bookmark
)
urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', add_comment, name='add-comment'),
    path('tag/<slug:slug>/', TagPostListView.as_view(), name='tag-posts'),
    path('bookmarks/', BookmarkListView.as_view(), name='bookmark-list'),
    path('post/<slug:slug>/like/', toggle_like, name='post-like'),
    path('post/<slug:slug>/bookmark/', toggle_bookmark, name='post-bookmark'),
]
