from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
    #관심 상품 모두 조회할 수 있어야 함 => 이거 만드는게 맞을 것 같음
    path('profile/current/', views.current_user_profile, name='current_profile'),
    path('profile/<str:username>/preference/', views.preference_list, name='preference_list'),  # 특정 유저의 관심상품 목록
    path('profile/<str:username>/preference/save/<str:bankname>/<str:preference>/', views.add_to_preference, name='add_to_preference'),
    path('profile/<str:username>/preference/delete/<str:bankname>/<str:preference>/', views.remove_from_preference, name='remove_from_preference'),
]
    