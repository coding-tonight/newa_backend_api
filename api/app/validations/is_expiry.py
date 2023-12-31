from datetime import datetime

from django.conf import settings

from app.models import Otp


#  check if the otp is expiry or not

def is_expiry(created):
    diff_in_sec = created - datetime.now().strftime('H%:%M:%S')

    diff = diff_in_sec / 60

    if diff > settings.OTP_LIFE_TIME:
        return True
    # Otp.objects.get()
    return False
