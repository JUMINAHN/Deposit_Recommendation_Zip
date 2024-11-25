from .models import UserPreferencePattern
from bank.models import DepositProducts, DepositOptions

# recommendations/services.py
class ProductRecommender:
    def __init__(self, user_info):
        self.age = user_info.get('age')
        self.income = user_info.get('income')
        self.asset = user_info.get('asset')
        
    def get_age_group(self):
        if self.age < 30: return '20대'
        elif self.age < 40: return '30대'
        elif self.age < 50: return '40대'
        else: return '50대 이상'
        
    def get_income_level(self):
        if self.income < 30000000: return '저소득'
        elif self.income < 50000000: return '중소득'
        else: return '고소득'
        
    def get_asset_level(self):
        if self.asset < 50000000: return '소액'
        elif self.asset < 100000000: return '중액'
        else: return '고액'
        
    def recommend_products(self, products):
        age_group = self.get_age_group()
        income_level = self.get_income_level()
        asset_level = self.get_asset_level()
        
        # 점수 기반 추천
        scored_products = []
        for product in products:
            score = 0
            
            # 연령대별 가중치
            if age_group == '20대' and float(product['maxRate2']) > 3.0:
                score += 3
            elif age_group in ['30대', '40대'] and 2.5 <= float(product['maxRate2']) <= 4.0:
                score += 2
                
            # 소득 수준별 가중치
            if income_level == '고소득' and float(product['maxRate2']) > 3.5:
                score += 2
                
            # 자산 규모별 가중치
            if asset_level == '고액' and float(product['maxRate2']) > 3.0:
                score += 2
                
            scored_products.append({
                **product,
                'score': score,
                'recommendation_reason': self.get_recommendation_reason(age_group, income_level, asset_level)
            })
            
        # 점수순 정렬 후 상위 5개 반환
        return sorted(scored_products, key=lambda x: (-x['score'], -float(x['maxRate2'])))[:5]
        
    def get_recommendation_reason(self, age_group, income_level, asset_level):
        reasons = {
            '20대': '높은 금리로 자산 형성에 유리',
            '30대': '안정적인 수익률과 리스크 밸런스',
            '40대': '안정적인 자산 운용에 적합',
            '고소득': '우대금리 혜택 극대화 가능',
            '고액': '큰 원금에 대한 이자 수익 극대화'
        }
        return reasons.get(age_group, '') + '\n' + reasons.get(income_level, '')
    




    def recommend_products(self, user):
        age_group = self.get_age_group(user.age)
        asset_range = self.get_asset_range(user.asset)
        income_range = self.get_income_range(user.income)

        # 유사 사용자 선호도 패턴 찾기
        similar_preferences = UserPreferencePattern.objects.filter(
            age_group=age_group,
            asset_range=asset_range,
            income_range=income_range
        ).order_by('-count')[:5]

        # 추천 상품 목록 생성
        recommended_products = []
        for pref in similar_preferences:
            product = DepositProducts.objects.filter(
                kor_co_nm=pref.preferred_product.bankname,
                fin_prdt_nm=pref.preferred_product.products
            ).first()
            if product:
                recommended_products.append(product)

        return recommended_products