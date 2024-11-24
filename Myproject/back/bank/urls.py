from django.urls import path
from . import views


urlpatterns = [
    path('save-deposit-products/', views.save_deposit_products, name='save_deposit_products'),
    path('deposit-products/', views.deposit_products, name='deposit_products'),
    path('deposit-products-options/<str:fin_prdt_cd>/', views.deposit_product_options, name='deposit_product_options'),
    path('deposit-products/top-rate/', views.top_rate, name='top_rate'),
    path('chatbot/', views.chatbot_response, name='chatbot'),  # 'api/'를 제거
]
