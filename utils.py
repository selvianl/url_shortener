import secrets

from database import SessionLocal
from config import CHARS
from models import URL


def is_key_exists(db: SessionLocal, key) -> bool:
    record = db.query(URL).filter(
        URL.key == key, URL.is_active
    ).first()
    return True if record else False


def generate_unique_key(db, length: int = 5) -> str:
    key = "".join(secrets.choice(CHARS) for _ in range(length))
    while is_key_exists(db, key):
        generate_unique_key(db)
    return key
