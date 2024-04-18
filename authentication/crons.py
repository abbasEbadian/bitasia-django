from authentication.models import OTP


def check_otp_expiration():
    instances = OTP.objects.filter(expired=False, consumed=False)
    for i in range(5):
        print(i)
    for otp in instances:
        print(otp.has_expired() and not otp.expired)
        print("CAE")
        if otp.has_expired() and not otp.expired:
            otp.expire()
