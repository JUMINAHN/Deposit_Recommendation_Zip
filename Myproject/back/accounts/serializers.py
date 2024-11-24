from rest_framework import serializers
from .models import User, Product

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('username',)  # 수정할 수 없는 필드

class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['bankname', 'products', 'joinway', 'special', 'month', 'maxRate', 'maxRate2']

class UserPreferenceSerializer(serializers.ModelSerializer):
    preference = PreferenceSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'preference']