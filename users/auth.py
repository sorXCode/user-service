import os

from fastapi_users.authentication import JWTAuthentication

SECRET = os.environ["SECRET"]

jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600)

auth_backends = [jwt_authentication]
