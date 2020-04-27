from django.contrib import admin
from .models import Skill, UserProfile, Post, Application, Review
from .forms import UserProfileCreationForm

admin.site.register(Skill)
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Application)
admin.site.register(Review)