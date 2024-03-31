from django.utils import timezone


def otp_expired(otp_timestamp: timezone):
    # Calculate the expiration time by adding 3 minutes to the OTP timestamp
    expire_time = otp_timestamp + timezone.timedelta(minutes=3)

    # Check if the expiration time is earlier than the current time
    if expire_time < timezone.now():
        # If the expiration time has passed, return True to indicate OTP has expired
        return True

    # If the expiration time has not passed, return False to indicate OTP is still valid
    return False
