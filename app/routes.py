from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import Loginform, Registrationform
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'Maria'}, 'post': 'Awesome pics took in Poland'
        },
        {
            'author': {'username': 'Tom'}, 'post': 'Beautiful dinner in Norway'
        }
    ]
    return render_template('index.html', posts=posts)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.checkpassword(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Registrationform()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.setpassword(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registered')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
