from django.urls import path
from . import views

urlpatterns = [
    path('profile/current/', views.current_user_profile, name='current_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('accounts/<str:username>/follow/', views.follow, name='follow'),
    path('profile/<str:username>/preference/', views.preference_list, name='preference_list'),  # 특정 유저의 관심상품 목록
    path('profile/<str:username>/preference/save/<str:bankname>/<str:preference>/', 
        views.add_to_preference, 
        name='add_to_preference'),    
    path('profile/<str:username>/preference/delete/<str:bankname>/<str:preference>/', views.remove_from_preference, name='remove_from_preference'),
    path('analyze-image/', views.analyze_image, name='analyze_image'),
    path('verify-ad/', views.verify_ad_view, name='verify_ad'),
]
    