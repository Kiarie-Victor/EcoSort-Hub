import random
from Accounts.models import Otp


def otp_generate():
    # Define the length of the OTP
    length = 6

    # Initialize an empty string to store the OTP
    otp = ''

    # Loop until a unique OTP is generated
    while True:
        # Generate a random OTP string of specified length
        otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])

        # Check if the generated OTP already exists in the database
        if Otp.objects.filter(otp_code=otp).exists():
            # If the OTP already exists, generate a new one
            continue
        else:
            # If the OTP is unique, break out of the loop
            break

    # Return the unique OTP
    return otp
