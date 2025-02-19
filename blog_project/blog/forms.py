from allauth.account.forms import SignupForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Post, Tag, Comment

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

class CommentForm(forms.ModelForm):
    class Meta:
      model = Comment
      fields = ['content']
      labels = {'content': ''}
    
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Comment', css_class='btn btn-primary mt-3'))
        self.fields['content'].widget = forms.Textarea(attrs={
            'rows': 2,
            'class': 'form-control'})