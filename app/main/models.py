from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.extensions import db
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id : so.Mapped[int] = so.mapped_column(primary_key=True)
    username : so.Mapped[str] = so.mapped_column(sa.String(64),unique=True, index=True)
    mail : so.Mapped[str] = so.mapped_column(sa.String(128),unique=True, index=True)
    password_hash : so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    id : so.Mapped[int] = so.mapped_column(primary_key=True, index=True)
    user_id : so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
    title : so.Mapped[str] = so.mapped_column(sa.String(128))
    description : so.Mapped[str] = so.mapped_column(sa.String(256))
    completed : so.Mapped[bool] = so.mapped_column(sa.Boolean)
    created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))

