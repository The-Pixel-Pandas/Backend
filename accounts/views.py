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
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Sum
from django.db.models.functions import Abs
from .models import User, Profile, Wallet, Leaderboard, Task, News, Comment, NewsComment
from .serializer import UserSerializer, ProfileSerializer, LoginSerializer, LeaderboardSerializer, LeaderboardResponseSerializer, TaskSerializer, TaskCompletionSerializer, NewsSerializer, CommentSerializer, NewsCommentSerializer
from .utils import get_tokens_for_user
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Wallet
from .models import TransactionHistory
from .serializer import TransactionHistorySerializer
from .models import Question
from .serializer import QuestionSerializer
from .models import Question, Option, Bet
from .serializer import QuestionSerializer, BetSerializer
from rest_framework.generics import ListCreateAPIView
from django.shortcuts import get_object_or_404
from .models import Option, Question
from .serializer import OptionSerializer
from .models import SiteBalance
from rest_framework import generics
from .models import Option
from .serializer import OptionSerializer
from rest_framework import generics
from .models import Option, Question
from .serializer import OptionSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Option, Question, User, SiteBalance
from .serializer import OptionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SiteBalance
from .serializer import SiteBalanceSerializer
from decimal import Decimal
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Option, Question, User
from .serializer import OptionSerializer
from decimal import Decimal
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from django.db import transaction
from rest_framework import serializers
from rest_framework.decorators import action
from .models import TransactionHistory

# Add StandardResultsSetPagination class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

User = get_user_model()



# Login view using JWT
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']  # Get the authenticated user

        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            # Check if the username is "admin"
            is_admin = user.user_name == "admin"

            # Fetch the user's profile
            profile = Profile.objects.get(user=user)

            # Prepare the response
            return Response({
                'user': {
                    'id': user.id,
                    'user_name': user.user_name,
                    'email': user.gmail,
                    'age': user.age,
                    'avatar': user.avatar,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'total_balance': user.total_balance,
                    'wallet_field': user.wallet_field,
                    'user_token': user.user_token,
                    'bio': profile.bio,
                    'location': profile.location,
                    'birth_date': profile.birth_date,
                    'profit': str(profile.profit),
                    'volume': str(profile.volume),
                    'winrate': profile.winrate,
                    'rank_total_profit': profile.rank_total_profit,
                    'rank_total_volume': profile.rank_total_volume,
                    'rank_monthly_profit': profile.rank_monthly_profit,
                    'rank_monthly_volume': profile.rank_monthly_volume,
                    'rank_weekly_profit': profile.rank_weekly_profit,
                    'rank_weekly_volume': profile.rank_weekly_volume,
                    'medals': profile.medals,
                    'job': profile.job,
                    'gender': profile.gender,
                    'favorite_subject': profile.favorite_subject
                },
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                },
                'is_admin': is_admin  # Add this field to indicate if the user is "admin"
            }, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
# Signup view
class SignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Ensure avatar has a default value if not provided
        avatar = request.data.get('avatar', 1)  # Default to 1 if avatar is not provided
        user_name = request.data.get('user_name')

        serializer = self.get_serializer(data={**request.data, 'avatar': avatar})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create a profile for the user
        profile = Profile.objects.create(
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

        # Check if the username is "admin"
        is_admin = user_name == "admin"

        # Prepare the response
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'user_name': user.user_name,
                'email': user.gmail,
                'age': user.age,
                'avatar': user.avatar,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'total_balance': user.total_balance,
                'wallet_field': user.wallet_field,
                'user_token': user.user_token,
                'bio': profile.bio,
                'location': profile.location,
                'birth_date': profile.birth_date,
                'profit': str(profile.profit),
                'volume': str(profile.volume),
                'winrate': profile.winrate,
                'rank_total_profit': profile.rank_total_profit,
                'rank_total_volume': profile.rank_total_volume,
                'rank_monthly_profit': profile.rank_monthly_profit,
                'rank_monthly_volume': profile.rank_monthly_volume,
                'rank_weekly_profit': profile.rank_weekly_profit,
                'rank_weekly_volume': profile.rank_weekly_volume,
                'medals': profile.medals,
                'job': profile.job,
                'gender': profile.gender,
                'favorite_subject': profile.favorite_subject
            },
            'is_admin': is_admin  # Add this field to indicate if the user is "admin"
        }, status=status.HTTP_201_CREATED)
    
class ProfileViewSet(viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return profiles belonging to the authenticated user.
        """
        if not self.request.user.is_authenticated:
            return Profile.objects.none()
        return Profile.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific profile by ID"""
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED
            )

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
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED
            )

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
                if 1 <= avatar_value <= 8:
                    request.data['avatar'] = avatar_value
                else:
                    return Response(
                        {"avatar": ["Value must be between 1 and 8"]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except (ValueError, TypeError):
                return Response(
                    {"avatar": ["Invalid value. Must be an integer between 1 and 8"]},
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
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED
            )

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
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED
            )

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

                # Get user's profile
                try:
                    profile = user.profile
                except Profile.DoesNotExist:
                    profile = None

                # Create ranking entry
                ranking_entry = {
                    'id': user.id,
                    'avatar': user.avatar if user.avatar else None,
                    'username': user.user_name,
                    'rank': rank,
                    'profit': float(user.total_balance),
                    'volume': float(user.wallet_field),
                    'token': user.user_token,
                    'bio': profile.bio if profile else '',
                    'medals': profile.medals if profile else [],
                    'total_balance': float(user.total_balance),
                    'winrate': profile.winrate if profile else 0,
                    'job': profile.job if profile else None,
                    'location': profile.location if profile else None,
                    'favorite_subject': profile.favorite_subject if profile else 'Not specified'
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
    

class WalletView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access this view

    def get(self, request, *args, **kwargs):
        # Get the user's balance directly from the User model
        user = request.user
        
        # Calculate volume (total BET amounts) and profit (total WIN amounts)
        volume = (
            TransactionHistory.objects.filter(user=user, transaction_type='BET')
            .aggregate(total=Sum(Abs('amount')))
            .get('total') or 0
        )
        profit = (
            TransactionHistory.objects.filter(user=user, transaction_type='WIN')
            .aggregate(total=Sum(Abs('amount')))
            .get('total') or 0
        )
        volume = max(volume, 0)
        profit = max(profit, 0)

        # Sync profile metrics
        try:
            profile = Profile.objects.get(user=user)
            profile.volume = volume
            profile.profit = profit
            profile.save()
        except Profile.DoesNotExist:
            pass

        return Response({
            "user_id": user.id,
            "user_name": user.user_name,
            "total_balance": float(user.total_balance),
            "volume": float(volume),
            "profit": float(profit)
        })

class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        # Get the transaction history for the authenticated user
        transactions = TransactionHistory.objects.filter(user=request.user)
        
        # Filter by transaction type if provided
        transaction_type = request.query_params.get('type')
        if transaction_type:
            transactions = transactions.filter(transaction_type=transaction_type)
        
        # Filter by date range if provided
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date:
            transactions = transactions.filter(date__gte=start_date)
        if end_date:
            transactions = transactions.filter(date__lte=end_date)
        
        # Order by most recent first
        transactions = transactions.order_by('-date', '-time')
        
        # Apply pagination
        paginator = self.pagination_class()
        paginated_transactions = paginator.paginate_queryset(transactions, request)
        
        # Serialize the paginated data with request context
        serializer = TransactionHistorySerializer(
            paginated_transactions, 
            many=True,
            context={'request': request}
        )
        
        # Return paginated response
        return paginator.get_paginated_response(serializer.data)

class QuestionCreateView(CreateAPIView):
    """
    API endpoint to create a new question.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = QuestionPagination

    def is_admin_user(self, user):
        """Check if user is admin (either is_staff or username is 'admin')"""
        return user.is_staff or user.user_name == "admin"

    def get_remaining_questions(self, user):
        """Get the number of questions the user can still create today"""
        if self.is_admin_user(user):  # Admin users have no limit
            return "unlimited"
        
        today = timezone.now().date()
        questions_today = Question.objects.filter(
            user=user,
            created_at__date=today
        ).count()
        
        return max(0, 5 - questions_today)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            
            # Get the created question
            question = serializer.instance
            
            # Get remaining questions count
            remaining = "unlimited" if self.is_admin_user(request.user) else self.get_remaining_questions(request.user)
            
            headers = self.get_success_headers(serializer.data)
            return Response({
                **serializer.data,
                'remaining_questions': remaining
            }, status=status.HTTP_201_CREATED, headers=headers)
        except serializers.ValidationError as e:
            if isinstance(e.detail, dict) and 'error' in e.detail:
                return Response(e.detail, status=status.HTTP_403_FORBIDDEN)
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            # Add remaining questions count for authenticated users
            if request.user.is_authenticated:
                response.data['remaining_questions'] = "unlimited" if self.is_admin_user(request.user) else self.get_remaining_questions(request.user)
            return response
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Question.objects.all()
        
        # Filter by topic
        topic = self.request.query_params.get('topic', None)
        if topic:
            queryset = queryset.filter(question_topic__icontains=topic)
        
        # Filter by type
        question_type = self.request.query_params.get('type', None)
        if question_type:
            queryset = queryset.filter(question_type__icontains=question_type)
        
        # Filter by tag
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(question_tag__icontains=tag)
        
        # Filter by search term (searches in description and topic)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(question_description__icontains=search) |
                Q(question_topic__icontains=search)
            )
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Order by newest first
        return queryset.order_by('-created_at')

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def update(self, request, *args, **kwargs):
        """
        Update a question.
        Only admin users can update questions.
        Partial updates are allowed.
        """
        if not request.user.is_authenticated or request.user.user_name != "admin":
            return Response(
                {"detail": "Only admin users can update questions."},
                status=status.HTTP_403_FORBIDDEN
            )
        partial = True  # Always allow partial updates
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a question.
        Only admin users can delete questions.
        """
        if not request.user.is_authenticated or request.user.user_name != "admin":
            return Response(
                {"detail": "Only admin users can delete questions."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

class QuestionDetailView(APIView):
    """
    Retrieve a specific question.
    """
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

class ResolveQuestionView(APIView):
    """
    Resolve a question and distribute winnings.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # Check if user is admin
        if not request.user.is_authenticated or request.user.user_name != "admin":
            return Response(
                {"error": "Only admin users can resolve questions."},
                status=status.HTTP_403_FORBIDDEN
            )

        question = get_object_or_404(Question, pk=pk)
        winning_option_id = request.data.get('winning_option_id')
        
        if not winning_option_id:
            return Response(
                {"error": "Winning option ID is required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Get the winning option
            winning_option = question.options.get(pk=winning_option_id)
            losing_option = question.options.exclude(pk=winning_option_id).first()
            
            # Calculate total volumes
            winning_volume = winning_option.option_volume
            losing_volume = losing_option.option_volume
            
            # Resolve the question
            question.resolve_question(winning_option_id)
            
            # Get all transactions for this question
            transactions = TransactionHistory.objects.filter(
                question=question,
                transaction_type__in=['WIN', 'LOSS']
            ).order_by('-date', '-time')
            
            # Prepare response data
            response_data = {
                "message": "Question resolved successfully.",
                "question_id": question.question_id,
                "winning_option": {
                    "id": winning_option.option_id,
                    "description": winning_option.description,
                    "volume": float(winning_volume)
                },
                "losing_option": {
                    "id": losing_option.option_id,
                    "description": losing_option.description,
                    "volume": float(losing_volume)
                },
                "transactions": [{
                    "transaction_id": t.transaction_id,
                    "user_id": t.user.id,
                    "user_name": t.user.user_name,
                    "amount": float(t.amount),
                    "type": t.transaction_type,
                    "date": t.date,
                    "time": t.time
                } for t in transactions]
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Option.DoesNotExist:
            return Response(
                {"error": "Invalid winning option ID."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class PlaceBetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            option = Option.objects.get(pk=pk)
            user = request.user
            amount = Decimal(request.data.get('amount', 0))

            # Validate the bet amount
            if amount % 100 != 0 or amount < 100 or amount > 10000:
                return Response(
                    {"error": "Amount must be a multiple of 100 between 100 and 10,000."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if question is active
            if not option.question.is_active:
                return Response(
                    {"error": "This question is no longer active for betting."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check user's balance
            if user.total_balance < amount:
                return Response(
                    {"error": "Insufficient balance."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Use transaction to ensure atomicity
            with transaction.atomic():
                # Create the bet
                bet = Bet.objects.create(
                    user=user,
                    option=option,
                    amount=amount
                )

                # Create transaction history entry with negative amount for bet
                TransactionHistory.objects.create(
                    question=option.question,
                    amount=-amount,  # Negative amount for bet
                    user=user,
                    option=option,
                    transaction_type='BET'
                )

                # Update balances across all models
                user.total_balance -= amount
                user.save()

                # Update wallet balance
                wallet = Wallet.objects.get(user_id_fk=user)
                wallet.total_balance = user.total_balance
                wallet.save()

                # Update profile balance
                profile = Profile.objects.get(user=user)
                profile.total_balance = user.total_balance
                profile.save()

                # Update option volume and question volume
                option.update_option_volume(amount)

                # Update chances for all options
                for opt in option.question.options.all():
                    opt.update_chance(option.question.question_volume)

            return Response({
                "message": "Bet placed successfully.",
                "bet_id": bet.bet_id,
                "amount": amount,
                "option": option.description,
                "question": option.question.question_topic,
                "remaining_balance": user.total_balance,
                "option_volume": option.option_volume,
                "question_volume": option.question.question_volume
            }, status=status.HTTP_200_OK)

        except Option.DoesNotExist:
            return Response(
                {"error": "Option not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class EndQuestionView(APIView):
    def post(self, request, pk, *args, **kwargs):
        question = Question.objects.get(pk=pk)

        # Validate the question
        if not question.validate_question():
            return Response({"message": "Question invalidated due to insufficient bets."}, status=status.HTTP_400_BAD_REQUEST)

        # Resolve the question
        winning_option_id = request.data.get('winning_option_id')
        question.resolve_question(winning_option_id)

        return Response({"message": "Question resolved and rewards distributed."}, status=status.HTTP_200_OK)
    


class OptionListCreateView(generics.ListCreateAPIView):
    serializer_class = OptionSerializer

    def get_queryset(self):
        question_id = self.kwargs['question_id']
        return Option.objects.filter(question__question_id=question_id)

    def perform_create(self, serializer):
        # Get 'question_id' from the URL
        question_id = self.kwargs['question_id']
        question = Question.objects.get(question_id=question_id)

        # Get volume from request data and validate
        volume = question.question_volume

        if not volume or float(volume) <= 0:
            return Response({"error": "Invalid volume."}, status=status.HTTP_400_BAD_REQUEST)

        volume = Decimal(volume)

        user = self.request.user

        if user.total_balance < volume:
            return Response({"error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct volume from the user's total balance
        user.total_balance -= volume
        user.save()

        # Add volume to the question's total volume
        question.question_volume += volume
        question.save()

        # Create the option and associate with the question
        option = serializer.save(question=question)

        # Add the volume to the option's volume
        option.option_volume = volume
        option.save()

        # Return the created option data
        return Response(OptionSerializer(option).data, status=status.HTTP_201_CREATED)
    
class OptionListView(generics.ListAPIView):
    """
    View to list all options for a specific question.
    """
    serializer_class = OptionSerializer

    def get_queryset(self):
        """
        Optionally filter the options by the question ID passed in the URL.
        """
        question_id = self.kwargs['question_id']
        return Option.objects.filter(question_id=question_id)  


class SiteBalanceView(APIView):
    """
    View to handle the site's balance.
    """
    def get(self, request):
        # Get the first (or only) SiteBalance object
        site_balance = SiteBalance.objects.first()
        if not site_balance:
            return Response({"error": "Site balance not initialized"}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize and return the site balance
        serializer = SiteBalanceSerializer(site_balance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Update or create site balance
        balance_data = request.data.get("balance")
        if balance_data is None:
            return Response({"error": "Balance value is required"}, status=status.HTTP_400_BAD_REQUEST)

        site_balance, created = SiteBalance.objects.get_or_create(
            defaults={'balance': balance_data}  # Initialize with balance if it doesn't exist
        )

        if not created:
            site_balance.balance = balance_data
            site_balance.save()

        return Response({"message": "Site balance updated successfully"}, status=status.HTTP_200_OK)

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = News.objects.all()
        
        # Filter by topic
        topic = self.request.query_params.get('topic', None)
        if topic:
            queryset = queryset.filter(news_topic=topic)
            
        # Filter by type
        news_type = self.request.query_params.get('type', None)
        if news_type:
            queryset = queryset.filter(news_type=news_type)
            
        # Filter by tag
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(news_tag=tag)
            
        # Search in description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(news_description__icontains=search)
            
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save()

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Task.objects.all()
        task_topic = self.request.query_params.get('task_topic', None)
        task_type = self.request.query_params.get('task_type', None)
        task_tag = self.request.query_params.get('task_tag', None)
        
        if task_topic:
            queryset = queryset.filter(task_topic=task_topic)
        if task_type:
            queryset = queryset.filter(task_type=task_type)
        if task_tag:
            queryset = queryset.filter(task_tag=task_tag)
            
        return queryset

    def create(self, request, *args, **kwargs):
        # Check if user is admin
        if request.user.user_name != "admin":
            return Response(
                {'error': 'Only admin users can create tasks.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['post'], url_path='complete_task')
    def complete_task(self, request):
        user = request.user
        task_id = request.data.get('task_id')
        
        if not task_id:
            return Response(
                {'error': 'task_id is required.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return Response(
                {'error': 'Task not found.'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if user has already completed this task
        if TransactionHistory.objects.filter(
            user=user,
            task=task,
            transaction_type='TASK_REWARD'
        ).exists():
            return Response(
                {'error': 'You have already completed this task.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                # Get initial balances for logging
                initial_balance = user.total_balance
                initial_wallet = user.wallet_field
                
                # Calculate new balance
                new_balance = user.total_balance + task.amount

                # Update user's balance fields
                user.total_balance = new_balance
                user.wallet_field = new_balance  # Ensure wallet field matches total balance
                user.save()

                # Update profile's balance to match user's total_balance
                profile = Profile.objects.get(user=user)
                profile.total_balance = new_balance
                profile.save()

                # Create a transaction history record
                TransactionHistory.objects.create(
                    task=task,
                    amount=task.amount,
                    user=user,
                    transaction_type='TASK_REWARD'
                )

                # Verify final balances
                final_balance = user.total_balance
                final_wallet = user.wallet_field
                final_profile_balance = profile.total_balance

                # Log balance changes for debugging
                print(f"Task completion balance changes:")
                print(f"Initial balance: {initial_balance}")
                print(f"Task amount: {task.amount}")
                print(f"New balance: {new_balance}")
                print(f"Final user balance: {final_balance}")
                print(f"Final wallet: {final_wallet}")
                print(f"Final profile balance: {final_profile_balance}")

                return Response({
                    'message': 'Task completed successfully.',
                    'new_balance': float(new_balance),
                    'task_id': task_id,
                    'amount': float(task.amount),
                    'debug_info': {
                        'initial_balance': float(initial_balance),
                        'final_balance': float(final_balance),
                        'final_wallet': float(final_wallet),
                        'final_profile_balance': float(final_profile_balance)
                    }
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'Error completing task: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update user profile",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_name': openapi.Schema(type=openapi.TYPE_STRING, description='New username'),
                'bio': openapi.Schema(type=openapi.TYPE_STRING, description='User biography'),
                'job': openapi.Schema(type=openapi.TYPE_STRING, description='User job'),
                'location': openapi.Schema(type=openapi.TYPE_STRING, description='User location'),
                'favorite_subject': openapi.Schema(type=openapi.TYPE_STRING, description='User favorite subject'),
                'avatar': openapi.Schema(type=openapi.TYPE_INTEGER, description='User avatar number (1-8)'),
            }
        ),
        responses={
            200: openapi.Response(
                description="Profile updated successfully",
                schema=ProfileSerializer()
            ),
            400: "Bad Request",
            401: "Unauthorized",
            409: "Username already exists"
        }
    )
    def put(self, request):
        try:
            user = request.user
            profile = user.profile

            # Handle username update
            new_username = request.data.get('user_name')
            if new_username and new_username != user.user_name:
                # Check if username already exists (excluding current user)
                if User.objects.filter(user_name=new_username).exclude(id=user.id).exists():
                    return Response(
                        {"error": "This username is already taken"},
                        status=status.HTTP_409_CONFLICT
                    )
                user.user_name = new_username
                user.save()

            # Update profile fields
            profile.bio = request.data.get('bio', profile.bio)
            profile.job = request.data.get('job', profile.job)
            profile.location = request.data.get('location', profile.location)
            profile.favorite_subject = request.data.get('favorite_subject', profile.favorite_subject)

            # Handle avatar update
            avatar_value = request.data.get('avatar')
            if avatar_value is not None:
                try:
                    avatar_value = int(avatar_value)
                    if 1 <= avatar_value <= 8:
                        profile.avatar = avatar_value
                        user.avatar = avatar_value  # Update user's avatar as well
                        user.save()
                    else:
                        return Response(
                            {"error": "Avatar must be a number between 1 and 8"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except (ValueError, TypeError):
                    return Response(
                        {"error": "Avatar must be a valid number"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            profile.save()

            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class UpdateUserBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update user's total balance",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the user to update (optional, defaults to current user)'),
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Amount to add (positive) or subtract (negative)'),
            },
            required=['amount']
        ),
        responses={
            200: "Balance updated successfully",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden - Can only update own balance unless admin",
            404: "User not found"
        }
    )
    def post(self, request):
        user_id = request.data.get('user_id')
        amount = request.data.get('amount')

        if amount is None:
            return Response(
                {"error": "Amount is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            amount = Decimal(str(amount))
        except (ValueError, TypeError, InvalidOperation):
            return Response(
                {"error": "Invalid amount value."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # If no user_id provided, use the current user
        if not user_id:
            user = request.user
        else:
            try:
                user = User.objects.get(id=user_id)
                # Check if user is trying to update someone else's balance
                if user != request.user and request.user.user_name != "admin":
                    return Response(
                        {"error": "You can only update your own balance."},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        try:
            with transaction.atomic():
                # Update user's balance
                user.total_balance += amount
                user.save()

                # Update wallet balance
                wallet = Wallet.objects.get(user_id_fk=user)
                wallet.total_balance = user.total_balance
                wallet.save()

                # Update profile balance
                profile = Profile.objects.get(user=user)
                profile.total_balance = user.total_balance
                profile.save()

                # Create transaction history record
                TransactionHistory.objects.create(
                    amount=amount,
                    user=user,
                    transaction_type='BALANCE_UPDATE'
                )

                return Response({
                    "message": "Balance updated successfully",
                    "user_id": user.id,
                    "user_name": user.user_name,
                    "new_balance": float(user.total_balance),
                    "amount_changed": float(amount)
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error updating balance: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        question_id = self.kwargs.get('question_pk')
        return Comment.objects.filter(question_id=question_id)

    def perform_create(self, serializer):
        question_id = self.kwargs.get('question_pk')
        question = get_object_or_404(Question, pk=question_id)
        serializer.save(question=question)

    @action(detail=True, methods=['post'])
    def like(self, request, question_pk=None, pk=None):
        comment = self.get_object()
        user = request.user

        if comment.likes.filter(id=user.id).exists():
            comment.likes.remove(user)
            comment.like_number = comment.likes.count()  # Update like_number
            comment.save()
            return Response({'status': 'unliked'})
        else:
            comment.likes.add(user)
            comment.like_number = comment.likes.count()  # Update like_number
            comment.save()
            return Response({'status': 'liked'})
    

class NewsCommentViewSet(viewsets.ModelViewSet):
    serializer_class = NewsCommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter comments by news_pk from URL
        news_pk = self.kwargs.get('news_pk')
        return NewsComment.objects.filter(news_id=news_pk)
    
    def perform_create(self, serializer):
        # Automatically set the user to the currently logged-in user
        news_pk = self.kwargs.get('news_pk')
        news = News.objects.get(pk=news_pk)
        serializer.save(user=self.request.user, news=news)

    @action(detail=True, methods=['post'])
    def like(self, request, news_pk=None, pk=None):
        comment = self.get_object()
        user = request.user

        if comment.likes.filter(id=user.id).exists():
            comment.likes.remove(user)
            comment.like_number = comment.likes.count()
            comment.save()
            return Response({'status': 'unliked'})
        else:
            comment.likes.add(user)
            comment.like_number = comment.likes.count()
            comment.save()
            return Response({'status': 'liked'})