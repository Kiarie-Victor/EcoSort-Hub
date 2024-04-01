from rest_framework.views import APIView
from main.serializers import MemberSerializer
from main.models import Member
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle,SimpleRateThrottle
from Accounts.models import PendingUserModel, Member, Otp
from Accounts.serializers import LoginSerializer, PendingDataSerializer, RegistrationSerializer, MemberSerializer
from django.db import transaction
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# LoginView handles user login and token assignment after successful login


class LoginView(APIView):
    def post(self, request):
        # Initialize login serializer
        serializer = LoginSerializer(
            data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data.get('user')
            if user is None:
                # If user is not found, return Unauthorized response
                return Response({'detail': 'Invalid login credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

            # Generate Refresh Token for the user
            refresh = RefreshToken.for_user(user=user)

            # Return response with Access and Refresh tokens
            return Response({'access_token': str(refresh.access_token),
                             'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            # Handle validation error
            return Response({"errors": str(e)})


# RegistrationView handles user registration process
class RegistrationView(APIView):
    throttle_classes = [AnonRateThrottle, SimpleRateThrottle]

    def post(self, request):
        # Initialize serializer with request data
        serializer = PendingDataSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                try:
                    # Extract data from the request
                    email = serializer.validated_data['email']
                    username = serializer.validated_data['username']
                    phone_number = serializer.validated_data['phone_number']
                    password = serializer.validated_data['password']

                    # Generate OTP
                    otp_code = otp_generator.otp_generate()

                    # Create OTP instance and save
                    otp_instance = Otp.objects.create(otp_code=otp_code)
                    otp_instance.save()

                    # Send email with OTP
                    response = email_sender.sendEmail(
                        username=username, otp_code=otp_code, email=email)
                    if response:
                        # Create PendingUserModel instance and save
                        pending_user = PendingUserModel.objects.create(
                            user_otp=otp_code, username=username, email=email, phone_number=phone_number, password=password)
                        pending_user.save()
                        # Return success response
                        return Response({'Detail': 'Otp code sent successfully'}, status=status.HTTP_200_OK)

                    # Raise exception if error encountered when sending email
                    raise Exception('Error encountered when sending Email')

                except Exception as e:
                    # Handle exception
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # If serializer is not valid, return serializer errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# OtpVerification handles OTP verification and user registration process


class OtpVerification(APIView):
    def post(self, request):
        # Initialize serializer with request data
        serializer = OtpSerializer(data=request.data)

        if serializer.is_valid():
            otp_code = serializer.validated_data['otp_code']
            try:
                # Ensure all database operations are atomic
                with transaction.atomic():
                    try:
                        # Get OTP instance by code
                        otp_instance = Otp.objects.get(otp_code=otp_code)
                    except Otp.DoesNotExist:
                        # Return error response if OTP code is invalid
                        return Response({'error': 'Invalid OTP code.'}, status=status.HTTP_400_BAD_REQUEST)

                    if otp_expired.otp_expired(otp_timestamp=otp_instance.created_at):
                        # Delete expired OTP instance and return error response
                        otp_instance.delete()
                        return Response({'error': "Otp Expired"}, status=status.HTTP_400_BAD_REQUEST)

                    try:
                        # Get pending user by OTP code
                        pending_user = PendingUserModel.objects.get(
                            user_otp=otp_code)
                    except PendingUserModel.DoesNotExist:
                        # Return error response if pending user not found
                        return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

                    # Prepare data for user registration
                    data = {
                        "username": pending_user.username,
                        "email": pending_user.email,
                        "phone_number": pending_user.phone_number,
                        "password": pending_user.password,
                        "location": pending_user.location
                    }

                    # Serialize and validate user registration data
                    user_serializer = RegistrationSerializer(data=data)
                    if user_serializer.is_valid():
                        # Save user data
                        user_serializer.save()
                        # Delete OTP and pending user instances
                        otp_instance.delete()
                        pending_user.delete()

                        # Authenticate and login user
                        user_to_login = authenticate(
                            request, email=pending_user.email, password=pending_user.password)
                        login(request, user_to_login)
                        # Generate access and refresh tokens
                        token = RefreshToken.for_user(user=user_to_login)
                        # Return success response with tokens
                        return Response({"access": str(token.access_token), "refresh": str(token)}, status=status.HTTP_200_OK)
                    else:
                        # Return error response if user data is invalid
                        return Response({'error': 'Invalid user data'}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                # Return error response if any internal server error occurs
                return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Return serializer errors if validation fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    # Throttling to limit the number of requests
    throttle_classes = [UserRateThrottle, SimpleRateThrottle]
    # Permission class for authentication
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve user information and serialize it
        user = request.user
        serializer = MemberSerializer(instance=user)

        # Return user data in the response
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Deserialize and validate user data
        serializer = MemberSerializer(data=request.data)

        if serializer.is_valid():
            # Extract validated data
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            phone_number = serializer.validated_data['phone_number']
            location = serializer.validated_data['location']

            try:
                # Update user profile if user exists
                user = Member.objects.get(username=username, email=email)
                user.email = email
                user.location = location
                user.username = username
                user.phone_number = phone_number
                user.save()

                # Return success message if profile is updated
                return Response({'status': 'Details Updated'}, status=status.HTTP_200_OK)

            except Member.DoesNotExist:
                # Return error message if user does not exist
                return Response({'status': 'Failed To update Info'}, status=status.HTTP_400_BAD_REQUEST)

        # Return validation errors if serializer is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteProfile(APIView):
    authentication_classes = [JWTAuthentication]
    # Throttling for rate limiting
    throttle_classes = [SimpleRateThrottle, UserRateThrottle]
    # Permission class for authentication
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Retrieve authenticated user
        user = request.user

        # Retrieve and delete user object
        user_object = Member.objects.get(username=request.user.username)
        user_object.delete()

        # Return success message after deleting profile
        return Response({'Status': 'Profile deleted successfully'}, status=status.HTTP_200_OK)
