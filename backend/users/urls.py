# users/urls.py

from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, CurrentUserView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    # You might add password reset, change password etc. later
]