from rest_framework import serializers
from .models import DepositOptions, DepositProducts

# ===================== 예적금, 이름만 예금으로 ===============================
class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = ('intr_rate', 'intr_rate2', 'intr_rate_type_nm', 'save_trm')

class DepositProductsSerializer(serializers.ModelSerializer):
    options = DepositOptionsSerializer(many=True, read_only=True)
    class Meta:
        model = DepositProducts
        fields = ('dcls_month', 'kor_co_nm', 'fin_prdt_nm', 'join_way', 'spcl_cnd', 'join_deny', 'options')
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['options'] = DepositOptionsSerializer(instance.depositoptions_set.all(), many=True).data
        return representation

class DepositProductsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'

class DepositOptionsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'

