from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.user_post, name='user_post'),
    path('profile/', views.profile_views, name='profile_views'),
    path('profile/<int:id>/', views.profile_data, name='profile_data'),
    path('profile/<int:id>/edit/', views.profile_edit, name='profile_edit'),
    
]