from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>', views.PostView.as_view(), name='post')
]