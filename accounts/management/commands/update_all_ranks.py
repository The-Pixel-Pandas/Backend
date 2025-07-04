from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Update ranks for all users'

    def handle(self, *args, **options):
        users = User.objects.all()
        total = users.count()
        
        self.stdout.write(f'Updating ranks for {total} users...')
        
        updated = 0
        for user in users:
            try:
                with transaction.atomic():
                    user.update_ranks()
                updated += 1
                if updated % 100 == 0:
                    self.stdout.write(f'Updated {updated}/{total} users...')
            except Exception as e:
                self.stderr.write(f'Error updating user {user.id}: {str(e)}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated ranks for {updated}/{total} users'))
