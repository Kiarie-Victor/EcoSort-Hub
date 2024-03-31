from django.core.mail import EmailMessage
from decouple import config


def sendEmail(username, otp_code, email) -> bool:
    # Set the email receiver, subject, sender, and message content
    receiver = email
    subject = f'Otp Verification {otp_code}'
    sender = config('EMAIL_HOST_USER')
    message = f"Dear {username}, \n Your code is: {otp_code}. \n Use it to access your account. If you didn't request this, simply ignore this message.\n Yours, \n Anonymous"

    try:
        # Create an EmailMessage object with the specified details
        email = EmailMessage(subject=subject, body=message,
                             from_email=sender, to=[receiver])

        # Send the email
        email.send(fail_silently=False)

        # Return True to indicate successful email sending
        return True

    except Exception as e:
        # Return False if an exception occurs during email sending
        return False
