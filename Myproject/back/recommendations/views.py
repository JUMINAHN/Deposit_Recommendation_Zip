from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import ProductRecommender

@api_view(['GET'])
def get_recommendations(request):
    user = request.user
    if not all([user.age, user.asset, user.income]):
        return Response({
            'error': '사용자 프로필 정보가 불완전합니다.'
        }, status=400)

    recommender = ProductRecommender()
    recommended_products = recommender.recommend_products(user)
    
    return Response({
        'recommendations': [
            {
                'bankname': product.kor_co_nm,
                'product_name': product.fin_prdt_nm,
                'interest_rate': product.options.first().intr_rate2 if product.options.exists() else 0,
                'join_way': product.join_way,
            } for product in recommended_products
        ]
    })