from django.urls import path
from . import views


urlpatterns = [
    path('save-deposit-products/<str:topFinGrpNo>/<int:pageNo>/', views.save_deposit_products, name='save_deposit_products'),
    path('save-deposit-products2/<str:topFinGrpNo>/<int:pageNo>/', views.save_deposit_products2, name='save_deposit_products2'),
    path('deposit-products/', views.deposit_products, name='deposit_products'),
    path('deposit-products-options/<str:fin_prdt_cd>/', views.deposit_product_options, name='deposit_product_options'),
]
