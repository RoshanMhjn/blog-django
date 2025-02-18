from django.contrib import admin
from .models import Post, Tag
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.urls import path


class CustomAdminSite(admin.AdminSite):
  site_header = "Blog Admin"
  
  def get_urls(self):
    urls = super().get_urls()
    custom_urls = [
      path('dashboard/', self.admin_view(self.dashboard_view), name="admin_dashboard"),
    ]
    return custom_urls + urls

  def dashboard_view(self, request):
    user_count = User.objects.count()
    blog_count = Post.objects.count

    context = {
      'user_count': user_count,
      'blog_count': blog_count
    }
    
    return TemplateResponse(request, "admin/dashboard.html")


# Register your models here.

admin.site.register(Post)
admin.site.register(Tag)

admin_site = CustomAdminSite(name='custom_admin')