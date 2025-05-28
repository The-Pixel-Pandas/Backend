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
from .models import User, Profile, Wallet, Leaderboard, Task
from .serializer import UserSerializer, ProfileSerializer, LoginSerializer, LeaderboardSerializer, LeaderboardResponseSerializer, TaskSerializer, TaskCompletionSerializer
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
                    'id': user.id,  # Add the user's id here
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
    

class WalletView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access this view

    def get(self, request, *args, **kwargs):
        # Get the wallet for the authenticated user
        try:
            wallet = Wallet.objects.get(user_id_fk=request.user)  # Fetch the wallet linked to the user
        except Wallet.DoesNotExist:
            return Response({"detail": "Wallet not found."}, status=404)  # Handle case where wallet doesn't exist

        # Example: Update total_balance dynamically (if needed)
        wallet.total_balance += 10  # Example logic to update balance
        wallet.save()

        # Return the updated wallet data
        return Response({
            "user_id": wallet.user_id_fk.id,
            "user_name": wallet.user_id_fk.user_name,
            "total_balance": wallet.total_balance,
            "volume": wallet.calculate_volume(),  # Call the method to calculate volume
            "profit": wallet.calculate_profit()   # Call the method to calculate profit
        })    

class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get the transaction history for the authenticated user
        transactions = TransactionHistory.objects.filter(user=request.user)
        serializer = TransactionHistorySerializer(transactions, many=True)
        return Response(serializer.data)    
class QuestionCreateView(CreateAPIView):
    """
    API endpoint to create a new question.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionListView(APIView):
    """
    List all questions or create a new question.
    """
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

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
    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        winning_option_id = request.data.get('winning_option_id')
        if not winning_option_id:
            return Response({"error": "Winning option ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            question.resolve_question(winning_option_id)
            return Response({"message": "Question resolved successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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

            # Create the bet
            bet = Bet.objects.create(
                user=user,
                option=option,
                amount=amount
            )

            # Deduct from user's balance
            user.total_balance -= amount
            user.save()

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

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Task.objects.none()
        return Task.objects.all()

    @action(detail=False, methods=['post'])
    def complete_task(self, request):
        """
        Mark a task as completed and add the amount to user's total balance
        """
        serializer = TaskCompletionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        task_id = serializer.validated_data['task_id']
        try:
            task = Task.objects.get(task_id=task_id)
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if task.is_completed:
            return Response(
                {"detail": "Task is already completed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if task.complete_task(request.user):
            return Response({
                "detail": "Task completed successfully.",
                "amount_added": task.amount,
                "new_balance": request.user.total_balance
            }, status=status.HTTP_200_OK)
        
        return Response(
            {"detail": "Failed to complete task."},
            status=status.HTTP_400_BAD_REQUEST
        )
