from fastapi import APIRouter, Request
from fastapi_users import FastAPIUsers
from .models import User, UserCreate, UserUpdate, UserDB, user_db
from .auth import auth_backends, jwt_authentication, SECRET

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


def on_after_register(user: UserDB, request: Request):
    # TODO: send welcome email here
    print(f"User {user.id} has registered.")


user_router.include_router(
    fastapi_users.get_register_router(on_after_register),
    prefix="/auth",
    tags=["auth"],
)


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    # TODO: send forgot password mail
    print(f"User {user.id} has forgot their password. Reset token: {token}")


def on_after_reset_password(user: UserDB, request: Request):
    #TODO: Send mail
    print(f"User {user.id} has reset their password.")


user_router.include_router(
    fastapi_users.get_reset_password_router(
        SECRET, after_forgot_password=on_after_forgot_password, after_reset_password=on_after_reset_password),
    prefix="/auth",
    tags=["auth"],
)

user_router.include_router(
    fastapi_users.get_users_router(requires_verification=True),
    prefix="/users",
    tags=["users"],
)


user_router.include_router(
    fastapi_users.get_verify_router(SECRET),
    prefix="/auth",
    tags=["auth"],
)