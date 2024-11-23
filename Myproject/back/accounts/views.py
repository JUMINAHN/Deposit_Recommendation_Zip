from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User, Product
from .serializers import ProfileSerializer
from django.http import JsonResponse
from django.contrib.auth import get_user_model

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    # 프로필 조회
    if request.method == 'GET':
        serializer = ProfileSerializer(user)
        return Response(serializer.data)
    # 프로필 수정
    elif request.method == 'PUT':
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 이건 메서드가 뭘로가야됨..? 일단 다 되게 해놨음
def follow(request, user_pk):
    User = get_user_model()
    you = User.objects.get(pk=user_pk)
    me = request.user

    if me != you:
        if me in you.followers.all():
            you.followers.remove(me)
            # me.followings.remove(you)
            is_followed = False
        else:
            you.followers.add(me)
            # me.followings.add(you)
            is_followed = True
        context = {
            'is_followed': is_followed,
            'followings_count': you.followings.count(),
            'followers_count': you.followers.count(),
        }
        return JsonResponse(context)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_preference(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    user.preference.add(product)
    return Response({'관심상품 추가!'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_preference(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    user.preference.remove(product)
    return Response({'관심상품 삭제!'})