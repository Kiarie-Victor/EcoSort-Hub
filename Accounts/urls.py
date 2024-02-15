from django.urls import path
from Accounts.views import LoginView, RegistrationView, OtpVerification
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/register/', RegistrationView.as_view(), name='login'),
    path('api/otp_verification/', OtpVerification.as_view(), name="otp"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
