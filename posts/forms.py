from .models import UserProfile, Post
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import DateInput
from django.forms import ModelForm

# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name', 'password')

class UserProfileCreationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'has_skill')
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'})
        }

class PostCreationForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'points', 'req_skill')

