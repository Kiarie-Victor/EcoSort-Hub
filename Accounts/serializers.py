from rest_framework import serializers
from Accounts.models import Member, Otp
import re
import phonenumbers
from django.contrib.auth import login, authenticate, get_user_model


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

    def validate_username(self, username: str):
        """
        Method to validate the username.

        Args:
            username (str): The username to validate.

        Returns:
            str: The validated username.
        Raises:
            serializers.ValidationError: If the username is empty or already taken.
        """
        if not username.strip():
            raise serializers.ValidationError('Username cannot be empty.')

        if Member.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'This username is already taken.')

        return username

    def validate_location(self, location: str):
        """
        Method to validate the location.

        Args:
            location (str): The location to validate.

        Returns:
            str: The validated location.
        Raises:
            serializers.ValidationError: If the location is empty.
        """
        if not location.strip():
            raise serializers.ValidationError('Must provide location')

        return location

    def validate_email(self, email: str):
        """
        Method to validate the email.

        Args:
            email (str): The email to validate.

        Returns:
            str: The validated email.
        Raises:
            serializers.ValidationError: If the email is empty, invalid, or already taken.
        """
        if not email.strip():
            raise serializers.ValidationError('Email cannot be empty.')

        reg_ex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$'
        if not re.match(reg_ex, email):
            raise serializers.ValidationError('Invalid Email format.')

        if Member.objects.filter(email=email).exists():
            raise serializers.ValidationError('The email is already taken.')

        return email

    def validate_phone_number(self, phone_number: str):
        """
        Method to validate the phone number.

        Args:
            phone_number (str): The phone number to validate.

        Returns:
            str: The validated phone number.
        Raises:
            serializers.ValidationError: If the phone number is empty or invalid.
        """
        if not phone_number.strip():
            raise serializers.ValidationError(
                'Phone Number field cannot be empty')
        try:
            parsed_number = phonenumbers.parse(phone_number, region='KE')
            if not phonenumbers.is_valid_number(parsed_number):
                raise serializers.ValidationError(
                    'Invalid phone number format')
            else:
                phone_number = phonenumbers.format_number(
                    parsed_number, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError('Invalid phone number format')

        return phone_number

    def validate_password(self, password: str):
        """
        Method to validate the password.

        Args:
            password (str): The password to validate.

        Returns:
            str: The validated password.
        Raises:
            serializers.ValidationError: If the password is empty or does not meet requirements.
        """
        if not password.strip():
            raise serializers.ValidationError('Password cannot be empty')

        if not any(char.isupper() for char in password):
            raise serializers.ValidationError(
                'Password must contain at least one uppercase letter')

        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError(
                'Password must contain at least one digit.')

        if len(password) < 8:
            raise serializers.ValidationError(
                "Password must not be less than 8 digits.")

        if not any((char in "!@#$%^&*()-_=+[]|;:'\",.<>?/") for char in password):
            raise serializers.ValidationError(
                "Password must contain at least one of the following special characters: !@#$%^&*()-_=+[]|;:'\",.<>?/")

        return password
