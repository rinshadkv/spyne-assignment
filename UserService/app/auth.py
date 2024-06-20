import logging
from datetime import datetime, timedelta

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import User

# JWT configs
SECRET_KEY = "dsfdfdfder4wewedesfdefefrgrt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3600

# Logging setup
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Security related functions
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "sub": str(data["user_id"])})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        logger.debug("Decoding JWT token")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"Token payload: {payload}")
        user_id = payload.get("sub")

        if user_id is None:
            logger.debug("User ID is None in token payload")
            raise credentials_exception

        user_id_int = int(user_id) if user_id.isdigit() else user_id
    except (JWTError, ValueError) as e:
        logger.debug(f"Error decoding token or converting user_id: {e}")
        raise credentials_exception

    logger.debug(f"Fetching user with ID: {user_id_int}")
    user = get_user(db, user_id_int)
    if user is None:
        logger.debug("User not found in the database")
        raise credentials_exception
    logger.debug("User authenticated successfully")
    return user
