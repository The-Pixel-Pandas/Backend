from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.urls import path, include
from core.urls import urlpatterns

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="""
        # Authentication Instructions
        
        1. First, use the `/api/login/` endpoint to get your JWT token
        2. Click the 'Authorize' button at the top of the page
        3. Enter your token in the format: `Bearer your_token_here`
        4. Click 'Authorize'
        
        All subsequent requests will include your token automatically.
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your-email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(),  # Remove authentication for schema generation
    patterns=urlpatterns,  # Include all URL patterns
)

# Add security scheme definition
schema_view.security_definitions = {
    "Bearer": {
        "type": "apiKey",
        "name": "Authorization",
        "in": "header",
        "description": "JWT Authorization header using the Bearer scheme. Example: \"Bearer {token}\""
    }
}

# Add security requirement to all operations
schema_view.security = [{"Bearer": []}] 