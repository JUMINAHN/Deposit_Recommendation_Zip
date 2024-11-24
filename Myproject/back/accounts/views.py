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
def profile_view(request, username):
    #request user? 
    # User = get_user_model()
    user = request.user
    # profile_user = User.objects.get(username=username) #username
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


#전체 조회 관련 내용 추가
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def preference_list(request, username):
    try:
        User = get_user_model()
        user = User.objects.get(username=username) #유저의 정보를 기반으로 제품 찾기
        preferences = user.preference.all()
        data = [{
            'bankName': product.bankname,
            'productName': product.products
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
            
        # 상품이 없으면 생성
        product, created = Product.objects.get_or_create(
            bankname=bankname,
            products=preference,
            defaults={
                'joinway': '',  # 기본값 설정
                'special': '',
                'month': 0,
                'maxRate': 0.0,
                'maxRate2': 0.0
            }
        )
        
        request.user.preference.add(product)
        return Response({
            'bankName': bankname,
            'productName': preference,
            'message': '장바구니에 상품을 담았습니다!'
        })
    except Exception as e:
        return Response({'message': f'상품 저장 중 오류가 발생했습니다: {str(e)}'}, status=400)
    
    
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