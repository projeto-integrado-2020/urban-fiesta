from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .extensions import db


class User(UserMixin, db.Document):
    email = db.EmailField(required=True, unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    password_hash = db.StringField(max_length=128)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
