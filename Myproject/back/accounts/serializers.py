from rest_framework import serializers
from .models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('username',)  # 수정할 수 없는 필드
