from django.db import models

# Create your models here.

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