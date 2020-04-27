from django.shortcuts import render, get_object_or_404
from .forms import UserProfileCreationForm, PostCreationForm, ReviewForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import Post, UserProfile, Application, Review
from django.contrib.auth.decorators import login_required
from django import forms

# Index page view
def index(request):
    return render(request,
                'posts/index.html',
                {'userprofile' : UserProfile.objects.all()})


# Sign up page view
class SignUpView(generic.CreateView):
    form_class = UserProfileCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


# Sign in page view
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account is disabled")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'users/login.html')


# Log out page view
def user_logout(request):
    if request.user:
        logout(request)
    return render(request, 'users/login.html')


# Create application view
def create_application(request, post_id):
    if request.user: 
        current_giver = request.user
        current_post = Post.objects.get(pk=post_id)
        seeker = current_post.seeker
        if seeker.can_accept_application(post=current_post) and current_giver.can_apply_post(post=current_post):
            if Application.objects.filter(giver=current_giver).count() < 1:
                application = Application.objects.create(post=current_post, giver=current_giver, status="PENDING")
                application.save()
            else:
                return HttpResponse("You have already applied for a post")
        else:
            print("Seeker points: {0}, Post points: {1}, Giver points: {2}".format(seeker.points, current_post.points, current_giver.points))
            return HttpResponse("Not enough points or required skill")
    return render(request, 'posts/apply.html')

# Specific post view
class PostView(generic.DetailView):
    model = Post
    template_name = "posts/post.html"

# List of posts view
class PostListView(generic.ListView):
    template_name = 'posts/post-list.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.all()

# User profile view
class ProfileView(generic.DetailView):
    model = UserProfile
    template_name = "posts/profile.html"


# Application view
class ApplicationView(generic.ListView):
    model = Application
    template_name = "posts/applications.html"
    context_object_name = 'application_list'

    def get_queryset(self):
        id = self.kwargs['pk']
        target_post = get_object_or_404(Post, pk = id)
        return Application.objects.filter(post=target_post)
    
    def get_context_data(self, **kwargs):
        context = super(ApplicationView, self).get_context_data(**kwargs)
        id = self.kwargs['pk']
        target_post = get_object_or_404(Post, pk = id)
        context['post'] = target_post
        accepted = Application.objects.filter(post=target_post, status='ACCEPTED')
        if accepted:
            context['giver'] = accepted[0].giver
        return context

    
# Specific pplication view
def choose_applications(request, post_id, application_id):
    # the chosen application
    accepted = Application.objects.get(id=application_id)
    if request.user:
        current_post = Post.objects.get(pk=post_id)
        # Change status of all application for this post
        application_list = Application.objects.filter(post=current_post)
        for application in application_list:
            if application == accepted:
                print(application)
                application.status = "ACCEPTED"
            else:
                application.status = "DECLINED"
            application.save()
        # change points for seeker
        seeker = accepted.post.seeker
        seeker.accept_application(current_post)
        seeker.save()
        # change point for giver
        giver = accepted.giver
        giver.accept_job(current_post)
        giver.save()
        # change post status
        accepted.post.status = "ACCEPTED"
        accepted.post.save()
    return render(
        request, 
        "posts/applications.html",
        {'giver' : accepted.giver})


# Search view
class PostSearchView(generic.ListView):
    model = Post
    template_name = "posts/search-results.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        post_list = Post.objects.filter(req_skill__title__icontains=query)
        return post_list

def job_done(request, application_id):
    if request.user:
        current_appl = Application.objects.get(id=application_id)
        current_post = current_appl.post
        current_post.status ="ACCEPTED"

    return render(
        request,
        "posts/done.html"
    )


# Create a post view
class CreatePostView(LoginRequiredMixin, generic.CreateView):
    form_class = PostCreationForm
    success_url = reverse_lazy('posts:post-list')
    template_name = 'posts/post-form.html'

    def form_valid(self, form):
        form.instance.seeker = self.request.user
        if not form.instance.seeker.can_create_post(form.instance):
            return HttpResponse("You don't have enough point to create this post")
        return super().form_valid(form)


# Review view
class ReviewView(generic.CreateView):
    form_class = ReviewForm
    success_url = reverse_lazy('posts:post-list')
    template_name = "posts/review.html"

    def form_valid(self, form):
        form.instance.seeker = self.request.user
        return super().form_valid(form)


# View the list of review for user
class UserReviewView(generic.ListView):
    model = Review
    context_object_name = 'review_list'
    template_name = 'posts/review-list.html'

    def get_queryset(self):
        id = self.kwargs['pk']
        self.giver = UserProfile.objects.filter(pk=id)[0]
        return Review.objects.filter(giver=self.giver)