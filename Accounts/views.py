from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

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
                    # otp_code = otp_generator.otp_generator()

                    otp_instance = Otp.objects.create(otp_code=otp_code)
                    otp_instance.save()
                    # response = email_sender.sendEmail(
                        # username=username, otp_code=otp_code, email=email)
                    if response:
                        # handling save PendingUserData
                        pending_user = PendingUserModel.objects.create(
                            user_otp=otp_code, username=username, email=email, phone_number=phone_number, password=password, date_of_birth=date_of_birth)
                        pending_user.save()
                        return Response({'Detail': 'Otp code sent successfully'}, status=status.HTTP_200_OK)

                    raise Exception('Error encountered when sending Email')

                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
