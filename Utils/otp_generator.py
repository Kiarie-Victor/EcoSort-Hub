import random
from Accounts.models import Otp
def otp_generate():
    length = 6
    otp = ''
    while True:
        otp = ''.join([str(random.randint(0,9)) for _ in range(length)])
        
        if Otp.objects.filter(otp_code=otp).exists():
            continue
        else:
            break
    return otp