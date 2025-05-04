from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.validators import UniqueValidator
from .models import Profile
from .utils import get_tokens_for_user

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        user = authenticate(
            user_name=data['user_name'],
            password=data['password']
        )
        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')
        
        data['user'] = user
        return data

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    gmail = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]  # Ensure gmail is unique
    )
    avatar = serializers.ImageField(required=False, allow_null=True)  # Make avatar optional

    class Meta:
        model = User
        fields = ('user_name', 'gmail', 'first_name', 'last_name', 'password', 'age', 'avatar', 'total_balance', 'all_rank', 'monthly_rank', 'weekly_rank', 'wallet_field')

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
        # Create the user
        user = User.objects.create_user(
            user_name=validated_data['user_name'],
            gmail=validated_data['gmail'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            age=validated_data.get('age', 0),
            avatar=validated_data.get('avatar')
        )
        
        # Generate JWT tokens
        tokens = get_tokens_for_user(user)
        
        # Add tokens to the response
        validated_data['tokens'] = tokens
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
    bio = serializers.CharField(read_only=True)
    location = serializers.CharField(read_only=True)
    birth_date = serializers.DateField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    profit = serializers.DecimalField(source='user.total_balance', max_digits=10, decimal_places=2, read_only=True)
    volume = serializers.DecimalField(source='user.wallet_field', max_digits=10, decimal_places=2, read_only=True)
    winrate = serializers.SerializerMethodField()
    rank_total_profit = serializers.IntegerField(source='user.all_rank', read_only=True)
    rank_total_volume = serializers.IntegerField(source='user.all_rank', read_only=True)
    rank_monthly_profit = serializers.IntegerField(source='user.monthly_rank', read_only=True)
    rank_monthly_volume = serializers.IntegerField(source='user.monthly_rank', read_only=True)
    rank_weekly_profit = serializers.IntegerField(source='user.weekly_rank', read_only=True)
    rank_weekly_volume = serializers.IntegerField(source='user.weekly_rank', read_only=True)
    medals = serializers.SerializerMethodField()
    avatar = serializers.ImageField(source='user.avatar', read_only=True)
    job = serializers.CharField(source='user.job', read_only=True)
    gender = serializers.CharField(source='user.gender', read_only=True)
    age = serializers.IntegerField(source='user.age', read_only=True)
    favorite_subject = serializers.CharField(source='user.favorite_subject', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'user_name', 'email', 'bio', 'location',
            'birth_date', 'created_at', 'updated_at',
            'profit', 'volume', 'winrate', 'rank_total_profit', 'rank_total_volume',
            'rank_monthly_profit', 'rank_monthly_volume', 'rank_weekly_profit',
            'rank_weekly_volume', 'medals', 'avatar', 'job', 'gender', 'age',
            'favorite_subject'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_winrate(self, obj):
        # Implement winrate calculation logic here
        return 0  # Default value

    def get_medals(self, obj):
        # Implement medal retrieval logic here
        return []  # Default empty list

    def update(self, instance, validated_data):
        # Handle profile picture upload
        if 'profile_picture' in validated_data:
            instance.profile_picture = validated_data.pop('profile_picture')
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
