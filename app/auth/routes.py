from flask import render_template, request, redirect, url_for, abort, flash
from flask import Blueprint
from app.extensions import db
from app.auth.forms import LoginForm, RegistrationForm
from app.main.models import User
import sqlalchemy as sa
from flask_login import current_user, login_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('views.index'))
    return render_template('login.html', title='Login', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, mail=form.mail.data)
        user.set_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
    return render_template('register.html',title = 'Register', form=form)