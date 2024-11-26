from django.db import models
from accounts.models import User, Product

class UserPreferencePattern(models.Model):
    age_group = models.IntegerField()  # 연령대 (20대, 30대 등)
    asset_range = models.CharField(max_length=50)  # 자산 범위
    income_range = models.CharField(max_length=50)  # 연봉 범위
    preferred_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)  # 해당 패턴의 선호도 카운트

class ProductRecommendation(models.Model):
    age_group = models.CharField(max_length=20)  # '20대', '30대' 등
    income_level = models.CharField(max_length=20)  # '저소득', '중소득', '고소득'
    asset_level = models.CharField(max_length=20)  # '소액', '중액', '고액'
    recommended_interest_rate = models.FloatField()  # 추천 금리 범위
    priority = models.IntegerField()  # 추천 우선순위
    
    class Meta:
        ordering = ['priority']


class Product(models.Model):
    bankname = models.CharField(max_length=100)
    products = models.CharField(max_length=100)
    join_way = models.TextField(null=True, blank=True)
    special = models.TextField(null=True, blank=True)
    maxRate = models.DecimalField(max_digits=5, decimal_places=2)
    maxRate2 = models.DecimalField(max_digits=5, decimal_places=2)

class UserStatistics(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    age_group = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    user_count = models.IntegerField()
    avg_satisfaction = models.FloatField()