from fastapi import APIRouter, Request, status, Body
from fastapi.exceptions import HTTPException
from fastapi_users import FastAPIUsers
from fastapi_users.router.common import ErrorCode
from fastapi_users.user import UserAlreadyVerified, UserNotExists
from pydantic import EmailStr

from .auth import SECRET, auth_backends, jwt_authentication
from .models import User, UserCreate, UserDB, UserUpdate, user_db
from .utils.helpers import generate_token
from .utils.mailer import send_token

fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

user_router = APIRouter()

user_router.include_router(
    fastapi_users.get_auth_router(
        jwt_authentication, requires_verification=True),
    prefix="/auth/jwt",
    tags=["auth"],
)


async def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has registered.")


# user registeration router
user_router.include_router(
    fastapi_users.get_register_router(on_after_register),
    prefix="/auth",
    tags=["auth"],
)


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    # TODO: send forgot password mail
    print(f"User {user.id} has forgot their password. Reset token: {token}")


# password reset router
user_router.include_router(
    fastapi_users.get_reset_password_router(
        SECRET, after_forgot_password=on_after_forgot_password),
    prefix="/auth",
    tags=["auth"],
)

# user profile router
user_router.include_router(
    fastapi_users.get_users_router(requires_verification=True),
    prefix="/users",
    tags=["users"],
)


@user_router.post('/auth/request-verify-token', status_code=status.HTTP_202_ACCEPTED)
async def request_verify_token(request: Request, email: EmailStr = Body(..., embed=True)):
    try:
        user = await fastapi_users.get_user(email)
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.VERIFY_USER_ALREADY_VERIFIED,
            )
        elif user.is_active:
            token = generate_token(email)
            await send_token(email, token)
    except UserNotExists:
        pass
    return None

@user_router.post('/verify', response_model=User)
async def verify(request: Request, token: str = Body(..., embed=True), email: str = Body(..., embed=True)):
    token_is_valid = token==generate_token(email)
    try:
        user = await fastapi_users.get_user(email)
        if user.is_verified:
            return user
        elif token_is_valid:
            verified_user = await fastapi_users.verify_user(user)
            return verified_user
        elif not token_is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.VERIFY_USER_BAD_TOKEN,
            )
    except UserNotExists:
        # return default exception for UserNotExists for security purpose
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.VERIFY_USER_BAD_TOKEN,
        )
