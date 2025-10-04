import SQLalchemy as sa
import SQLalchemy.orm as so
from app import db
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id : so.Mapped[int] = so.mapped_column(primary_key=True)
    username : so.Mapped[str] = so.mapped_column(sa.String(64),unique=True, index=True)
    mail : so.Mapped[str] = so.mapped_column(sa.String(128),unique=True, index=True)
    password_hash : so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

