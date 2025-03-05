from rest_framework import serializers
from Accounts.models import Member, Otp
import re
import phonenumbers
from django.contrib.auth import login, authenticate, get_user_model
from Utils.validation_mixin import ValidationMixin

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer handles the creation of new Member instances.

    Attributes:
        model (class): The Member model.
        fields (tuple): Fields to include in the serialized representation.
    """

    class Meta:
        model = Member
        fields = ("email", "username", "phone_number", "location", "password")

    def create(self, validated_data):
        """
        Method to create a new Member instance.

        Args:
            validated_data (dict): Validated data for the new Member instance.

        Returns:
            Member: The newly created Member instance.
        """
        print(validated_data)
        user = get_user_model().objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    This serializer validates user login credentials and authenticates users.

    Attributes:
        email (str): User email.
        password (str): User password.
    """

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

        # Assigning user to data dictionary in order to use it to give the user tokens
        data['user'] = user
        return data


class PendingDataSerializer(serializers.Serializer):
    """
    Serializer for pending user registration data.

    This serializer validates and processes the data submitted for user registration.

    Attributes:
        username (str): User's username.
        email (str): User's email.
        phone_number (str): User's phone number.
        location (str): User's location.
        password (str): User's password.
    """

    username = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    location = serializers.CharField()
    password = serializers.CharField()


class MemberSerializer(serializers.Serializer, ValidationMixin):
    username = serializers.CharField()
    phone_number = serializers.CharField()
    location = serializers.CharField()
    email = serializers.CharField()

class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ['otp_code']

class ProfileUpdateSerializer(serializers.Serializer):
    username = serializers.CharField()
    location = serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data): 
        username = data.get['username']
        location = data.get['location']
        password = data.get['password']
        request = self.context.get['request']

        user_email = request.email

        user = Member.objects.get(email=user_email)
        if Member.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username taken.")
        else:
            user.username = username
        if Member.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError("Cannot update number. ")

