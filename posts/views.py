from django.shortcuts import render, get_object_or_404
from .forms import UserProfileCreationForm, PostCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import Post, UserProfile, Application

# Create your views here.
def index(request):
    return render(request,
                'base.html',
                {'userprofile' : UserProfile.objects.all()})


class SignUpView(generic.CreateView):
    form_class = UserProfileCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


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


class CreatePostView(LoginRequiredMixin, generic.CreateView):
    form_class = PostCreationForm
    success_url = reverse_lazy('posts:post-list')
    template_name = 'posts/post_form.html'

    def form_valid(self, form):
        form.instance.seeker = self.request.user
        return super().form_valid(form)


def create_application(request, post_id):
    if request.user: 
        giver = request.user.userprofile
        current_post = Post.objects.get(pk=post_id)
        seeker = current_post.seeker
        if seeker.can_accept_application(post=current_post):
            application = Application.objects.create(post=current_post, giver=giver, status="PENDING")
            application.save()
            current_post.status="ACCEPTED"
        else:
            print("cant")
    return render(request, 'posts/apply.html')


class PostView(generic.DetailView):
    model = Post
    template_name = "posts/post.html"


class PostListView(generic.ListView):
    template_name = 'posts/post-list.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.all()


class ProfileView(generic.ListView):
    model = Post
    template_name = "posts/profile.html"
    context_object_name = 'post_list'

    def get_queryset(self):
        id = self.kwargs['pk']
        target_profile = get_object_or_404(UserProfile, pk = id)
        return Post.objects.filter(seeker=target_profile)


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

    
def choose_applications(request, post_id, application_id):
    accepted = Application.objects.get(id=application_id)
    if request.user:
        current_post = Post.objects.get(pk=post_id)
        application_list = Application.objects.filter(post=current_post)
        for application in application_list:
            if application == accepted:
                print(application)
                application.status = "ACCEPTED"
            else:
                application.status = "DECLINED"
            application.save()
        seeker = accepted.post.seeker
        seeker.accept_application(current_post)
        seeker.save()
    print(accepted)
    return render(
        request, 
        "posts/index.html", 
        {'giver' : accepted})

        




