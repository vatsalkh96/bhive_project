from passlib.context import CryptContext
import datetime

hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_hash(data: str) -> str:
    return hash_context.hash(data)

def verify_hash(plain_data: str, hashed_data: str) -> bool:
    return hash_context.verify(plain_data, hashed_data)


def utcnow()->datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)
