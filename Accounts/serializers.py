from rest_framework import serializers
from Accounts.models  import Member, Otp
import re
import phonenumbers
from django.contrib.auth import login,authenticate,get_user_model


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("email", "username", "phone_number", "location",
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


class PendingDataSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    location = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, username: str):
        if not username.strip():
            raise serializers.ValidationError('Username cannot be empty.')

        # checking if there already exists a user with the username.
        if Member.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'This username is already taken.')

        return username

    def validate_location(self, location:str):
        if not location.strip():
            raise serializers.ValidationError('Must provide location')

        return location

    def validate_email(self, email):
        if not email.strip():
            raise serializers.ValidationError('Email cannot be empty.')

        # regular expression for a normal email
        reg_ex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$'
        if not re.match(reg_ex, email):
            raise serializers.ValidationError('Invalid Email format.')

        # checking if a user with the email input already exists.
        if Member.objects.filter(email=email).exists():
            raise serializers.ValidationError('The email is already taken.')

        return email

    def validate_phone_number(self, phone_number):
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

    def validate_password(self, password):
        if not password.strip():
            raise serializers.ValidationError('Password cannot be empty')

        # checking if the password contains at least 1 uppercase Character
        if not any(char.isupper() for char in password):
            raise serializers.ValidationError(
                'Password must contain at least one uppercase letter')

        # checking if the password contains at least one digit
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError(
                'Password must contain at least one digit.')

        # password must have at least 8 characters.
        if (len(password) < 8):
            raise serializers.ValidationError(
                "Password must not be less than 8 digits.")

        # password must contain at least one of the special characters
        if not any((char in "!@#$%^&*()-_=+[]|;:'\",.<>?/") for char in password):
            raise serializers.ValidationError(
                "Password must contain at least one of the following special characters: !@#$%^&*()-_=+[]|;:'\",.<>?/")

        return password
