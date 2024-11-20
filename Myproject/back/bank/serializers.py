from rest_framework import serializers
from .models import DepositOptions, DepositProducts

class DepositProductsSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    class Meta:
        model = DepositProducts
        fields = ('kor_co_nm', 'fin_prdt_nm', 'options')
    def get_options(self, obj):
        options = DepositOptions.objects.filter(product=obj)
        return DepositOptionsSerializer(options, many=True).data
    
# class DepositOptionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DepositOptions
#         fields = '__all__'
#         read_only_fields = ('product',)

class DepositOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DepositOptions
        fields = ('intr_rate', 'intr_rate_type_nm', 'save_trm')

