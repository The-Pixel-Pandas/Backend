from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.validators import UniqueValidator
from .models import Profile, Leaderboard
from .utils import get_tokens_for_user
from rest_framework import serializers
from .models import Wallet
from .models import TransactionHistory
from .models import Question, Option, Bet
from .models import Question
from .models import Option
from .models import Profile

User = get_user_model()


from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User

class LoginSerializer(serializers.Serializer):
    gmail = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        gmail = data.get('gmail')
        password = data.get('password')

        if not gmail or not password:
            raise serializers.ValidationError("Both 'gmail' and 'password' are required.")

        # Authenticate the user
        user = authenticate(username=gmail, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials. Please try again.")

        data['user'] = user
        return data
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)  # Required
    gmail = serializers.EmailField(
        required=True,  # Required
        validators=[UniqueValidator(queryset=User.objects.all())]  # Ensure gmail is unique
    )
    user_name = serializers.CharField(
        required=True,  # Required
        validators=[UniqueValidator(queryset=User.objects.all())]  # Ensure user_name is unique
    )
    first_name = serializers.CharField(required=False, allow_blank=True)  # Optional
    last_name = serializers.CharField(required=False, allow_blank=True)  # Optional
    age = serializers.IntegerField(required=False, allow_null=True, min_value=0)  # Optional
    avatar = serializers.IntegerField(
        required=False,  # Optional
        min_value=1,
        max_value=8,
        default=1
    )
    total_balance = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, default=10000
    )  # Optional
    all_rank = serializers.IntegerField(required=False, default=0)  # Optional
    monthly_rank = serializers.IntegerField(required=False, default=0)  # Optional
    weekly_rank = serializers.IntegerField(required=False, default=0)  # Optional
    wallet_field = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, default=0.00
    )  # Optional

    class Meta:
        model = User
        fields = (
            'user_name', 'gmail', 'password', 'first_name', 'last_name', 'age',
            'avatar', 'total_balance', 'all_rank', 'monthly_rank', 'weekly_rank', 'wallet_field'
        )

    def validate_user_name(self, value):
        """
        Check if the username already exists.
        """
        if User.objects.filter(user_name=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_gmail(self, value):
        """
        Check if the email (gmail) already exists.
        """
        if User.objects.filter(gmail=value).exists():
            raise serializers.ValidationError("This gmail is already taken.")
        return value

    def create(self, validated_data):
        """
        Create and return a new user with JWT tokens.
        """
        # Ensure avatar defaults to 1 if not provided
        validated_data['avatar'] = validated_data.get('avatar', 1)

        # Create the user
        user = User.objects.create_user(
            user_name=validated_data['user_name'],
            gmail=validated_data['gmail'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password'],
            age=validated_data.get('age', 0),
            avatar=validated_data['avatar']
        )
        return user
    # def create(self, validated_data):
    #     """
    #     Ensure user_name and gmail are unique before proceeding to create the user
    #     """
    #     user_name = validated_data.get('user_name')
    #     if User.objects.filter(user_name=user_name).exists():
    #         raise serializers.ValidationError({"user_name": "This username is already taken."})

    #     # Create the user
    #     user = User.objects.create_user(
    #         user_name=validated_data['user_name'],
    #         gmail=validated_data['gmail'],
    #         password=validated_data['password'],
    #         first_name=validated_data.get('first_name', ''),
    #         last_name=validated_data.get('last_name', ''),
    #         age=validated_data.get('age', 0),
    #         avatar=validated_data.get('avatar', None),
    #         total_balance=validated_data.get('total_balance', 0.00),
    #         all_rank=validated_data.get('all_rank', 0),
    #         monthly_rank=validated_data.get('monthly_rank', 0),
    #         weekly_rank=validated_data.get('weekly_rank', 0),
    #         wallet_field=validated_data.get('wallet_field', 0),
    #     )
    #     return user
class ProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.user_name', read_only=True)
    email = serializers.EmailField(source='user.gmail', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    profit = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    volume = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    winrate = serializers.IntegerField(required=False, min_value=0, max_value=100)
    rank_total_profit = serializers.IntegerField(required=False, min_value=0)
    rank_total_volume = serializers.IntegerField(required=False, min_value=0)
    rank_monthly_profit = serializers.IntegerField(required=False, min_value=0)
    rank_monthly_volume = serializers.IntegerField(required=False, min_value=0)
    rank_weekly_profit = serializers.IntegerField(required=False, min_value=0)
    rank_weekly_volume = serializers.IntegerField(required=False, min_value=0)
    medals = serializers.JSONField(required=False, default=list)
    avatar = serializers.IntegerField(required=False, min_value=1, max_value=9, allow_null=True)
    job = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    gender = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    age = serializers.IntegerField(required=False, allow_null=True, min_value=0)
    favorite_subject = serializers.CharField(required=False, allow_null=True, allow_blank=True, default='Not specified')
    total_balance = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)  # Added total_balance

    def validate_favorite_subject(self, value):
        if value is None:
            return 'Not specified'
        return str(value)  # Ensure it's always a string

    def validate(self, data):
        # Ensure all numeric fields are non-negative
        for field in [
            'profit', 'volume', 'winrate', 'rank_total_profit', 'rank_total_volume',
            'rank_monthly_profit', 'rank_monthly_volume', 'rank_weekly_profit',
            'rank_weekly_volume', 'age'
        ]:
            if field in data and data[field] is not None and data[field] < 0:
                raise serializers.ValidationError({field: 'Must be non-negative'})
        
        # Ensure winrate is between 0 and 100
        if 'winrate' in data and data['winrate'] is not None:
            if data['winrate'] > 100:
                raise serializers.ValidationError({'winrate': 'Must be between 0 and 100'})
        
        # Ensure all string fields are valid
        for field in ['bio', 'location', 'job', 'gender', 'favorite_subject']:
            if field in data and data[field] is not None:
                data[field] = str(data[field])
        
        # Handle medals
        if 'medals' in data and data['medals'] is not None:
            if not isinstance(data['medals'], list):
                try:
                    data['medals'] = json.loads(data['medals'])
                except json.JSONDecodeError:
                    raise serializers.ValidationError({'medals': 'Must be a valid JSON array'})
        
        return data

    class Meta:
        model = Profile
        fields = [
            'user_id', 'user_name', 'email', 'bio', 'location', 'birth_date',
            'profit', 'volume', 'winrate', 'rank_total_profit', 'rank_total_volume',
            'rank_monthly_profit', 'rank_monthly_volume', 'rank_weekly_profit',
            'rank_weekly_volume', 'medals', 'avatar', 'job', 'gender', 'age',
            'favorite_subject', 'total_balance'  # Included total_balance
        ]
        read_only_fields = ['user_id', 'user_name', 'email', 'total_balance']  # Mark total_balance as read-only

    def update(self, instance, validated_data):
        """
        Update profile fields and save the instance.
        This method will update all fields that are passed in the request body.
        """
        # Update all fields in the profile instance
        instance.bio = validated_data.get('bio', instance.bio)
        instance.location = validated_data.get('location', instance.location)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.profit = validated_data.get('profit', instance.profit)
        instance.volume = validated_data.get('volume', instance.volume)
        instance.winrate = validated_data.get('winrate', instance.winrate)
        instance.rank_total_profit = validated_data.get('rank_total_profit', instance.rank_total_profit)
        instance.rank_total_volume = validated_data.get('rank_total_volume', instance.rank_total_volume)
        instance.rank_monthly_profit = validated_data.get('rank_monthly_profit', instance.rank_monthly_profit)
        instance.rank_monthly_volume = validated_data.get('rank_monthly_volume', instance.rank_monthly_volume)
        instance.rank_weekly_profit = validated_data.get('rank_weekly_profit', instance.rank_weekly_profit)
        instance.rank_weekly_volume = validated_data.get('rank_weekly_volume', instance.rank_weekly_volume)
        instance.medals = validated_data.get('medals', instance.medals)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.job = validated_data.get('job', instance.job)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.age = validated_data.get('age', instance.age)
        instance.favorite_subject = validated_data.get('favorite_subject', instance.favorite_subject)
        instance.total_balance = validated_data.get('total_balance', instance.total_balance)  # Added total_balance

        # Save the updated instance
        instance.save()
        return instance
    

class LeaderboardSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.user_name', read_only=True)
    profit = serializers.DecimalField(source='user.total_balance', max_digits=10, decimal_places=2, read_only=True)
    volume = serializers.DecimalField(source='user.wallet_field', max_digits=10, decimal_places=2, read_only=True)
    avatar = serializers.ImageField(source='user.avatar', read_only=True)
    rank_total_profit = serializers.IntegerField(read_only=True)
    rank_total_volume = serializers.IntegerField(read_only=True)
    rank_monthly_profit = serializers.IntegerField(read_only=True)
    rank_monthly_volume = serializers.IntegerField(read_only=True)
    rank_weekly_profit = serializers.IntegerField(read_only=True)
    rank_weekly_volume = serializers.IntegerField(read_only=True)

    class Meta:
        model = Leaderboard
        fields = ['id', 'user_name', 'profit', 'volume', 'avatar',
                 'rank_total_profit', 'rank_total_volume',
                 'rank_monthly_profit', 'rank_monthly_volume',
                 'rank_weekly_profit', 'rank_weekly_volume',
                 'start_time', 'type_id', 'leaderboard_token']

class LeaderboardResponseSerializer(serializers.Serializer):
    all_time = serializers.DictField()
    monthly = serializers.DictField()
    weekly = serializers.DictField()

    def to_representation(self, instance):
        # Get the page number from context
        page = self.context.get('page', 1)

        # Add 'id' to each user in the leaderboard response
        def add_user_id(data):
            return [
                {
                    'id': user.get('id') or user.get('user_id'),  # Include user ID
                    'avatar': user.get('avatar'),
                    'username': user.get('username'),
                    'rank': user.get('rank'),
                    'profit': user.get('profit'),
                    'volume': user.get('volume'),
                    'token': user.get('token'),
                }
                for user in data
            ]

        # Prepare the response
        return {
            'all_time': {
                'volume': add_user_id(instance['all_time']['volume']),
                'profit': add_user_id(instance['all_time']['profit'])
            },
            'monthly': {
                'volume': add_user_id(instance['monthly']['volume']),
                'profit': add_user_id(instance['monthly']['profit'])
            },
            'weekly': {
                'volume': add_user_id(instance['weekly']['volume']),
                'profit': add_user_id(instance['weekly']['profit'])
            },
            'next': f"http://127.0.0.1:8000/api/leaderboards/?page={page + 1}" if page < 5 else None,
            'previous': f"http://127.0.0.1:8000/api/leaderboards/?page={page - 1}" if page > 1 else None
        }

    def get_next(self, obj):
        page = self.context.get('page', 1)
        if page < 4:  # Assuming 4 pages for 6 rankings
            return f'http://127.0.0.1:8000/api/leaderboards/?page={page + 1}'
        return None

    def get_previous(self, obj):
        page = self.context.get('page', 1)
        if page > 1:
            return f'http://127.0.0.1:8000/api/leaderboards/?page={page - 1}'
        return None

    class Meta:
        fields = ['current_node', 'next', 'previous']#github 


class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = ['transaction_id', 'question', 'amount', 'time', 'date', 'user']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'question_id',
            'question_description',
            'question_topic',
            'question_type',
            'question_tag',
            'question_volume',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['question_id', 'created_at', 'updated_at']
class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = ['user', 'amount']        

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['option_id', 'question', 'description', 'total_balance']
        read_only_fields = ['option_id', 'question', 'total_balance']  # Make 'question' and 'total_balance' read-only