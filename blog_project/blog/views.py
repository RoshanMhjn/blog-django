from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import ListView, CreateView
from .models import Post
from django.urls import reverse_lazy
from allauth.account.views import SignupView
from .forms import CustomSignupForm, PostForm
from django.views.generic import DetailView

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