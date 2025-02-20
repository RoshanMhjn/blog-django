import re
from haystack import indexes
from .models import Post
from django.utils.html import strip_tags

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')

    def prepare_content(self, obj):
        return strip_tags(obj.content)  

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
