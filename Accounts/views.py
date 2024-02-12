from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.tokens import RefreshToken

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
