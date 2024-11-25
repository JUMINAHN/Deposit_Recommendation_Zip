from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User, Product
from .serializers import ProfileSerializer
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .serializers import PreferenceSerializer  
from django.utils.http import unquote



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
def follow(request, username):
    try:
        User = get_user_model()
        to_follow = User.objects.get(username=username)
        user = request.user

        if user == to_follow:
            return Response({'message': '자기 자신을 팔로우할 수 없습니다.'}, status=400)

        if user in to_follow.followers.all():
            to_follow.followers.remove(user)
            is_followed = False
        else:
            to_follow.followers.add(user)
            is_followed = True

        return Response({
            'is_followed': is_followed,
            'followers': [user.username for user in to_follow.followers.all()],
            'followings': [user.username for user in to_follow.followings.all()]
        })
    except User.DoesNotExist:
        return Response({'message': '사용자를 찾을 수 없습니다.'}, status=404)


#전체 조회 관련 내용 추가
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_preference(request, username, bankname, preference):
    try:
        if request.user.username != username:
            return Response({'message': '권한이 없습니다.'}, status=403)

        # URL 디코딩 처리
        decoded_bankname = unquote(bankname).strip()
        decoded_preference = unquote(preference).strip()

        product = Product.objects.filter(
            bankname=decoded_bankname,
            products=decoded_preference
        ).first()

        if not product:
            return Response({'message': '존재하지 않는 상품입니다.'}, status=404)

        request.user.preference.add(product)
        serializer = PreferenceSerializer(product)
        return Response(serializer.data)
    except Exception as e:
        return Response({'message': str(e)}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_preference(request, username, bankname, preference):
    try:
        if request.user.username != username:
            return Response({'message': '권한이 없습니다.'}, status=403)
            
        decoded_bankname = unquote(bankname)
        decoded_preference = unquote(preference)
        
        # 상품이 없으면 생성
        product, created = Product.objects.get_or_create(
            bankname=decoded_bankname,
            products=decoded_preference,
            defaults={
                'joinway': '',  # getOptionDeposit에서 가져온 데이터
                'special': '',  # getOptionDeposit에서 가져온 데이터
                'month': 0,    # getOptionDeposit에서 가져온 데이터
                'maxRate': 0,  # getOptionDeposit에서 가져온 데이터
                'maxRate2': 0  # getOptionDeposit에서 가져온 데이터
            }
        )
        
        request.user.preference.add(product)
        serializer = PreferenceSerializer(product)
        return Response(serializer.data)
    except Exception as e:
        return Response({'message': str(e)}, status=400)
    
@api_view(['POST'])
def sync_products(request):
    try:
        data = request.data  # getOptionDeposit의 데이터
        for item in data:
            Product.objects.update_or_create(
                bankname=item['bankname'],
                products=item['products'],
                defaults={
                    'joinway': item['joinWay'],
                    'special': item['special'],
                    'month': item['month'],
                    'maxRate': item['maxRate'],
                    'maxRate2': item['maxRate2']
                }
            )
        return Response({'message': '상품 동기화 완료'})
    except Exception as e:
        return Response({'message': str(e)}, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_preference(request, username, bankname, preference):
    try:
        if request.user.username != username:
            return Response({'message': '권한이 없습니다.'}, status=403)

        bankname = unquote(bankname)
        preference = unquote(preference)
            
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