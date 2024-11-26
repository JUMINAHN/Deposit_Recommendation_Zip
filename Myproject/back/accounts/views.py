from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User, Product, AdView, MLResult
from .serializers import ProfileSerializer
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .serializers import PreferenceSerializer  
from django.utils.http import unquote
import random
from django.utils import timezone


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

async def perform_ml_analysis(image):
    try:
        # 머신러닝 분석 결과를 반환하는 함수
        results = await model.predict(image)
        
        # 결과 포맷팅
        return {
            'class': results[0].className,  # 가장 높은 확률의 클래스
            'probability': float(results[0].probability)  # 확률
        }
    except Exception as e:
        print(f"ML 분석 오류: {str(e)}")
        raise Exception("이미지 분석 중 오류가 발생했습니다.")


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

@api_view(['DELETE'])
def delete_user(request):
    try:
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# views.py에서 사용할 때
async def analyze_image(request):  # async 추가
    try:
        image = request.FILES['image']
        user = request.user
        
        # 일일 시도 횟수 체크
        if user.daily_attempts >= 3:
            return Response({'message': '오늘의 시도 횟수를 모두 사용했습니다.'}, status=400)

        # 이미지 분석
        result = await perform_ml_analysis(image)  # await 사용 가능
        
        # 포인트 지급 로직 (0.1% 확률)
        points = 0
        if random.random() < 0.001:  # 0.1% 확률
            if result.get('class') == '오만원':
                points = 50000
                user.points += points
                user.save()

        # 결과 저장
        ml_result = MLResult.objects.create(
            user=user,
            image=image,
            result=result.get('class'),
            probability=result.get('probability'),
            points_awarded=points
        )

        user.daily_attempts += 1
        user.last_attempt = timezone.now()
        user.save()

        return Response({
            'result': result,
            'points_awarded': points,
            'attempts_left': 3 - user.daily_attempts
        })

    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_ad_view(request):
    user = request.user
    
    # 광고 시청 기록 저장
    AdView.objects.create(
        user=user,
        ad_type=request.data.get('ad_type', 'general')
    )
    
    # 시도 횟수 초기화
    user.daily_attempts = 0
    user.save()
    
    return Response({'message': '추가 시도가 활성화되었습니다.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_ad_view(request):
    user = request.user
    
    # 광고 시청 기록 저장
    AdView.objects.create(
        user=user,
        ad_type=request.data.get('ad_type', 'general')
    )
    
    # 시도 횟수 초기화
    user.daily_attempts = 0
    user.save()
    
    return Response({'message': '추가 시도가 활성화되었습니다.'})

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