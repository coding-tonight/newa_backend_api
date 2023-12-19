import logging
from datetime import datetime
from django.contrib.auth import authenticate
from django.db import transaction

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken

from app.messages import globalMessage
from app.validations import login_validation, register_validation
from app.models import AuthUser
from app.email import SendMail


logger = logging.getLogger('django')


class LoginApiView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, format=None):
        try:
            #  check if there is a auth header or not
            if not request.META.get('HTTP_AUTHORIZATION'):
                return Response({
                    globalMessage.MESSAGE: 'Not acceptable'
                }, status=status.HTTP_406_NOT_ACCEPTABLE)

            error_list, email, password = login_validation(request)

            if error_list:
                return Response({
                    globalMessage.MESSAGE: globalMessage.UNAUTHORIZED,
                    'errors': error_list,
                    'status': globalMessage.ERROR_CODE
                }, status=status.HTTP_401_UNAUTHORIZED)

            # authenticate user

            user = authenticate(email=email, password=password)

            if user:
                # if user is valid then generate refresh token
                refresh = RefreshToken()
                user_detail = AuthUser.objects.get(id=user.pk)

                MSG = {
                    globalMessage.MESSAGE: globalMessage.LOGIN_MESSAGE,
                    'refresh_token': refresh,
                    'access_token': refresh.access_token,
                    'data': {
                        'first_name': user_detail.first_name,
                        'last_name': user_detail.last_name,
                        'email': user_detail.email,
                        'phone_number': user_detail.phone_number,
                        'profile': user_detail.profile,
                        'is_superuser': user_detail.is_superuser,
                        'is_staff': user_detail.is_staff,
                        'is_verify': user_detail.is_verify,
                        'is_active': user_detail.is_active
                    },
                    'recevied_at': datetime.now()
                }

                return Response(MSG, status=status.HTTP_200_OK)

            #  if user is not authenticate then
            return Response({
                globalMessage.MESSAGE: globalMessage.UNAUTHORIZED,
                'status': globalMessage.ERROR_CODE
            }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)

            return Response({
                globalMessage.MESSAGE: globalMessage.ERROR_MESSAGE,
                'status': globalMessage.ERROR_CODE
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegisterApiView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, format=None):
        error_list, first_name, last_name, email, password, profile, address, phone_number = register_validation(
            request)

        if error_list:
            return Response({
                globalMessage.MESSAGE: globalMessage.UNAUTHORIZED,
                'errors': error_list
            }, status=status.HTTP_401_UNAUTHORIZED)

        with transaction.atomic():
            sid = transaction.savepoint()
            try:
                user = AuthUser.objects.create_user(email=email, password=password, first_name=first_name,
                                                    last_name=last_name, profile=profile, address=address,
                                                    phone_number=phone_number)

                if user:
                    #  generate token after registeration
                    # SendMail.send_verify_mail()

                    transaction.savepoint_commit(sid)
                    return Response({
                        globalMessage.MESSAGE: globalMessage.REGISTER_MESSAGE,
                        'recevied_at': datetime.now()
                    }, status=status.HTTP_201_CREATED)

            except Exception as exe:
                transaction.savepoint_rollback(sid)
                pass
