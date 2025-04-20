from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['user_name', 'password']

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
