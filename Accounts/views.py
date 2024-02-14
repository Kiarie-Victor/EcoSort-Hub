from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from Accounts.models import PendingUserModel, Member, Otp
from Accounts.serializers import LoginSerializer, PendingDataSerializer, RegistrationSerializer
from django.db import transaction

# Create your views here.

# This login view handles the user login and token assigning after
# successful login
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(
            data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception = True)
            user = serializer.validated_data.get('user')
            if user is None:
                return Response({'detail': 'Invalid login credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Refresh token assigning for a successfully logged in user
            refresh = RefreshToken.for_user(user=user)

            # returning  response of both access and refresh tokens
            return Response({'access_token': str(refresh.access_token),
                            'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({"errors": str(e)})


class RegistrationView(APIView):
    throttle_classes = [AnonRateThrottle]

    def post(self, request):

        serializer = PendingDataSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                try:
                    # get all the data from the request
                    email = serializer.validated_data['email']
                    username = serializer.validated_data['username']
                    phone_number = serializer.validated_data['phone_number']
                    password = serializer.validated_data['password']

                    # handle otp generation and sending
                    otp_code = otp_generator.otp_generator()

                    otp_instance = Otp.objects.create(otp_code=otp_code)
                    otp_instance.save()
                    response = email_sender.sendEmail(
                        username=username, otp_code=otp_code, email=email)
                    if response:
                        # handling save PendingUserData
                        pending_user = PendingUserModel.objects.create(
                            user_otp=otp_code, username=username, email=email, phone_number=phone_number, password=password)
                        pending_user.save()
                        return Response({'Detail': 'Otp code sent successfully'}, status=status.HTTP_200_OK)

                    raise Exception('Error encountered when sending Email')

                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OtpVerification(APIView):
    def post(self, request):
        serializer = OtpSerializer(data=request.data)

        if serializer.is_valid():
            otp_code = serializer.validated_data['otp_code']
            try:
                with transaction.atomic():
                    try:
                        otp_instance = Otp.objects.get(otp_code=otp_code)

                    except Otp.DoesNotExist:
                        return Response({'error': 'Invalid OTP code.'}, status=status.HTTP_400_BAD_REQUEST)

                    if otp_expired.otp_expired(otp_timestamp=otp_instance.created_at):
                        otp_instance.delete()
                        return Response({'error': "Otp Expired"}, status=status.HTTP_400_BAD_REQUEST)

                    try:
                        pending_user = PendingUserModel.objects.get(
                            user_otp=otp_code)

                    except PendingUserModel.DoesNotExist:
                        return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

                    data = {
                        "username": pending_user.username,
                        "email": pending_user.email,
                        "phone_number": pending_user.phone_number,
                        "password": pending_user.password,
                    }

                    user = RegistrationSerializer(data=data)
                    if user.is_valid():
                        user.save()
                        otp_instance.delete()
                        pending_user.delete()

                        # Giving the user and access and refresh token

                        user_to_login = authenticate(
                            request, email=pending_user.email, password=pending_user.password)
                        login(request, user_to_login)
                        token = RefreshToken.for_user(user=user_to_login)
                        return Response({"access": str(token.access_token),
                                        "refresh": str(token)}, status=status.HTTP_200_OK)
                    else:
                        return Response({'error': 'Invalid user data'}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
