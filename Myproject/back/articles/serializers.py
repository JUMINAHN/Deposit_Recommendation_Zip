#게시글과 댓글 생성 필요함
from .models import Articles, Comments
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Articles
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at', 'likes_count', 'is_liked']
        read_only_fields = ('user', 'likes')

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

class CommentSerializer(serializers.ModelSerializer): #comment serializer
    user = serializers.StringRelatedField(read_only=True)
    #대댓글 보류
    class Meta:
        model = Comments
        fields = ('content', 'created_at', 'updated_at', 'user', 'id')
        read_only_fields= ('article', ) #article이 몇번째인지 사용자가 기록하지 않기 떄문 => read_only 사용
        # read_only_fields = ['user']