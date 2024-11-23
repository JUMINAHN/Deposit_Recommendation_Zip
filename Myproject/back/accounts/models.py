from django.db import models
from django.contrib.auth.models import AbstractUser


class Product(models.Model):
    bankname = models.TextField() # 은행명
    products = models.TextField() # 상품명
    joinway = models.TextField() # 가입방법
    special = models.TextField() # 이거모얌
    month = models.IntegerField() # 가입기간
    maxRate = models.FloatField()
    maxRate2 = models.FloatField()
    


# Create your models here.
class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    website = models.URLField(blank=True, null=True)  # 깃허브주소?
    nickname = models.TextField(blank=True, null=True) # 닉네임
    age = models.IntegerField(blank=True, null=True) # 나이
    asset = models.FloatField(blank=True, null=True) # 자산
    income = models.FloatField(blank=True, null=True) # 연봉
    bankname = models.TextField(blank=True, null=True) # 은행명
    preference = models.ManyToManyField(Product, blank=True) # 관심상품명


