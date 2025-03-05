from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
import phonenumbers
from Utils.uuid_field import UUIDGenerator


class MemberManager(BaseUserManager):
    """
    Custom manager for the Member model.

    This manager provides methods for creating regular users and superusers.

    Attributes:
        None
    """

    def create_user(self, email, username, phone_number, location, password=None, **extra_fields):
        """
        Method to create a regular user.

        Args:
            email (str): The user's email.
            username (str): The user's username.
            phone_number (str): The user's phone number.
            location (str): The user's location.
            password (str): The user's password.
            **extra_fields: Additional fields to be saved for the user.

        Returns:
            Member: The created user object.

        Raises:
            ValueError: If email or phone number is not provided or if phone number is invalid.
        """
        if not email:
            raise ValueError('The email field cannot be empty')

        email = self.normalize_email(email)
        try:
            parsed_number = phonenumbers.parse(phone_number, 'KE')
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError('The phone number is not valid')
            else:
                phone_number = phonenumbers.format_number(
                    parsed_number, phonenumbers.PhoneNumberFormat.E164)

        except phonenumbers.NumberParseException:
            raise ValueError('The phone number is not valid')

        user = self.model(email=email, username=username,
                          phone_number=phone_number, location=location, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone_number, location, password=None, **extra_fields):
        """
        Method to create a superuser.

        Args:
            email (str): The user's email.
            username (str): The user's username.
            phone_number (str): The user's phone number.
            location (str): The user's location.
            password (str): The user's password.
            **extra_fields: Additional fields to be saved for the user.

        Returns:
            Member: The created superuser object.

        Raises:
            ValueError: If email or phone number is not provided or if phone number is invalid.
        """
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, phone_number, location, password=password, **extra_fields)


class Member(AbstractBaseUser, PermissionsMixin, UUIDGenerator, models.Model):
    """
    Custom user model representing a member.

    This model extends the AbstractBaseUser and PermissionsMixin provided by Django.

    Attributes:
        email (str): User's email.
        username (str): User's username.
        phone_number (str): User's phone number.
        location (str): User's location.
        password (str): User's password.
        groups (ManyToManyField): User's assigned groups.
        user_permissions (ManyToManyField): User's assigned permissions.
        is_active (bool): Indicates if the user is active.
        is_staff (bool): Indicates if the user is staff.
        objects (MemberManager): Manager for the Member model.
        USERNAME_FIELD (str): Field used for authentication (email).
        REQUIRED_FIELDS (list): Fields required for creating a user (username, phone_number).
    """

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    location = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    # groups = models.ManyToManyField(Group, related_name='member_group')
    # user_permissions = models.ManyToManyField(
    #     Permission, related_name='member_user_permissions')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number', 'location',]

    def __str__(self):
        """
        Method to return string representation of the user.

        Returns:
            str: Username of the user.
        """
        return self.username


class Otp(models.Model):
    """
    Model to store OTP codes.

    Attributes:
        otp_code (str): The OTP code.
        created_at (datetime): The date and time when the OTP was created.
        is_verified (bool): Indicates if the OTP has been verified.
    """

    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.otp_code


class PendingUserModel(models.Model):
    """
    Model to store pending user data.

    Attributes:
        user_otp (str): The OTP associated with the user.
        username (str): The username of the pending user.
        email (str): The email of the pending user (unique).
        phone_number (str): The phone number of the pending user.
        location (str): The location of the pending user.
        password (str): The password of the pending user.
    """

    user_otp = models.CharField(max_length=6)
    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username
    
