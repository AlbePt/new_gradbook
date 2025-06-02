from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Хеширует пароль для хранения в БД.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Сравнивает сырой пароль с хранимым хешем.
    """
    return pwd_context.verify(plain_password, hashed_password)
