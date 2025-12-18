from django.shortcuts import render
from .models import user_jwtservices
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserJWTSerializer
# Create your views here.
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
#signup view with jwt access-token and refresh token generation
from django.contrib.auth.models import User


def get_tokens_for_user(user):
    if not user:
        raise AuthenticationFailed('User not found')
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }





@api_view(['POST'])
def signup_view(request):
    """Create a Django auth User, return JWT tokens on success."""
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')

    if not username or not password:
        return Response({'detail': 'username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'detail': 'User with this username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)

    # Optionally keep a copy in the custom model for compatibility
    try:
        user_jwt = user_jwtservices.objects.create(username=username, email=email, password=password)
    except Exception:
        # If custom model save fails, ignore and proceed with Django User
        pass

    tokens = get_tokens_for_user(user)
    return Response(tokens, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_view(request):
    """Authenticate a user and return access and refresh tokens."""
    username = request.data.get('username')
    password = request.data.get('password')
    if username is None or password is None:
        return Response({'detail': 'Username and password required.'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    tokens = get_tokens_for_user(user)
    return Response(tokens, status=status.HTTP_200_OK)