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
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'user_name', 'email', 'first_name', 'last_name',
            'bio', 'location', 'birth_date', 'phone_number',
            'website', 'profile_picture', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def update(self, instance, validated_data):
        # Handle profile picture upload
        if 'profile_picture' in validated_data:
            instance.profile_picture = validated_data.pop('profile_picture')
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
