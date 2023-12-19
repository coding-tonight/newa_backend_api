import base64

from app.models import AuthUser
from app.messages import globalMessage


def login_validation(request):
    try:
        encoded_data = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]

        decoded_data = base64.b64decode(
            encoded_data).decode('utf-8').split(':')

        email = decoded_data[0]
        password = decoded_data[1]
        error_list = []
        
        #  validation
        if not email:
            error_list.append({
                'email': [
                    globalMessage.NULL_ERROR_MESSAGES
                ]
            })

        if not password:
            error_list.append({
                'password': [
                    globalMessage.NULL_ERROR_MESSAGES
                ]
            })

        return error_list, email, password

    except Exception as exe:
        raise Exception(exe)
