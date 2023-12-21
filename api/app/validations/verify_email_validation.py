from app.models import Otp
from app.messages import globalMessage


def verify_email(request):
    try:
        if not request.data:
            pass

        data = request.data
        otp = data.get('otp')
        error_list = []

        if otp and not Otp.objects.filter(otp=otp).exists():
            error_list.append({
                'otp': [
                    globalMessage.NOT_MATCH
                ]
            })

        return error_list, otp

    except Exception as exe:
        raise Exception(exe)
