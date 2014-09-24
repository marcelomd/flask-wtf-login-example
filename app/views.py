# coding: utf-8

from flask import Blueprint, g, render_template, request
from flask.ext.login import current_user, login_required, login_user, \
        logout_user, redirect, url_for
from .forms import LoginForm, RegisterForm
from .models import User
from . import db


main = Blueprint('main', __name__)


@main.before_request
def before_request():
    g.user = current_user


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/home')
@login_required
def home():
    return render_template('home.html')


@main.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            redirect_url = request.args.get('next') or url_for('main.login')
            return redirect(redirect_url)
    return render_template('login.html', form=form)


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User(email=form.email.data,
                username=form.username.data,
                password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)
