from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """
    Custom authentication backend for email-based authentication.

    This backend allows users to authenticate using their email and password.

    Methods:
        authenticate(request, email=None, password=None, **kwargs): Authenticates a user based on email and password.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Authenticate a user based on email and password.

        Args:
            request: The request object.
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The authenticated user if successful, None otherwise.
        """
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
