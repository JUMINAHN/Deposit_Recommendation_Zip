from django.db import models
from django.contrib.auth.models import AbstractUser
import tensorflow as tf
from django.utils import timezone
import random


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
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    points = models.IntegerField(default=0)  # 포인트 필드 추가
    last_attempt = models.DateTimeField(null=True, blank=True)  # 마지막 시도 시간
    daily_attempts = models.IntegerField(default=0)  # 일일 시도 횟수

class MLResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ml_images/')
    result = models.CharField(max_length=100)  # 분석 결과
    probability = models.FloatField()  # 확률
    created_at = models.DateTimeField(auto_now_add=True)
    points_awarded = models.IntegerField(default=0)  # 지급된 포인트

class AdView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    ad_type = models.CharField(max_length=50)

async def perform_ml_analysis(image):
    try:
        # 모델 경로 설정
        model_path = 'media/models/my_model'  # Django 프로젝트의 media 폴더 내 경로
        
        # 모델 로드
        model = tf.keras.models.load_model(model_path)
        
        # 이미지 전처리
        img = tf.keras.preprocessing.image.load_img(
            image, target_size=(224, 224)  # 모델 입력 크기에 맞게 조정
        )
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
        
        # 예측
        predictions = model.predict(img_array)
        
        return {
            'class': '오만원' if predictions[0][0] > 0.5 else '다른 지폐',
            'probability': float(predictions[0][0])
        }
    except Exception as e:
        print(f"ML 분석 오류: {str(e)}")
        raise Exception("이미지 분석 중 오류가 발생했습니다.")