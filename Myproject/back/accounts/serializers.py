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
        fields = ['bankname', 'products', 'maxRate', 'maxRate2']

        
class UserPreferenceSerializer(serializers.ModelSerializer):
    preference = PreferenceSerializer(many=True)
    
    class Meta:
        model = User
        fields = ['username', 'preference']
        
    def update(self, instance, validated_data):
        preference_data = validated_data.pop('preference', [])
        instance = super().update(instance, validated_data)
        
        if preference_data:
            instance.preference.clear()
            for pref in preference_data:
                product = Product.objects.get_or_create(**pref)[0]
                instance.preference.add(product)
                
        return instance