from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, SignupView, ProfileViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),  # Add 'api/' prefix here
    path('api/signup/', SignupView.as_view(), name='signup'),  # Add 'api/' prefix here
    path('api/', include(router.urls)),  # This will include all profile endpoints
]
