from itsdangerous import URLSafeTimedSerializer
import os


class Security:
    def __init__(self):
        pass

    @staticmethod
    def generate_confirmation_token(email):
        serializer = URLSafeTimedSerializer(os.environ['S_KEY'])
        return serializer.dumps(email, salt=os.environ['SECURITY_PASSWORD_SALT'])

    @staticmethod
    def confirm_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(os.environ['S_KEY'])
        try:
            email = serializer.loads(
                token,
                salt=os.environ['SECURITY_PASSWORD_SALT'],
                max_age=expiration
            )
        except:
            return False
        return email