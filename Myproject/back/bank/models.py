from django.db import models
from django.conf import settings

#ERD 내용을 기반으로 모델 생성

class Articles(models.Model) :
    #유저 아이디 추후 추가할 예정 => user_id
    title = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)


class Comments(models.Model):
    #유저랑 아티클 생성 예정 => 아티클은 역참조로 진행해야 함
    article = models.ForeignKey(Articles, related_name='comments', on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)


# #좋아요 data? => 해당 페이지 필요여부 의구심 일단 킵 
# class Likes(models.Model):
#     #유저, 아티클
#     pass