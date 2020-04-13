from .models import UserProfile, Post
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import DateInput
from django.forms import ModelForm
from django import forms

# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name', 'password')

class UserProfileCreationForm(UserCreationForm):  
    email = forms.EmailField(required = False)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'has_skill')
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'})
        }

class PostCreationForm(ModelForm):
    description = forms.CharField(
                        required=False,
                        widget=forms.Textarea(
                                attrs={
                                    "placeholder": "Your description"
                                }
                            )
                        )
    
    # def __init__(self, *args, **kwargs):
    #     self.post = self.instance
    #     super(PostCreationForm, self).__init__(*args, **kwargs)

    # def clean_points(self, *args, **kwargs):
    #     points = self.cleaned_data.get("points")
    #     if points > self.post.seeker.points:
    #         raise forms.ValidationError("Not enough points to create post")
    #     return points

    class Meta:
        model = Post
        fields = ('title', 'description', 'points', 'req_skill')

