from django.shortcuts import render
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from Utils.didYouKnow import didYouKnowMessage
from rest_framework_simplejwt.authentication import JWTAuthentication
from main.models import WasteCategory
from main.serializers import WasteCategorySerializer

# View for fetching environmental tips



class EnvironmentalTipView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        random_fact = didYouKnowMessage()
        if random_fact:
            return Response(random_fact, status=status.HTTP_200_OK)
        return Response({'error': "Couldn't fetch fun facts"}, status=status.HTTP_417_EXPECTATION_FAILED)

# View for handling WasteCategory operations


class WasteCategoryView(APIView):
    # Get all waste categories
    def get(self, request):
        waste_categories = WasteCategory.objects.all()
        serializer = WasteCategorySerializer(waste_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Create a new waste category
    def post(self, request):
        serializer = WasteCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
