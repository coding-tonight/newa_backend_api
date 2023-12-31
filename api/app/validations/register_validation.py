from app.models import AuthUser
from app.messages import globalMessage

from app.regexs import ntc_phone_number_regex, ncell_phone_number_regex


def register_validation(request):
    try:
        data = request.data
        error_list = []

        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        profile = data.get('profile')
        phone_number = data.get('phone_number')
        province = data.get('province')
        city = data.get('city')
        distrist = data.get('distrist')

        # validation

        if email and AuthUser.objects.filter(email=email).exists():
            error_list.append({
                'email': [
                    globalMessage.DUPLICATE_ERROR_MESSAGES
                ]
            })

        if password != confirm_password:
            error_list.append({
                'password': [
                    globalMessage.PASSWORD_NOT_MATCH
                ]
            })

        if phone_number:
            if not ncell_phone_number_regex.match(phone_number) or not ntc_phone_number_regex.match(phone_number):
               pass

        return error_list, first_name, last_name, email, password, profile, phone_number, city, distrist, province

    except Exception as exe:
        raise Exception(exe)
