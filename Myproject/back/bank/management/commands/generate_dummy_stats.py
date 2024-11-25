# bank/management/commands/generate_dummy_stats.py
from django.core.management.base import BaseCommand
from bank.models import Product, UserStatistics
import random

class Command(BaseCommand):
    def handle(self, *args, **options):
        age_groups = ['20대', '30대', '40대', '50대']
        genders = ['남성', '여성']
        
        for product in Product.objects.all():
            for age in age_groups:
                for gender in genders:
                    UserStatistics.objects.create(
                        product=product,
                        age_group=age,
                        gender=gender,
                        user_count=random.randint(50, 500),
                        avg_satisfaction=round(random.uniform(3.5, 4.8), 1)
                    )