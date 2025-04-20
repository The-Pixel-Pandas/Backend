from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    """
    Utility function to generate JWT tokens for the given user.
    Adds user_id to the token payload instead of the default id.
    """
    refresh = RefreshToken.for_user(user)
    
    # Add the custom user_id to the token payload (instead of id)
    refresh.payload['user_id'] = user.user_id  # Use 'user_id' instead of 'id'
    
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }
