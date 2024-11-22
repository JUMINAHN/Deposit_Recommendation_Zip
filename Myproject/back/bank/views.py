from django.shortcuts import render
from django.http import JsonResponse

import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.conf import settings
from .models import DepositOptions, DepositProducts
from .serializers import DepositOptionsSerializer, DepositProductsSerializer, DepositOptionsCreateSerializer, DepositProductsCreateSerializer
from django.core.serializers.json import DjangoJSONEncoder


# Create your views here.
BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'

@api_view(['GET'])
def save_deposit_products(request):
    url = BASE_URL + 'depositProductsSearch.json'
    params = {
        'auth': settings.API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1
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

# @api_view(['GET'])
# def deposit_products(request):
#     products = DepositProducts.objects.all().prefetch_related('depositoptions_set')
#     serializers = DepositProductsSerializer(products, many=True)
#     return Response(serializers.data)


# @api_view(['GET', 'POST'])
# def deposit_products(request):
#     products = DepositProducts.objects.all()
#     if request.method == 'GET':
#         serializers = DepositProductsSerializer(products, many=True)
#         return JsonResponse(serializers.data, safe=False)
#     elif request.method == 'POST':
#         serializer = DepositProductsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         else:
#             return JsonResponse({'message': '이미 있는 데이터이거나, 데이터가 잘못 입력되었습니다.'})

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



@api_view(['GET'])
def top_rate(request):
    # 최고 우대 금리 옵션 찾기
    max_intr_rate2 = DepositOptions.objects.all().order_by('-intr_rate2').first()
    
    deposit_product = max_intr_rate2.product
    
    # deposit_product는 이미 DepositProducts 객체이므로 직접 사용
    product_serializers = DepositProductsSerializer(deposit_product)
    option_serializers = DepositOptionsSerializer(max_intr_rate2)
    
    return JsonResponse({
        'deposit_product': product_serializers.data,
        'options': option_serializers.data
    })





