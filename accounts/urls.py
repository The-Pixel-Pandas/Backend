from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, SignupView, ProfileViewSet, UserRegistrationView, UserLoginView, UserLogoutView, UserProfileView, get_csrf_token

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),  # Add 'api/' prefix here
    path('api/signup/', SignupView.as_view(), name='signup'),  # Add 'api/' prefix here
    path('api/', include(router.urls)),  # This will include all profile endpoints
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('csrf-token/', get_csrf_token, name='csrf-token'),
]
