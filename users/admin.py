# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserProfileCreationForm, UserProfileChangeForm
from .models import UserProfile

class UserProfileAdmin(UserAdmin):
    model = UserProfile
    add_form = UserProfileCreationForm
    form = UserProfileChangeForm

admin.site.register(UserProfile, UserProfileAdmin)