from django.urls import path
from .views import LoginView, SignupView

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),  # Add 'api/' prefix here
    path('api/signup/', SignupView.as_view(), name='signup'),  # Add 'api/' prefix here
]
