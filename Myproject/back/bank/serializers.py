from rest_framework import serializers
from .models import DepositOptions, DepositProducts

class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'


# class DepositOptionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DepositOptions
#         fields = '__all__'
#         read_only_fields = ('product',)

class DepositOptionsSerializer(serializers.ModelSerializer):
    fin_prdt_cd = serializers.IntegerField(source='product.id', read_only=True)

    class Meta:
        model = DepositOptions
        fields = ('id', 'intr_rate_type_nm', 'intr_rate', 'intr_rate2', 'save_trm', 'fin_prdt_cd')

