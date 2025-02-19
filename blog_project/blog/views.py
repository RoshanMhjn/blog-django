from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.views.generic import ListView, CreateView, TemplateView, View, DetailView
from .models import Post, Comment
from django.urls import reverse_lazy
from allauth.account.views import SignupView
from .forms import CustomSignupForm, PostForm, CommentForm
from django.views.generic import DetailView,UpdateView, DeleteView
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect


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
    
    def get(self, request, *args, **kwargs):
 
        self.object = self.get_object()
        self.object.views += 1
        self.object.save()  
        context = self.get_context_data(object=self.object)
        
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['has_liked'] = self.request.user in self.object.likes.all()
        
        if self.request.user.is_authenticated:
            context['form'] = CommentForm()
        else:
            context['form'] = None
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect('blog:post_detail', pk=self.object.pk)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', pk=self.object.pk)

        context = self.get_context_data(object=self.object)
        context['form'] = form
        return self.render_to_response(context)

class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def get_success_url(self):
         return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})
    
    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

class CommentDeleteView(DeleteView):
     def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, author=request.user)
        comment.delete()
        return redirect(request.META.get('HTTP_REFERER', 'blog:post_list'))
    
class LikePostView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        
        return redirect('blog:post_detail', pk=post.id)