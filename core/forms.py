# core/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import Post, Comment

# Login form
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

# Registration form
class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content','image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title of your post'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your content here...'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write something...'}),
        }

from django import forms
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(label="Your Email")
    message = forms.CharField(widget=forms.Textarea, label="Your Message")


    