from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)  # Made nullable
    gmail = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    all_rank = models.IntegerField(default=0)
    monthly_rank = models.IntegerField(default=0)
    weekly_rank = models.IntegerField(default=0)
    wallet_field = models.IntegerField(default=0)
    total_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Use user_name as the username field
    username = None  # Remove the username field
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gmail']

    def __str__(self):
        return self.user_name
    
class Medal(models.Model):
    medal_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    badge = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# LeaderBoard Model
class LeaderBoard(models.Model):
    leaderboard_id = models.AutoField(primary_key=True)
    start_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')  # Correctly referencing 'user_id'
    type_id = models.IntegerField()

    def __str__(self):
        return f"Leaderboard {self.leaderboard_id}"


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
    User_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet", to_field='id')  # Referencing 'user_id'
    TotalBalance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Wallet of {self.User_id.user_name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    website = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.user_name}'s Profile"
