import random
def otp_generate():
    length = 6
    otp = ''
    while True:
        otp = ''.join([str(random.randint(0,9)) for _ in range(length)])
    return otp