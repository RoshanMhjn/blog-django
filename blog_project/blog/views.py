from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import ListView, CreateView, TemplateView
from .models import Post
from django.urls import reverse_lazy
from allauth.account.views import SignupView
from .forms import CustomSignupForm, PostForm
from django.views.generic import DetailView
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Count

# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'tags']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CustomSignupView(SignupView):
    form_class = CustomSignupForm

    def form_valid(self, form):
        user = form.save(self.request)
        login(self.request, user)
        return redirect("blog:post_list") 

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
class CustomDashboardView(TemplateView):
    template_view = 'admin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(self, **kwargs)
        total_users = User.objects.count()
        total_blogs = Post.objects.count()
        
        last_six_months = timezone.now() - timezone.timedelta(days=180)
        user_counts = User.objects.filter(date_joined__gte=last_six_months).values('date_joined__month').annotate(count=Count('id'))
        blog_counts = Post.objects.filter(created_at__gte=last_six_months).values('created_at__month').annotate(count=Count('id'))

        context.update({
            'total_users': total_users,
            'total_blogs': total_blogs,
            'user_counts': user_counts,
            'blog_counts': blog_counts,
        })
        
        print("Context data:", context)
        return context
        