from django.db import models
from django.contrib.auth.models import User, PermissionsMixin, AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from datetime import date
from .managers import UserProfileManager


# A class that represents a skill
class Skill(models.Model):
    title = models.CharField(max_length=200, default="Just another skill")
    description = models.CharField(max_length=200, default="Just another skill")
    
    def __str__(self):
        return self.title


# A class that represents an user profile
class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True, default='username')
    first_name = models.CharField(max_length=20, default='First')
    last_name = models.CharField(max_length=20, default='Last')
    email = models.EmailField(_('email address'), unique=True, default='email address')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    date_of_birth = models.DateField(default=date(1970, 1, 1))
    points = models.IntegerField(default=100)
    has_skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True)
    average_ratings = models.IntegerField(default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserProfileManager()

    def can_accept_application(self, post):
        print(self == post.seeker)
        return self == post.seeker and self.points >= post.points

    # Accepts an application for seeker
    def accept_application(self, post):
        self.points -= post.points
        post.status == 'ACCEPTED'

    # Accepts a post for giver
    def accept_job(self, post):
        self.points += post.points
        post.status == 'ACCEPTED'

    # Checks if seeker can create a post
    def can_create_post(self, post):
        return self == post.seeker and self.points >= post.points

    # Checks if giver can create a post
    def can_apply_post(self, post):
        return self != post.seeker and post.seeker.points >= post.points and self.has_skill == post.req_skill

    # Get the average rating of the user
    def get_average_ratings(self):
        review_list = Review.objects.filter(giver=self.pk)
        sum = 0
        for review in review_list:
            sum += review.ratings
        if review_list.count() > 0:
            return round(sum / review_list.count(), 1)
        else:
            return 0

    # Get the url of the user
    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])

    def __str__(self):
        return self.username


STATUS_CHOICES = [
    ("ACCEPTED", "ACCEPTED"),
    ("PENDING", "PENDING"),
    ("DECLINED", "DECLINED"),
]


# A class that represents a post
class Post(models.Model):
    title= models.CharField(max_length=40, default="Just another post")
    description = models.TextField(max_length=200, help_text="Describe your need.")
    status = models.CharField(
        max_length=8,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    points = models.IntegerField(default=0)
    seeker = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    req_skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# A class that represents an application
class Application(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    giver = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=8,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    def _str_(self):
        return self.post

# A class that represents a review
class Review(models.Model):
    seeker = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="seeker")
    giver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="giver")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ratings = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    comment = models.CharField(max_length=140, default="No comment")