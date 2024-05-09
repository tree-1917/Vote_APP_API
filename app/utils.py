# === Hashing Password 
from passlib.context import CryptContext 

#  Hashing User Password  #
pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')


# Hash helper # 
def _hash(password: str) : 
    return pwd_context.hash(password)

# _verify helper # 
def _verify(plain_password, hashed_password) : 
    return pwd_context.verify(plain_password, hashed_password)
