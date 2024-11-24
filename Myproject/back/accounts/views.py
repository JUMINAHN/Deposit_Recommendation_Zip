from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User, Product
from .serializers import ProfileSerializer
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .serializers import PreferenceSerializer  



@api_view(['GET', 'PUT']) #기존에는 request.user 정보만 반환해서 다른 유저의 정보를 받아올 수 없었음
@permission_classes([IsAuthenticated])
def profile_view(request, username):
    try:
        User = get_user_model()
        profile_user = User.objects.get(username=username)
        
        if request.method == 'GET':
            serializer = ProfileSerializer(profile_user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            # 자신의 프로필만 수정 가능
            if request.user != profile_user:
                return Response({'message': '권한이 없습니다.'}, status=403)
            serializer = ProfileSerializer(profile_user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
    except User.DoesNotExist:
        return Response({'message': '사용자를 찾을 수 없습니다.'}, status=404)


# 이건 메서드가 뭘로가야됨..? 일단 다 되게 해놨음
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, user_pk):
    try:
        User = get_user_model()
        you = User.objects.get(pk=user_pk)
        me = request.user

        # 자기 자신을 팔로우할 수 없음
        if me == you:
            return Response({'message': '자기 자신을 팔로우할 수 없습니다.'}, status=400)

        if me in you.followers.all():
            you.followers.remove(me)
            is_followed = False
        else:
            you.followers.add(me)
            is_followed = True

        context = {
            'is_followed': is_followed,
            'followers': [user.username for user in you.followers.all()],
            'followings': [user.username for user in you.followings.all()],
        }
        return Response(context)
    except User.DoesNotExist:
        return Response({'message': '사용자를 찾을 수 없습니다.'}, status=404)


#전체 조회 관련 내용 추가
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def preference_list(request, username):
    try:
        User = get_user_model()
        user = User.objects.get(username=username)
        preferences = user.preference.all()
        data = [{
            'bankname': product.bankname,
            'products': product.products,
            'maxRate': product.maxRate,
            'maxRate2': product.maxRate2
        } for product in preferences]
        return Response(data)
    except User.DoesNotExist:
        return Response({'message': '사용자를 찾을 수 없습니다.'}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_preference(request, username, bankname, preference):
    try:
        if request.user.username != username:
            return Response({'message': '권한이 없습니다.'}, status=403)
            
        # 상품 조회 또는 생성
        product = Product.objects.filter(
            bankname=bankname,
            products=preference
        ).first()
        
        if not product:
            return Response({'message': '존재하지 않는 상품입니다.'}, status=404)
        
        request.user.preference.add(product)
        serializer = PreferenceSerializer(product)
        return Response(serializer.data)
    except Exception as e:
        return Response({'message': str(e)}, status=400)
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_preference(request, username, bankname, preference):
    try:
        # 요청한 사용자와 대상 사용자가 같은지 확인
        if request.user.username != username:
            return Response({'message': '권한이 없습니다.'}, status=403)
            
        product = Product.objects.get(bankname=bankname, products=preference)
        request.user.preference.remove(product)
        return Response({'message': '관심 상품에서 제거되었습니다.'})
    except Product.DoesNotExist:
        return Response({'message': '삭제할 수 없는 상품입니다.'}, status=404)
    

@api_view(['GET']) #사용자 정보 반환
@permission_classes([IsAuthenticated])
def current_user_profile(request):
    serializer = ProfileSerializer(request.user)
    return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def add_to_preference(request, product_id):
#     user = request.user
#     product = Product.objects.get(id=product_id)
#     user.preference.add(product)
#     return Response({'관심상품 추가!'})

# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def remove_from_preference(request, product_id):
#     user = request.user
#     product = Product.objects.get(id=product_id)
#     user.preference.remove(product)
#     return Response({'관심상품 삭제!'})