from .models import UserProfile, Post, Review
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import DateInput
from django.forms import ModelForm
from django import forms


# A class that represents sign up form
class UserProfileCreationForm(UserCreationForm):  
    email = forms.EmailField(required = False)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'has_skill')
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'})
        }


# A class that represents post form
class PostCreationForm(ModelForm):
    description = forms.CharField(
                        required=False,
                        widget=forms.Textarea(
                                attrs={
                                    "placeholder": "Your description"
                                }
                            )
                        )

    def clean_points(self):
        points = self.cleaned_data["points"]
        return points

    class Meta:
        model = Post
        fields = ('title', 'description', 'points', 'req_skill')


<<<<<<< HEAD
=======
# A class that represents review form
>>>>>>> 87b8b450a7f8fb29e4c933f32dfd44d29feab157
class ReviewForm(ModelForm):
    def clean_post(self):
        post = self.cleaned_data["post"]
        return post


    class Meta:
        model = Review
        fields = ('giver', 'post', 'ratings', 'comment')