from django.contrib import admin
from .models import Post, Tag, Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content', 'created_at')
    search_fields = ('content', 'author__username')

# Register your models here.

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)