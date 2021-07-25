from turtledemo.chaos import g

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from auth.models import User
from config.database import db_session
from config.settings import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'error')
        return redirect(url_for('login'))

    login_user(user, remember=remember)
    g.user = current_user
    fallback = url_for('admin.index')
    dest = request.args.get('next')
    try:
        dest_url = url_for(dest)
        return redirect(dest_url)
    except:
        return redirect(fallback)



@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('name')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    if password2 != password1:
        flash('The two password fields does not match')
        return redirect(url_for('signup'))

    if User.query.filter_by(email=email).first():
        flash('Email address already exists')
        return redirect(url_for('signup'))

    if User.query.filter_by(username=username).first():
        flash('username address already exists')
        return redirect(url_for('signup'))
    new_user = User(email=email, username=username,
                    password=generate_password_hash(password1, method='sha256'))

    db_session.add(new_user)
    db_session.commit()
    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))