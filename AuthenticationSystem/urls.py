from django.urls import path
from .views import singin, manual_login, login

# ------------------------------
# Authentication API Endpoints
# Base URL prefix: /auth/
# ------------------------------
urlpatterns = [
    # ------------------------------
    # SIGN UP (User Registration)
    # Endpoint: POST /auth/singin/
    # Description:
    #   - Creates a new user account with type "normal"
    #   - Required fields: first_name, last_name, user_name, user_type, password
    #   - Returns: User data on successful creation
    #   - Permission: AllowAny (no authentication required)
    # ------------------------------
    path("singin/", singin, name="signin"),

    # ------------------------------
    # MANUAL LOGIN (Without JWT)
    # Endpoint: POST /auth/manual-login/
    # Description:
    #   - Authenticates user using id_code and password
    #   - If 'remember' = True → returns JWT tokens (access & refresh) + user data
    #   - If 'remember' = False → returns user data only (no tokens)
    #   - Permission: AllowAny (no authentication required)
    # ------------------------------
    path("manual-login/", manual_login, name="manual_login"),

    # ------------------------------
    # JWT LOGIN (Preferred Method)
    # Endpoint: POST /auth/login/
    # Description:
    #   - Validates the user's JWT token from the request headers
    #   - If valid → returns user dashboard info (no new tokens)
    #   - If invalid/missing → returns error (client should fallback to manual login)
    #   - Note: This endpoint is designed to work with JWT in Authorization header
    # ------------------------------
    path("login/", login, name="login"),
]