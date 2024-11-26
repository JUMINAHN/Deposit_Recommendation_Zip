import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings


@api_view(['GET'])
@permission_classes([AllowAny])  # 이 뷰에 인증 없이 접근 가능하도록 설정
def exchange_rates(request):
    api_key = settings.EXCHANGE_RATE_API_KEY
    url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&searchdate=20241121&data=AP01'
    try:
        response = requests.get(url)
        response.raise_for_status()  # 요청 오류 발생 시 예외 발생
        exchange_rates = response.json()
        # 한국수출입은행에 요청해서 받아오는 데이터는 타입이 Result빼고는 다 String이라서 환율계산하려면 실수로 바꿔줘야함
        # 콤마 들어가있으면 바로 float으로 형변환 안됨, 콤마 제거 후 형변환하기
        for rate in exchange_rates:
            if type(rate['deal_bas_r']) == str:
                if ',' in rate['deal_bas_r']:
                    rate['deal_bas_r'] = float(rate['deal_bas_r'].replace(',', ''))
                else:
                    rate['deal_bas_r'] = float(rate['deal_bas_r'])  # 매매 기준율 실수로 변환
        return Response(exchange_rates)
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=400) # DRF에서는 Jsonresponse보다 그냥 Response로하는게 더 일관성 있음
