# import re
# from urllib.parse import urlparse
# from sqlalchemy.orm import validates

# def is_valid_url(value: str) -> bool:
#     try:
#         result = urlparse(value)
#         return all([result.scheme, result.netloc])
#     except Exception:
#         return False

# def is_valid_tax_id(value: str) -> bool:
#     # Example: Basic check for 9-digit EIN/TaxID
#     return bool(re.fullmatch(r"\d{2}-\d{7}", value) or re.fullmatch(r"\d{9}", value))

# def is_valid_company_name(value: str) -> bool:
#     return bool(value.strip())

# def is_valid_naics(value: str) -> bool:
#     return bool(re.fullmatch(r"\d{6}", value))

# import re

# def is_valid_zipcode(value: str) -> bool:
#     """Validate US ZIP code (5-digit or ZIP+4)."""
#     return bool(re.match(r"^\d{5}(-\d{4})?$", value))

# def is_valid_state(value: str) -> bool:
#     """Basic validation to check state is alphabetic and reasonable length."""
#     return bool(value and value.isalpha() and 2 <= len(value) <= 100)

# def is_valid_country(value: str) -> bool:
#     """Basic country validation."""
#     return bool(value and value.isalpha() and 2 <= len(value) <= 100)


# def is_valid_email(email: str) -> bool:
#     return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email.strip()))

# def is_valid_phone(phone: str) -> bool:
#     return bool(re.match(r"^\+?\d{7,15}$", phone.strip()))


# def is_valid_hostname_or_ip(value: str) -> bool:
#     ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
#     hostname_pattern = r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$"
#     return bool(re.match(ip_pattern, value) or re.match(hostname_pattern, value))

# def is_valid_port(port: int) -> bool:
#     return 1 <= port <= 65535

# from urllib.parse import urlparse

# def is_valid_url(value: str) -> bool:
#     try:
#         result = urlparse(value)
#         return all([result.scheme in ("http", "https"), result.netloc])
#     except Exception:
#         return False
# import ipaddress

# def is_valid_ip(ip: str) -> bool:
#     try:
#         ipaddress.ip_address(ip.strip())
#         return True
#     except ValueError:
#         return False


# from datetime import datetime, timedelta
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import Session
# from database import get_db
# from models import *

# # === CONFIG ===
# SECRET_KEY = "your_super_secret_key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60

# # === SCHEMES ===
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # === UTILS ===
# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# class HashPassword:
#     def hash(self, password: str) -> str:
#         return pwd_context.hash(password)

# hash_password = HashPassword()

# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)




# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def get_user_by_username(db: Session, username: str):
#     return db.query(User).filter(User.username == username).first()

# def authenticate_user(db: Session, username: str, password: str):
#     user = get_user_by_username(db, username)
#     if not user or not verify_password(password, user.password):
#         return None
#     return user

# def has_permission(user: User, permission_name: str) -> bool:
#     """Check if the user's role includes the given permission."""
#     if not user.role or not user.role.role_permissions:
#         return False
#     return any(
#         rp.permission and rp.permission.name == permission_name
#         for rp in user.role.role_permissions
#         if rp.permission.is_active
#     )


# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     user = get_user_by_username(db, username)
#     if user is None:
#         raise credentials_exception
#     return user
