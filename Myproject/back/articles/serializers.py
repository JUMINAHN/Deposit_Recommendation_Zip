#게시글과 댓글 생성 필요함
from .models import Articles, Comments
from rest_framework import serializers


class ArticleSerializer(serializers.ModelSerializer): #article serializer
    user = serializers.StringRelatedField()
    class Meta:
        model = Articles
        fields = '__all__'
        # 정우수정부분
        read_only_fields = ('user',)

class CommentSerializer(serializers.ModelSerializer): #comment serializer
    user = serializers.StringRelatedField(read_only=True)
    #대댓글 보류
    class Meta:
        model = Comments
        fields = ('content', 'created_at', 'updated_at', 'user', 'id')
        read_only_fields= ('article', ) #article이 몇번째인지 사용자가 기록하지 않기 떄문 => read_only 사용
        # read_only_fields = ['user']