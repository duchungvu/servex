from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>', views.PostView.as_view(), name='post'),
    path('create/', views.CreatePostView.as_view(), name='post-create'),
    path('apply/post<int:post_id>/', views.create_application, name='apply'),
    path('applications/post<int:pk>', views.ApplicationView.as_view(), name='applications'),
    path('applications/application<int:application_id>/post<int:post_id>', views.choose_applications, name='chosen'),
    path('post/search_results/', views.PostSearchView.as_view(), name = "search-result"),
    path('application/review', views.ReviewView.as_view(), name='review')
]