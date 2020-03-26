from django.contrib.auth.models import User
from .models import UserProfile, Post
from django import forms
from django.forms.widgets import DateInput

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('date_of_birth', 'has_skill')
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'})
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'points', 'req_skill')
