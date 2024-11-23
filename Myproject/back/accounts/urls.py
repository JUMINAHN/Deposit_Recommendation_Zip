from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
]
