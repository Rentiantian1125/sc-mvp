import jwt


class token_service:
    TOKEN_SECRET = 'sc-mvp'
    TOKEN_ENCRYPTION_METHOD = 'HS256'

    @staticmethod
    def get_token(request):
        if not request.META.get('HTTP_AUTH'):
            return False
        else:
            return request.META.get('HTTP_AUTH')

    @staticmethod
    def create_token(payload):
        return str(jwt.encode(payload, token_service.TOKEN_SECRET, token_service.TOKEN_ENCRYPTION_METHOD),
                   encoding="utf8")

    @staticmethod
    def check_token(token):
        return jwt.decode(token, token_service.TOKEN_SECRET, token_service.TOKEN_ENCRYPTION_METHOD)
