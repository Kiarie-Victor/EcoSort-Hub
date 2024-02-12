from rest_framework import serializers
from Accounts.models  import Member, Otp
import re
import phonenumbers
from django.contrib.auth import login,authenticate,get_user_model


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("email", "username", "phone_number",
                  "password")
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        request = self.context.get('request')

        user = authenticate(request=request, email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid login credentials')

        login(request=request, user=user)

        # assigning user to data dictionary in oder to use it to give the user tokens
        data['user'] = user
        return data


