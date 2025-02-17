from allauth.account.forms import SignupForm
from django import forms
from .models import Post, Tag

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
      queryset=Tag.objects.all(),
      widget = forms.CheckboxSelectMultiple,
      required = False
    )
    
    class Meta:
      model = Post
      fields = ['title', 'content', 'image', 'tags']