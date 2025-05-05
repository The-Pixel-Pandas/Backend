from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models import Case, When, Value, IntegerField

class UserManager(BaseUserManager):
    def create_user(self, user_name, gmail, password=None, **extra_fields):
        if not user_name:
            raise ValueError('The User Name field must be set')
        if not gmail:
            raise ValueError('The Gmail field must be set')
        
        user = self.model(
            user_name=user_name,
            gmail=self.normalize_email(gmail),
            **extra_fields
        )
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, gmail, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(user_name, gmail, password, **extra_fields)
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = None  # Remove the username field
    user_name = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    avatar = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 10)], default=1)
    email = models.EmailField(unique=True, null=True, blank=True)  # Add email field to match Django's default
    gmail = models.EmailField(unique=True)  # Keep gmail as the main email field
    password = models.CharField(max_length=255)
    all_rank = models.IntegerField(default=0)
    monthly_rank = models.IntegerField(default=0)
    weekly_rank = models.IntegerField(default=0)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    wallet_field = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    import uuid
    user_token = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Keep email and gmail in sync
        if not self.email and self.gmail:
            self.email = self.gmail
        elif not self.gmail and self.email:
            self.gmail = self.email
        super().save(*args, **kwargs)

    objects = UserManager()

    USERNAME_FIELD = 'gmail'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.user_name

    def update_ranks(self):
        # Update all ranks
        self.all_rank = self.get_rank('all_time_profit')
        self.monthly_rank = self.get_rank('monthly_profit')
        self.weekly_rank = self.get_rank('weekly_profit')
        self.save()

    def get_rank(self, category):
        # Get the rank for the given category
        if category == 'all_time_profit':
            return User.objects.filter(
                total_balance__gt=self.total_balance
            ).count() + 1
        elif category == 'monthly_profit':
            return User.objects.filter(
                total_balance__gt=self.total_balance
            ).count() + 1
        elif category == 'weekly_profit':
            return User.objects.filter(
                total_balance__gt=self.total_balance
            ).count() + 1
        elif category == 'all_time_volume':
            return User.objects.filter(
                wallet_field__gt=self.wallet_field
            ).count() + 1
        elif category == 'monthly_volume':
            return User.objects.filter(
                wallet_field__gt=self.wallet_field
            ).count() + 1
        elif category == 'weekly_volume':
            return User.objects.filter(
                wallet_field__gt=self.wallet_field
            ).count() + 1
        return 0

    # Custom method to calculate user's score
    def calculate_score(self):
        return self.total_balance + self.wallet_field

    # Method to update user's ranks
    def update_ranks(self):
        # Update all-time ranks
        self.all_rank = self.get_rank('all_time_volume')
        self.monthly_rank = self.get_rank('monthly_profit')
        self.weekly_rank = self.get_rank('weekly_profit')
        
        self.save()

    # Method to update user's token
    def update_token(self):
        self.user_token = f'user_token_{self.id}'
        self.save()

class Leaderboard(models.Model):
    id = models.AutoField(primary_key=True)
    start_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboards', null=True, blank=True)
    type_id = models.IntegerField()
    leaderboard_token = models.CharField(max_length=255, unique=True, null=True, blank=True)
    
    # Add the missing fields
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    wallet_field = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    all_rank = models.IntegerField(default=0)
    monthly_rank = models.IntegerField(default=0)
    weekly_rank = models.IntegerField(default=0)

    class Meta:
        db_table = 'leaderboard'

    def __str__(self):
        return f"Leaderboard {self.id} - {self.user.user_name if self.user else 'No User'}"
    def __str__(self):
        return self.user_name
class Medal(models.Model):
    medal_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    badge = models.CharField(max_length=100)

    def __str__(self):
        return self.name





# TransactionHistory Model
class TransactionHistory(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.TimeField()
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')  # Referencing 'user_id'

    def __str__(self):
        return f"Transaction {self.transaction_id}"


# Question Model
class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_description = models.TextField()
    question_topic = models.CharField(max_length=100)
    question_type = models.CharField(max_length=50)
    question_tag = models.CharField(max_length=50)
    question_volume = models.IntegerField()
    question_chance_yes = models.DecimalField(max_digits=5, decimal_places=2)
    question_chance_no = models.DecimalField(max_digits=5, decimal_places=2)
    question_token = models.CharField(max_length=255, blank=True, null=True)
    question_token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.question_topic


# News Model
class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    news_description = models.TextField()
    news_topic = models.CharField(max_length=100)
    news_type = models.CharField(max_length=50)
    news_tag = models.CharField(max_length=50)

    def __str__(self):
        return self.news_topic


# Comment Model
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')  # Referencing 'user_id'
    like_number = models.IntegerField()
    comment_date = models.DateField()
    comment_time = models.TimeField()

    def __str__(self):
        return f"Comment {self.comment_id}"


# Wallet Model (related to User)
class Wallet(models.Model):
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    user_id_fk = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")

    def __str__(self):
        return f"Wallet of {self.user_id_fk.user_name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    volume = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    winrate = models.IntegerField(default=0)
    rank_total_profit = models.IntegerField(default=0)
    rank_total_volume = models.IntegerField(default=0)
    rank_monthly_profit = models.IntegerField(default=0)
    rank_monthly_volume = models.IntegerField(default=0)
    rank_weekly_profit = models.IntegerField(default=0)
    rank_weekly_volume = models.IntegerField(default=0)
    medals = models.JSONField(default=list)  # Store a list of integers (1, 2, 3)
    avatar = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 9)], default=1)  # Range updated to 1-8
    job = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    favorite_subject = models.CharField(max_length=100, null=False, blank=True, default='Not specified')

    def save(self, *args, **kwargs):
        # Ensure all numeric fields are non-negative
        self.winrate = max(0, min(100, self.winrate))
        self.rank_total_profit = max(0, self.rank_total_profit)
        self.rank_total_volume = max(0, self.rank_total_volume)
        self.rank_monthly_profit = max(0, self.rank_monthly_profit)
        self.rank_monthly_volume = max(0, self.rank_monthly_volume)
        self.rank_weekly_profit = max(0, self.rank_weekly_profit)
        self.rank_weekly_volume = max(0, self.rank_weekly_volume)

        # Ensure favorite_subject is always a string
        if self.favorite_subject is None:
            self.favorite_subject = 'Not specified'
        elif not isinstance(self.favorite_subject, str):
            self.favorite_subject = str(self.favorite_subject)

        # Ensure medals only contain integers between 1 and 3
        if not all(isinstance(medal, int) and 1 <= medal <= 3 for medal in self.medals):
            raise ValueError("Medals must be a list of integers between 1 and 3.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.user_name}'s Profile"