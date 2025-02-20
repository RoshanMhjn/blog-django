from django.urls import path, include
from .views import PostListView, PostCreateView, CustomSignupView, PostDetailView,CommentUpdateView, CommentDeleteView, LikePostView, PostUpdateView, PostDeleteView, PostSearchView
from haystack.views import SearchView



app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('new/', PostCreateView.as_view(), name='post_create'),
    path("signup/", CustomSignupView.as_view(), name="account_signup"),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('post/<int:post_id>/like/', LikePostView.as_view(), name='like_post'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('tinymce/', include('tinymce.urls')),
]
