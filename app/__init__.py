from flask import Flask
from app.main.views import views as view_bp
from app.auth.routes import auth as auth_bp
from app.extensions import db,migrate, login
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    app.register_blueprint(view_bp)
    app.register_blueprint(auth_bp)


    return app