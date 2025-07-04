from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import (
    LoginView, SignupView, ProfileViewSet, WalletLeaderboardViewSet, get_csrf_token,
    WalletView, TransactionHistoryView, ResolveQuestionView, PlaceBetView,
    QuestionViewSet, OptionListCreateView, OptionListView, TaskViewSet,
    NewsViewSet, ProfileUpdateView, UpdateUserBalanceView, CommentViewSet, NewsCommentViewSet
)
from .views import SiteBalanceView

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'wallet-leaderboards', WalletLeaderboardViewSet, basename='wallet-leaderboard')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'news', NewsViewSet, basename='news')
router.register(r'questions', QuestionViewSet, basename='question')

# Create a nested router for comments
questions_router = routers.NestedDefaultRouter(router, r'questions', lookup='question')
questions_router.register(r'comments', CommentViewSet, basename='question-comments')

# Nested router for news comments
news_router = routers.NestedDefaultRouter(router, r'news', lookup='news')
news_router.register(r'comments', NewsCommentViewSet, basename='news-comments')

urlpatterns = [
    # Include the router URLs directly
    path('', include(router.urls)),  # Profile endpoints like /profiles/ and /profiles/me/
    path('', include(questions_router.urls)),
    path('', include(news_router.urls)),

    # Custom endpoint for updating profiles
    path('profiles/<int:pk>/', ProfileViewSet.as_view({'put': 'update'}), name='profile-update'),
    
    # Profile update endpoint for username and other fields
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update-view'),

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

    # User balance update endpoint
    path('update-balance/', UpdateUserBalanceView.as_view(), name='update-user-balance'),
]
