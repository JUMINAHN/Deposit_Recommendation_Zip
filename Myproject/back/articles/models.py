from django.db import models
from django.conf import settings

#ERD 내용을 기반으로 모델 생성

class Articles(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_articles', blank=True)
    
    def number_of_likes(self):
        return self.likes.count()


class Comments(models.Model):
    #유저랑 아티클 생성 예정 => 아티클은 역참조로 진행해야 함
    article = models.ForeignKey(Articles, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)


# #좋아요 data? => 해당 페이지 필요여부 의구심 일단 킵 
# class Likes(models.Model):
#     #유저, 아티클
#     pass