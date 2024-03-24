from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from Utils.didYouKnow import didYouKnowMessage
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

class EnvironmentalTipView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        random_fact = didYouKnowMessage()
        if random_fact:
            return Response(random_fact, status=status.HTTP_200_OK)
        return Response({'error':'"couldn\'t fetch fun facts'}, status=status.HTTP_417_EXPECTATION_FAILED)
