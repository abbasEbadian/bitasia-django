from authentication.models import OTP


def check_otp_expiration():
    instances = OTP.objects.filter(expired=False, consumed=False)

    for otp in instances:
        if otp.has_expired() and not otp.expired:
            otp.expire()
