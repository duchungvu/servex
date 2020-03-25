from django.contrib import admin
from .models import Skill, UserProfile, Post, Application, Review

# Register your models here.
admin.site.register(Skill)
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Application)
admin.site.register(Review)