from flask import render_template, request, redirect, url_for, abort, flash
from flask import Blueprint
from flask_login import current_user, login_user,logout_user, login_required

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def index():
    return render_template('index.html')