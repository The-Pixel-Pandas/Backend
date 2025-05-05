from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test data for leaderboard'

    def handle(self, *args, **options):
        # List of sample usernames
        usernames = ['av', 'ak', 'am', 'user1', 'user2', 'user3', 'user4', 'user5']
        
        # Create test users with different data
        for i, username in enumerate(usernames):
            # Generate realistic values
            total_balance = random.uniform(1000, 10000)
            wallet_field = random.uniform(5000, 50000)
            
            user = User.objects.create_user(
                user_name=username,
                first_name=f'First{username}',
                last_name=f'Last{username}',
                gmail=f'{username}@example.com',
                password='test123',
                age=25,
                total_balance=total_balance,
                wallet_field=wallet_field,
                monthly_rank=i + 1,
                weekly_rank=i + 1
            )
            
            # Update user's ranks
            user.update_ranks()
            user.update_token()
            
            self.stdout.write(self.style.SUCCESS(f'Created user {username}'))

        self.stdout.write(self.style.SUCCESS('Successfully created test data'))
