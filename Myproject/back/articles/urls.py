
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'articles' 
urlpatterns = [
    path('', views.article_list_create), #메인 화면 == article
    path('<int:pk>/', views.article_detail), #어떠한 몇 번째 article?
    path('<int:pk>/comments/', views.comment_create), #몇 번째 article에 대한 댓글                     
    path('comments/', views.article_comment), #댓글 생성 => 번호 부여
    path('comments/<int:comment_pk>/', views.article_comment_detail), #상세 댓글 조회
    ]
