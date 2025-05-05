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
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView
from django.db.models import Q
from .models import User, Profile, Wallet, Leaderboard
from .serializer import UserSerializer, ProfileSerializer, LoginSerializer, LeaderboardSerializer, LeaderboardResponseSerializer
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
                'user': {
                    'id': user.id,
                    'gmail': user.gmail,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'total_balance': user.total_balance,
                    'wallet_field': user.wallet_field,
                    'all_rank': user.all_rank,
                    'monthly_rank': user.monthly_rank,
                    'weekly_rank': user.weekly_rank,
                    'avatar': user.avatar,  # Return the integer value of avatar
                    'user_name': user.user_name,
                    'user_token': user.user_token
                },
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
        # Ensure avatar has a default value if not provided
        avatar = request.data.get('avatar', 1)  # Default to 1 if avatar is not provided
        serializer = self.get_serializer(data={**request.data, 'avatar': avatar})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create a profile for the user
        Profile.objects.create(
            user=user,
            avatar=user.avatar,
            age=user.age,
            bio='',
            location='',
            birth_date=None,
            profit=0,
            volume=0,
            winrate=0,
            rank_total_profit=0,
            rank_total_volume=0,
            rank_monthly_profit=0,
            rank_monthly_volume=0,
            rank_weekly_profit=0,
            rank_weekly_volume=0,
            medals=[],
            job=None,
            gender=None,
            favorite_subject='Not specified'
        )

        # Generate tokens for the user
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'user_name': user.user_name,
                'email': user.gmail,
                'age': user.age,
                'avatar': user.avatar,
            }
        }, status=status.HTTP_201_CREATED)
class ProfileViewSet(viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return profiles belonging to the authenticated user
        return Profile.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific profile by ID"""
        profile_id = kwargs.get('pk')
        try:
            # Ensure the profile belongs to the authenticated user
            profile = Profile.objects.get(pk=profile_id, user=request.user)
        except Profile.DoesNotExist:
            return Response(
                {"detail": "You can only access your own profile."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Update a specific profile by ID"""
        profile_id = kwargs.get('pk')
        try:
            # Ensure the profile belongs to the authenticated user
            profile = Profile.objects.get(pk=profile_id, user=request.user)
        except Profile.DoesNotExist:
            return Response(
                {"detail": "You can only update your own profile."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Handle avatar field if it's in the request
        if 'avatar' in request.data:
            try:
                avatar_value = int(request.data['avatar'])
                if 1 <= avatar_value <= 9:
                    request.data['avatar'] = avatar_value
                else:
                    return Response(
                        {"avatar": ["Value must be between 1 and 9"]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except (ValueError, TypeError):
                return Response(
                    {"avatar": ["Invalid value. Must be an integer between 1 and 9"]},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        """Custom logic for updating a profile"""
        serializer.save()  # Save the updated profile

    def destroy(self, request, *args, **kwargs):
        """Delete a specific profile by ID"""
        profile_id = kwargs.get('pk')
        try:
            # Ensure the profile belongs to the authenticated user
            profile = Profile.objects.get(pk=profile_id, user=request.user)
        except Profile.DoesNotExist:
            return Response(
                {"detail": "You can only delete your own profile."},
                status=status.HTTP_403_FORBIDDEN
            )

        self.perform_destroy(profile)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        """Custom logic for deleting a profile"""
        instance.delete()
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get the current user's profile"""
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response(
                {"detail": "Profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

class LeaderboardViewSet(viewsets.ViewSet):
    serializer_class = LeaderboardSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get']  # Only allow GET requests

    def list(self, request, *args, **kwargs):
        # Get the page number from query parameters
        page = int(request.query_params.get('page', 1))

        # Get all users with non-zero profit and volume
        users = User.objects.filter(
            Q(total_balance__gt=0) | Q(wallet_field__gt=0)
        ).distinct()

        # Define ranking categories and their order
        ranking_categories = [
            ('all_time_volume', '-wallet_field'),
            ('all_time_profit', '-total_balance'),
            ('monthly_volume', '-wallet_field'),
            ('monthly_profit', '-total_balance'),
            ('weekly_volume', '-wallet_field'),
            ('weekly_profit', '-total_balance')
        ]

        # Dictionary to store rankings for each category
        rankings_dict = {category[0]: [] for category in ranking_categories}

        # Process each ranking category
        for category, order_by in ranking_categories:
            # Get top 20 users for this category
            top_users = users.order_by(order_by)[:20]

            # Process each user
            for rank, user in enumerate(top_users, start=1):
                # Update user's ranks and token
                user.update_ranks()
                user.update_token()

                # Create ranking entry
                ranking_entry = {
                    'avatar': user.avatar if user.avatar else None,
                    'username': user.user_name,
                    'rank': rank,  # Use the rank from the loop
                    'profit': float(user.total_balance),
                    'volume': float(user.wallet_field),
                    'token': user.user_token
                }

                # Add to appropriate category
                rankings_dict[category].append(ranking_entry)

        # Prepare the final response
        response_data = {
            'all_time': {
                'volume': rankings_dict['all_time_volume'],
                'profit': rankings_dict['all_time_profit']
            },
            'monthly': {
                'volume': rankings_dict['monthly_volume'],
                'profit': rankings_dict['monthly_profit']
            },
            'weekly': {
                'volume': rankings_dict['weekly_volume'],
                'profit': rankings_dict['weekly_profit']
            }
        }

        # Use the response serializer to format the data
        response_serializer = LeaderboardResponseSerializer(
            response_data,
            context={'page': page}
        )

        return Response(response_serializer.data)
    def create(self, request, *args, **kwargs):
        # Create a new leaderboard entry for the authenticated user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)