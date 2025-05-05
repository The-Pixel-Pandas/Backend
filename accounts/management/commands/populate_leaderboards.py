import random
from django.utils import timezone
from django.core.management.base import BaseCommand
from accounts.models import User, Leaderboard

class Command(BaseCommand):
    help = 'Populate the leaderboard with 1000 mock entries'

    def handle(self, *args, **kwargs):
        # Create 1000 mock users and leaderboard entries
        for i in range(1, 1001):
            user, created = User.objects.get_or_create(
                user_name=f'user_{i}',
                defaults={
                    'first_name': f'FirstName_{i}',
                    'last_name': f'LastName_{i}',
                    'gmail': f'user_{i}@example.com',
                    'password': 'password123',
                    'age': random.randint(18, 60),
                    'avatar': random.randint(1, 9),
                }
            )

            # Create leaderboard entry for the user
            Leaderboard.objects.create(
                user=user,
                total_balance=random.uniform(1000, 10000),
                wallet_field=random.uniform(500, 5000),
                all_rank=random.randint(1, 1000),
                monthly_rank=random.randint(1, 100),
                weekly_rank=random.randint(1, 50),
                start_time=timezone.now(),  # Set the current date and time
                type_id=random.randint(1, 5),
                leaderboard_token=f"token_{i}"
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated 1000 leaderboard entries'))