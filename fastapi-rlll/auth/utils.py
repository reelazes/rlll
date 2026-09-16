from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from core.config import settings

ACCESS_TOKEN_TYPE = "access"


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
):
    encoded_jwt = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded_jwt


def decode_jwt(
        token: str,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded

def hash_password(
        password: str,
) -> str:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode()


def validate_password(
        password: str,
        hashed_password: str,
) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def create_access_token(user_id: int, username: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "type": ACCESS_TOKEN_TYPE,
        "sub": str(user_id),
        "username": username,
        "iat": now,
        "exp": now + timedelta(minutes=settings.auth_jwt.access_token_expire_minutes),
    }
    return encode_jwt(payload)