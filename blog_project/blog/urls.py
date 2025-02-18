from django.urls import path
from .views import PostListView, PostCreateView, CustomSignupView, PostDetailView, CustomDashboardView



app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('new/', PostCreateView.as_view(), name='post_create'),
    path("signup/", CustomSignupView.as_view(), name="account_signup"),
    path('post/<int:id>/', PostDetailView.as_view(), name='post_detail'),
    path('admin/dashboard/', CustomDashboardView.as_view(), name='custom_dashboard'),
]
