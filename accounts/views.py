from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from .models import User, Profile, Wallet
from .serializer import UserSerializer, ProfileSerializer, LoginSerializer
from .utils import get_tokens_for_user

User = get_user_model()



# Login view using JWT
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        if user is not None:
            # Get JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user_id': user.id,
                'gmail': user.gmail,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'total_balance': user.total_balance,
                'wallet': user.wallet_field,
                'rank': user.all_rank,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            })
        
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# Signup view

class SignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        tokens = get_tokens_for_user(user)
        
        return Response({
            'user_id': user.id,
            'gmail': user.gmail,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'total_balance': user.total_balance,
            'wallet': user.wallet_field,
            'rank': user.all_rank,
            'tokens': tokens
        }, status=status.HTTP_201_CREATED)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """Return appropriate permissions based on action"""
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """Return profiles for the current authenticated user"""
        if self.request.user.is_authenticated:
            return Profile.objects.filter(user=self.request.user)
        return Profile.objects.all()

    def perform_create(self, serializer):
        """Create a new profile for the current user"""
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Authentication required to create a profile")
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Update the current user's profile"""
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        """Delete the profile"""
        instance.delete()

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get the current user's profile"""
        profile = Profile.objects.get(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Update the current user's profile"""
        profile = Profile.objects.get(user=request.user)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Delete the current user's profile"""
        # Get the profile ID from the URL
        profile_id = kwargs.get('pk')
        
        # Get the profile associated with the current user
        profile = Profile.objects.get(user=request.user)
        
        # Verify that the profile ID in the URL matches the user's profile
        if str(profile.id) != profile_id:
            raise PermissionDenied("You can only delete your own profile")
            
        self.perform_destroy(profile)
        return Response(status=status.HTTP_204_NO_CONTENT)

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})