from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView, SignupView, ProfileViewSet, LeaderboardViewSet, get_csrf_token,
    WalletView, TransactionHistoryView, ResolveQuestionView, PlaceBetView,
    QuestionViewSet, OptionListCreateView, OptionListView, TaskViewSet,
    NewsViewSet
)
from .views import SiteBalanceView

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'leaderboards', LeaderboardViewSet, basename='leaderboard')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'news', NewsViewSet, basename='news')
router.register(r'questions', QuestionViewSet, basename='question')

urlpatterns = [
    # Include the router URLs directly
    path('', include(router.urls)),  # Profile endpoints like /profiles/ and /profiles/me/

    # Custom endpoint for updating profiles
    path('profiles/<int:pk>/', ProfileViewSet.as_view({'put': 'update'}), name='profile-update'),

    # Authentication endpoints
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),

    # CSRF Token endpoint
    path('csrf-token/', get_csrf_token, name='csrf-token'),

    # Wallet endpoint
    path('wallet/', WalletView.as_view(), name='wallet'),

    # Transaction history endpoint
    path('transaction-history/', TransactionHistoryView.as_view(), name='transaction-history'),

    # Question-related endpoints
    path('questions/<int:pk>/resolve/', ResolveQuestionView.as_view(), name='resolve-question'),

    # Option-related endpoints
    path('questions/<int:question_id>/options/', OptionListView.as_view(), name='option-list'),  # For listing options (GET)
    path('questions/<int:question_id>/options/create/', OptionListCreateView.as_view(), name='option-list-create'),  # For creating options (POST)

    # Bet-related endpoints
    path('options/<int:pk>/bets/', PlaceBetView.as_view(), name='place-bet'),
    
    path('site-balance/', SiteBalanceView.as_view(), name='site-balance'),
]
