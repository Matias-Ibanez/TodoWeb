from app.extensions import db, login
from app.main.models import User

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))