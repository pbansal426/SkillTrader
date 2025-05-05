# users/views.py

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
# Import authenticate, login, logout (if needed for sessions) and get_user_model
from django.contrib.auth import authenticate, login, logout ,get_user_model
from django.contrib.auth.models import User # You might need this if not using get_user_model explicitly everywhere
from django.core.exceptions import ObjectDoesNotExist # Import ObjectDoesNotExist

from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer

# Get your custom user model
User = get_user_model()


# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all() # Use your User model
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        return user

class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # --- MODIFIED LOGIN LOGIC STARTS HERE ---
        try:
            # 1. Try to find the user by email (case-insensitive lookup is good practice)
            user = User.objects.get(email__iexact=email)
        except ObjectDoesNotExist:
            # 2. If user not found, return invalid credentials immediately
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        # 3. If user is found, check their password
        if user.check_password(password):
            # 4. Password is correct, now check if the user is active
            if user.is_active:
                # 5. User is valid and active - Proceed with login/token
                # Optionally login user if using sessions alongside tokens (e.g., for admin site access after API login)
                # from django.contrib.auth import login # Make sure login is imported if you uncomment below
                # login(request, user)

                # Get or create the DRF token
                token, created = Token.objects.get_or_create(user=user)

                # Return user data and the token
                return Response({
                    'token': token.key,
                    'user': UserSerializer(user).data # Return user details too
                }, status=status.HTTP_200_OK)
            else:
                # 6. User exists and password correct, but account is disabled
                return Response({'detail': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # 7. User exists, but password is incorrect
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        # --- MODIFIED LOGIN LOGIC ENDS HERE ---


class UserLogoutView(APIView):
     # Requires authentication to log out
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # Delete the user's token to log them out
        try:
            # Use request.user which is available because of TokenAuthentication
            request.user.auth_token.delete()
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
             # This case should ideally not happen if authenticated via TokenAuth,
             # but it's good to handle potential inconsistencies.
             return Response({'detail': 'No active token found for user.'}, status=status.HTTP_400_BAD_REQUEST)
        # Optionally, if using sessions:
        # from django.contrib.auth import logout # Make sure logout is imported if you uncomment below
        # logout(request)


class CurrentUserView(generics.RetrieveAPIView):
    # Requires authentication to access
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    # Override get_object to return the currently authenticated user
    def get_object(self):
        # request.user is set by the authentication class (TokenAuthentication)
        return self.request.user