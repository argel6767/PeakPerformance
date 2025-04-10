from django.urls import path
from .views import (
    UserInfoView, UserRegistrationView, LoginView, LogoutView, 
    CookieTokenRefreshView, TwoFactorVerifyView,  # Add these new imports
    PasswordResetRequestView, PasswordResetConfirmView  # Add these new imports
)

urlpatterns = [
    path('user-info/', UserInfoView.as_view(), name = 'user-info'),
    path('register/', UserRegistrationView.as_view(), name = 'register-user'),
    path('login/', LoginView.as_view(), name = 'user-login'),
    path('logout/', LogoutView.as_view(), name = 'user-logout'),
    path('refresh/', CookieTokenRefreshView.as_view(), name = 'token-refresh'),
    path('verify-2fa/', TwoFactorVerifyView.as_view(), name='verify-2fa'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
