# users/urls.py

from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, CurrentUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    
    # JWT auth endpoints:
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
# urlpatterns = [
#     path('register/', UserRegistrationView.as_view(), name='user-register'),
#     path('login/', UserLoginView.as_view(), name='user-login'),
#     path('logout/', UserLogoutView.as_view(), name='user-logout'),
#     path('me/', CurrentUserView.as_view(), name='current-user'),
#     # You might add password reset, change password etc. later
# ]