from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Skill(models.Model):
    title = models.CharField(max_length=200,default="Just another skill")
    description = models.CharField(max_length=200, default="Just another skill")

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    date_of_birth = models.DateField(default=0)
    points = models.IntegerField(default=0)
    has_skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


STATUS_CHOICES = [
    ("AC", "ACCEPTED"),
    ("PE", "PENDING"),
    ("DE", "DECLINED"),
]


class Post(models.Model):
    title= models.CharField(max_length=200, default="Just another post")
    description = models.TextField(max_length=200, help_text="Describe your need.")
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='PE'
    )
    point = models.IntegerField(default=0)
    seeker = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    req_skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.description


class Application(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    giver = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='PE'
    )





class Review(models.Model):
    seeker = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="seeker")
    giver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="giver")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ratings = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    comment = models.CharField(max_length=140, default="No comment")







