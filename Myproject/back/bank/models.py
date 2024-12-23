from django.db import models

# Create your models here.
# 이름은 예금이지만 적금이랑 뽑아오는 필드 다 똑같아서 그냥 진행할게용~
class DepositProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True)
    dcls_month = models.IntegerField()
    kor_co_nm = models.TextField()
    fin_prdt_nm = models.TextField()
    etc_note = models.TextField()
    join_deny = models.IntegerField(null=True, blank=True)
    join_member = models.TextField()
    join_way = models.TextField()
    spcl_cnd = models.TextField()

class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts, related_name='options', on_delete=models.CASCADE)
    fin_prdt_cd = models.TextField()
    intr_rate_type_nm = models.CharField(max_length=100)
    intr_rate = models.FloatField(null=True, blank=True)
    intr_rate2 = models.FloatField(null=True, blank=True)
    save_trm = models.IntegerField(null=True, blank=True)

class Product(models.Model):
    bankname = models.CharField(max_length=100)
    products = models.CharField(max_length=100)
    join_way = models.TextField(null=True, blank=True)
    special = models.TextField(null=True, blank=True)
    maxRate = models.DecimalField(max_digits=5, decimal_places=2)
    maxRate2 = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'products'

class UserStatistics(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    age_group = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    user_count = models.IntegerField()
    avg_satisfaction = models.FloatField()

    class Meta:
        db_table = 'user_statistics'