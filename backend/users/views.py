"""
Views for User authentication
"""
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings

from .serializers import (
    RegisterSerializer, 
    LoginSerializer, 
    GoogleAuthSerializer,
    UserSerializer
)

User = get_user_model()


def get_tokens_for_user(user):
    """Generate JWT tokens for user"""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration
    POST /auth/register/
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        tokens = get_tokens_for_user(user)
        user_data = UserSerializer(user).data
        
        return Response({
            'user': user_data,
            'tokens': tokens,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    API endpoint for user login
    POST /auth/login/
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            tokens = get_tokens_for_user(user)
            user_data = UserSerializer(user).data
            
            return Response({
                'user': user_data,
                'tokens': tokens,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)


class GoogleAuthView(APIView):
    """
    API endpoint for Google OAuth login/signup
    POST /auth/google/
    """
    permission_classes = (AllowAny,)
    serializer_class = GoogleAuthSerializer
    
    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        
        try:
            # Verify the token with Google
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                settings.GOOGLE_CLIENT_ID
            )
            
            # Extract user info from Google
            google_id = idinfo['sub']
            email = idinfo['email']
            username = idinfo.get('name', email.split('@')[0])
            
            # Check if user exists
            user, created = User.objects.get_or_create(
                google_id=google_id,
                defaults={
                    'email': email,
                    'username': username,
                }
            )
            
            # If user exists but was created with email/password, link Google account
            if not created and not user.google_id:
                user.google_id = google_id
                user.save()
            
            tokens = get_tokens_for_user(user)
            user_data = UserSerializer(user).data
            
            return Response({
                'user': user_data,
                'tokens': tokens,
                'message': 'Google authentication successful',
                'is_new_user': created
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            # Invalid token
            return Response({
                'error': 'Invalid Google token',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to get/update user profile
    GET/PUT /auth/profile/
    """
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
