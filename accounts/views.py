from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import get_user_model
from accounts.serializer import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from accounts.models import Wallet  # Adjust the import path based on your project structure
from rest_framework.generics import CreateAPIView
from accounts.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from accounts.models import User
from accounts.serializer import UserSerializer
from accounts.utils import get_tokens_for_user  # Import the utility function
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from accounts.models import User
from accounts.serializer import UserSerializer
from accounts.utils import get_tokens_for_user  # Import the updated utility function
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from accounts.utils import get_tokens_for_user
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from accounts.models import User
from accounts.serializer import UserSerializer, LoginSerializer
from accounts.utils import get_tokens_for_user
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from .models import Profile
from .serializer import ProfileSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

User = get_user_model()

# Utility function to generate JWT tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }

# Login view using JWT
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print("Login view called")
        validated_data = self.serializer_class(data=request.data)
        validated_data.is_valid(raise_exception=True)
        user = User.objects.get(user_name=validated_data.data['user_name'])
        if not user.password == validated_data.data['password']:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user is not None:
            # Get JWT tokens
            tokens = get_tokens_for_user(user)


            # Return the user details along with the JWT tokens and token count
            return Response({
                'user_id': user.id,  # Udese user_id instead of user.pk
                'gmail': user.gmail,  # Changed from email to gmail
                'first_name': user.first_name,
                'last_name': user.last_name,
                'total_balance': user.total_balance,
                'wallet': user.wallet_field,  # Assuming wallet_field is part of the User model
                'rank': user.all_rank,
                'tokens': tokens  # Return both access and refresh tokens
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# Signup view

class SignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Make sure this line is here!

    def perform_create(self, serializer):
        # Create the user
        user = serializer.save()

        # Generate JWT tokens using the updated function
        tokens = get_tokens_for_user(user)

        # Return user data along with the JWT tokens
        return Response({
            'id': user.id,  # Use user_id instead of id
            'email': user.gmail,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'tokens': tokens  # Returning both access and refresh tokens
        }, status=status.HTTP_201_CREATED)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own profile
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the profile with the current user
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def me(self, request):
        # Get or create profile for the current user
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def perform_update(self, serializer):
        # Ensure users can only update their own profile
        serializer.save(user=self.request.user)

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})