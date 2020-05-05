from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db


class User(db.Document):
    email = db.StringField(required=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> None:
        return check_password_hash(self.password_hash, password)
