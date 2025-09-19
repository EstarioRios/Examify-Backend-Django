from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

# ------------------------------

from .models import CustomUser
from .serializers import (
    CustomUserFullSerializer,
    CustomUserListSerializer,
)

# ------------------------------


# Generate JWT access and refresh tokens for a user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user=user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


# Dashboard Response Generator
def choose_dashboard(user, tokens, msg="Login successful", remember=False):
    if not tokens:
        return Response(
            {
                "user_type": user.user_type,
                "success": msg,
                "user": FullCustomUserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )
    else:
        # if remember == True:
        return Response(
            {
                "user_type": user.user_type,
                "success": msg,
                "tokens": tokens,
                "user": FullCustomUserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )
    # else:
    #     return Response(
    #         {
    #             "user_type": user.user_type,
    #             "success": msg,
    #             "user": FullCustomUserSerializer(user).data,
    #         },
    #         status=status.HTTP_200_OK,
    #     )


@api_view(["POST"])
@permission_classes([AllowAny])
def singin(request):
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    user_name = request.data.get("user_name")
    user_type = request.data.get("user_type")
    password = request.data.get("password")

    if not all([first_name, last_name, user_name, user_type, password]):
        return Response(
            {"msg": "all fields are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if CustomUser.objects.filter(user_name=user_name).exists():
        return Response(
            {"msg": f"user_name: {user_name} is already exitst"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if user_type == "normal":
        try:
            user = CustomUser.objects.create_normal(
                first_name=first_name,
                last_name=last_name,
                user_name=user_name,
                password=password,
            )
            return Response(
                {"user": FullCustomUserSerializer(user).data},
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            return Response(
                {"msg": f"{e}"},
                status=status.HTTP_403_FORBIDDEN,
            )


# Manual login if JWT not present
@api_view(["POST"])
@permission_classes([AllowAny])
def manual_login(request):
    remember = request.data.get("remember")
    user_id_code = request.data.get("id_code")
    user_password = request.data.get("password")

    if not user_id_code or not user_password:
        return Response(
            {"msg": "id_code and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = CustomUser.objects.get(id_code=user_id_code)
        if user.check_password(user_password):
            if str(remember).strip().capitalize() == "True":
                return choose_dashboard(user, tokens=get_tokens_for_user(user))
            else:
                return choose_dashboard(user, tokens=None)
            # return choose_dashboard(
            #     user, tokens=get_tokens_for_user(user), remember=remember
            # )
        else:
            return Response(
                {"msg": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
    except CustomUser.DoesNotExist:
        return Response({"msg": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# Login view: prefer JWT, fallback to manual login
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def login(request):
    # remember = request.data.get("remember")
    # if not remember:
    #     remember = False

    try:

        user_auth = JWTAuthentication().authenticate(request)
        if not user_auth:
            return Response(
                {"msg": "your JWT isn't fine"}, status=status.HTTP_400_BAD_REQUEST
            )
            # return manual_login(request, remember=remember)

        else:
            user, _ = user_auth
            return choose_dashboard(user, tokens=None)

    except AuthenticationFailed:
        return Response(
            {"msg": "your JWT isn't fine"}, status=status.HTTP_400_BAD_REQUEST
        )
        # return manual_login(request, remember=remember)
