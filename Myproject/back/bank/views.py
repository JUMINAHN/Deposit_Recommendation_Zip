from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response

import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings
from .models import DepositOptions, DepositProducts
from .serializers import DepositOptionsSerializer, DepositProductsSerializer, DepositOptionsCreateSerializer, DepositProductsCreateSerializer
from django.core.serializers.json import DjangoJSONEncoder
import openai 
import logging
logger = logging.getLogger(__name__)


# Create your views here.
BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'
# ===================================== 예금 =================================
@api_view(['GET'])
@permission_classes([AllowAny]) #모두 권한 설정
def save_deposit_products(request, topFinGrpNo, pageNo):
    url = BASE_URL + 'depositProductsSearch.json'
    params = {
        'auth': settings.API_KEY,
        'topFinGrpNo': topFinGrpNo, 
        'pageNo': pageNo
    }
    response = requests.get(url, params=params).json()
    for base in response.get('result').get('baseList'):
        fin_prdt_cd = base.get('fin_prdt_cd')
        save_data = {
            'fin_prdt_cd': fin_prdt_cd,
            'dcls_month': base.get('dcls_month'),
            'kor_co_nm': base.get('kor_co_nm'),
            'fin_prdt_nm': base.get('fin_prdt_nm'),
            'etc_note': base.get('etc_note', ''),
            'join_deny': base.get('join_deny', 0),
            'join_member': base.get('join_member', ''),
            'join_way': base.get('join_way', ''),
            'spcl_cnd': base.get('spcl_cnd', '')
        }
        serializer = DepositProductsCreateSerializer(data=save_data)
        if serializer.is_valid():
            serializer.save()

    for option in response.get('result').get('optionList'):
        fin_prdt_cd = option.get('fin_prdt_cd')
        try:
            product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
            save_data = {
                'product': product,
                'fin_prdt_cd': fin_prdt_cd,
                'intr_rate_type_nm': option.get('intr_rate_type_nm'),
                'intr_rate': option.get('intr_rate', -1),
                'intr_rate2': option.get('intr_rate2', -1),
                'save_trm': option.get('save_trm', 0)
            }
            DepositOptions.objects.update_or_create(
                product=product,
                fin_prdt_cd=fin_prdt_cd,
                save_trm=save_data['save_trm'],
                defaults=save_data
            )
        except DepositProducts.DoesNotExist:
            print(f"Product with fin_prdt_cd {fin_prdt_cd} does not exist")
    return JsonResponse({'message': '저장 성공'})

# ===================================== 적금 =================================
@api_view(['GET'])
@permission_classes([AllowAny]) 
def save_deposit_products2(request, topFinGrpNo, pageNo):
    url = BASE_URL + 'savingProductsSearch.json'
    params = {
        'auth': settings.API_KEY,
        'topFinGrpNo':  topFinGrpNo, # 은행
        'pageNo': pageNo # 1페이지 끝
    }
    response = requests.get(url, params=params).json()
    for base in response.get('result').get('baseList'):
        fin_prdt_cd = base.get('fin_prdt_cd')
        save_data = {
            'fin_prdt_cd': fin_prdt_cd,
            'dcls_month': base.get('dcls_month'),
            'kor_co_nm': base.get('kor_co_nm'),
            'fin_prdt_nm': base.get('fin_prdt_nm'),
            'etc_note': base.get('etc_note', ''),
            'join_deny': base.get('join_deny', 0),
            'join_member': base.get('join_member', ''),
            'join_way': base.get('join_way', ''),
            'spcl_cnd': base.get('spcl_cnd', '')
        }
        serializer = DepositProductsCreateSerializer(data=save_data)
        if serializer.is_valid():
            serializer.save()

    for option in response.get('result').get('optionList'):
        fin_prdt_cd = option.get('fin_prdt_cd')
        try:
            product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
            save_data = {
                'product': product,
                'fin_prdt_cd': fin_prdt_cd,
                'intr_rate_type_nm': option.get('intr_rate_type_nm'),
                'intr_rate': option.get('intr_rate', -1),
                'intr_rate2': option.get('intr_rate2', -1),
                'save_trm': option.get('save_trm', 0)
            }
            DepositOptions.objects.update_or_create(
                product=product,
                fin_prdt_cd=fin_prdt_cd,
                save_trm=save_data['save_trm'],
                defaults=save_data
            )
        except DepositProducts.DoesNotExist:
            print(f"Product with fin_prdt_cd {fin_prdt_cd} does not exist")
    return JsonResponse({'message': '저장 성공'})


@api_view(['GET'])
@permission_classes([AllowAny]) #모두 권한 설정
def deposit_products(request):
    products = DepositProducts.objects.prefetch_related('options')
    result = []
    for product in products:
        product_data = {
            'dcls_month': product.dcls_month,
            'kor_co_nm': product.kor_co_nm,
            'fin_prdt_nm': product.fin_prdt_nm,
            'join_way': product.join_way,
            'spcl_cnd': product.spcl_cnd,
            'join_deny': product.join_deny,
            'options': [
                {
                    'intr_rate': option.intr_rate,
                    'intr_rate2': option.intr_rate2,
                    'intr_rate_type_nm': option.intr_rate_type_nm,
                    'save_trm': option.save_trm
                } for option in product.options.all()
            ]
        }
        result.append(product_data)
    return JsonResponse(result, safe=False, encoder=DjangoJSONEncoder)



@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    options = DepositOptions.objects.filter(product=product)
    serializers = DepositOptionsSerializer(options, many=True)
    return JsonResponse(serializers.data, safe=False)


openai.api_key=settings.OPEN_API_KEY

@api_view(['POST'])
@permission_classes([AllowAny])
def chatbot_response(request):
    try:
        user_message = request.data.get('message')
        if not user_message:
            return Response({'error': 'Message is required'}, status=400)
        system_prompt = """
        당신은 금융 상품 추천 전문가입니다. 
        예금과 적금 상품에 대한 조언을 제공하고, 
        사용자의 재무 상황에 맞는 최적의 금융 상품을 추천해주세요.
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        chatbot_reply = response.choices[0].message.content
        return Response({'reply': chatbot_reply})
    except Exception as e:
        print("Error occurred:", str(e))
        return Response({'error': str(e)}, status=500)