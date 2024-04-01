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
        """
        Method to validate user login credentials.

        Args:
            data (dict): Login credentials.

        Returns:
            dict: Validated login credentials along with authenticated user.
        Raises:
            serializers.ValidationError: If the provided credentials are invalid.
        """
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


class PendingDataSerializer(serializers.Serializer, ValidationMixin):
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

