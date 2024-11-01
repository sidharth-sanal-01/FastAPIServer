from passlib.context import CryptContext

# for hashing the password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verifyPassword(plainPassword, hashedPassword):
    return pwd_context.verify(hashedPassword, plainPassword)
