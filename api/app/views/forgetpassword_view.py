import logging
# from datetime import datetime 

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status 



logger = logging.getLogger('django')


class ForgetPasswordApiView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, format=None):
        pass