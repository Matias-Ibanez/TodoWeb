from flask import render_template, request, redirect, url_for, abort, flash
from flask import Blueprint

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('base.html')