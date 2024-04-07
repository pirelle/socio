from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encrypt_password_strat(password):
    return pwd_context.hash(password)


def verify_password_strat(password, hashed):
    return pwd_context.verify(password, hashed)
