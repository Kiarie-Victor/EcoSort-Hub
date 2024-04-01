from django.urls import path
from Accounts.views import LoginView, RegistrationView, OtpVerification, ProfileView, DeleteProfile
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Define urlpatterns for API endpoints
urlpatterns = [
    # Endpoint for user login
    path('api/login/', LoginView.as_view(), name='login'),

    # Endpoint for user registration
    path('api/register/', RegistrationView.as_view(), name='register'),

    # Endpoint for OTP verification and user registration
    path('api/otp_verification/', OtpVerification.as_view(),
         name="otp_verification"),

    path('api/update_profile', ProfileView.as_view()),
    path('api/delete_account', DeleteProfile.as_view()),

    # Endpoint for obtaining access and refresh tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Endpoint for refreshing access token using refresh token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
