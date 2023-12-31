import logging
from datetime import datetime

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from app.models import Otp, AuthUser
from app.validations import is_expiry, verify_email
from app.messages import globalMessage


logger = logging.getLogger('django')


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, format=None):
        try:
            if not request.data:
                return Response({
                    globalMessage.MESSAGE: globalMessage.ERROR_MESSAGE
                }, status=status.HTTP_400_BAD_REQUEST)

            error_list, otp = verify_email(request)

            if not error_list:
                user_id = Otp.objects.get(otp=otp)

                expiry = is_expiry(user_id.created)

                if not expiry:
                    user = AuthUser.objects.get(id=user_id.user.id)
                    user.is_verify = True
                    user.save()
                    # user_id.delete()

                    MSG = {
                        globalMessage.MESSAGE: globalMessage.SUCCESS_MESSAGE,
                        'status': globalMessage.SUCCESS_CODE
                    }
                    return Response(MSG, status=status.HTTP_200_OK)

            return Response({
                globalMessage.MESSAGE: globalMessage.UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as exe:
            logger.error(str(exe), exc_info=True)

            return Response({
                globalMessage.MESSAGE: globalMessage.ERROR_MESSAGE,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # finally:
        #     # delete the otp
        #     Otp.objects.get(otp=otp).delete()
