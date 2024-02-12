from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import phonenumbers
from Utils.uuid_field import UUIDGenerator
# Create your models here.
class MemberManager(BaseUserManager):
    def create_user(self, email, username, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The email field cannot be empty')

        email = self.normalize_email(email)
        try:
            parsed_number = phonenumbers.parse(phone_number, 'KE')
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError('The phone number is not valid')
            else:
                phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

        except phonenumbers.NumberParseException:
            raise ValueError('The phone number is not valid')

        user = self.model(email=email, username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, username, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, phone_number, password, **extra_fields)

class Member(AbstractBaseUser, PermissionsMixin, UUIDGenerator, models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    def __str__(self):
        return self.username


class Otp(models.Model):
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

class PendingUserModel(models.Model):
    user_otp = models.CharField(max_length=6)
    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=20)