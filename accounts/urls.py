from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, SignupView, ProfileViewSet, LeaderboardViewSet, get_csrf_token

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'leaderboards', LeaderboardViewSet, basename='leaderboard')

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
]
