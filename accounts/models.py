from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models import Case, When, Value, IntegerField
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from django.db import models
from django.utils.timezone import now
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal



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
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=10000)
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
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=10000)
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
    question_volume = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))  # Total volume of bets
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(default=now)  # End time for the question
    is_active = models.BooleanField(default=True)  # Status of the question (active or not)

    def __str__(self):
        return self.question_topic

def initialize_options(self):
    """
    Initialize options with 10 coins from the site's balance and update question volume.
    """
    site_balance = SiteBalance.objects.first()
    if not site_balance:
        raise ValueError("Site balance is not initialized.")

    # Create "Yes" and "No" options
    yes_option = Option.objects.create(question=self, description="Yes", total_balance=Decimal('10.00'))
    no_option = Option.objects.create(question=self, description="No", total_balance=Decimal('10.00'))

    # Deduct 10 coins for each option from the site's balance
    site_balance.deduct(Decimal('10.00'))
    site_balance.deduct(Decimal('10.00'))

    # Update the question volume
    self.question_volume += Decimal('20.00')  # 10 coins for each option
    self.save()

def validate_question(self):
        """
        Validate the question at the end of its duration.
        If any option has less than 1,000 coins, invalidate the question and refund users.
        """
        for option in self.options.all():
            if option.total_bet < 1000.00:
                self.invalidate_question()
                return False
        return True

def invalidate_question(self):
        """
        Invalidate the question and refund all users.
        """
        for option in self.options.all():
            for bet in option.bets.all():
                bet.user.wallet.total_balance += bet.amount  # Refund the user's bet
                bet.user.wallet.save()
        self.is_active = False
        self.save()

def resolve_question(self, winning_option_id):
    """
    Resolve the question by distributing winnings to users who bet on the winning option.
    """
    if not self.validate_question():
        return

    winning_option = self.options.get(pk=winning_option_id)
    total_bet_all_options = sum(option.total_balance for option in self.options.all())
    site_balance = SiteBalance.objects.first()

    # Distribute winnings to users who bet on the winning option
    for bet in winning_option.bets.all():
        user_share = bet.amount / winning_option.total_balance  # User's share of the total bet on the winning option
        winnings = user_share * total_bet_all_options * Decimal('0.95')  # Deduct 5% for the site
        bet.user.wallet.total_balance += winnings
        bet.user.wallet.save()

    # Add 5% of the total bets to the site's balance
    site_balance.add(total_bet_all_options * Decimal('0.05'))

    # Mark the question as resolved
    self.is_active = False
    self.save()

class Option(models.Model):
    option_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    description = models.CharField(max_length=255)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)  # Use total_balance instead of balance
    chance = models.DecimalField(max_digits=5, decimal_places=2, default=50.00)  # Chance percentage

    def update_chance(self, total_volume):
        """
        Update the chance percentage based on the total volume of bets.
        """
        if total_volume > 0:
            self.chance = (self.total_balance / total_volume) * 100
        else:
            self.chance = 50.00  # Default to 50% if no bets
        self.save()
# Bet Model  
class Bet(models.Model):
    bet_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="bets")
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="bets")
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount the user bet
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Bet {self.bet_id} by {self.user.user_name} on {self.option.description}"
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
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=10000)
    user_id_fk = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")

    def calculate_volume(self):
        # Example logic for volume calculation
        return self.total_balance * 2  # Replace with your actual logic

    def calculate_profit(self):
        # Example logic for profit calculation
        return self.total_balance * Decimal('0.1')  # Replace with your actual logic

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
    total_balance = models.DecimalField(max_digits=15, decimal_places=2, default=10000.00)  # Added total_balance field

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
    
@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:  # Check if the user is newly created
        Wallet.objects.create(user_id_fk=instance)    
    
from decimal import Decimal

class SiteBalance(models.Model):
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('1000000.00'))  # Initial site balance

    def deduct(self, amount):
        """Deduct an amount from the site's balance."""
        self.balance -= Decimal(amount)  # Convert amount to Decimal
        self.save()

    def add(self, amount):
        """Add an amount to the site's balance."""
        self.balance += Decimal(amount)  # Convert amount to Decimal
        self.save()    

@receiver(post_save, sender=Question)
def initialize_question_options(sender, instance, created, **kwargs):
    if created:  # Only initialize options for newly created questions
        instance.initialize_options()        