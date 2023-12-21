from rest_framework.exceptions import APIException

class BaseException(APIException):
    status_code = None
    detail = None

    def __init__(self, detail, code):
        super().__init__(self, detail, code)
        self.detail = detail
        self.status_code = code
    

    

