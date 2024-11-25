from django.db import models
from django.contrib.auth.models import AbstractUser


class Product(models.Model):
    bankname = models.CharField(max_length=255)  # TextField 대신 CharField 사용
    products = models.CharField(max_length=255)
    joinway = models.TextField(blank=True)
    special = models.TextField(blank=True)
    month = models.IntegerField(default=0)
    maxRate = models.FloatField(default=0.0)
    maxRate2 = models.FloatField(default=0.0)
    
    class Meta:
        unique_together = ('bankname', 'products')  # 은행명과 상품명의 조합이 유일하도록
    


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


