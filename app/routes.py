from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import Loginform, Registrationform, Postform
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from datetime import datetime
import base64


@app.route('/')
@app.route('/index')
@login_required
def index():
    image = open('C:/Users/rados/Desktop/PythonKurs/0toflask/app/images.png','rb')
    image_read = image.read()
    image_64 = base64.b64encode(image_read)
    print(image_64)
    img_decode = image_64.decode()
    posty = Post.query.all()
    return render_template('index.html', posts=posty,image=img_decode )


@app.route('/user/<username>')
@login_required
def userpage(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)
    return render_template('user.html', user=user, posts=posts)


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


@app.route('/myprofile', methods=['GET', 'POST'])
@login_required
def myprofile():
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        form = Postform()
        if form.validate_on_submit():
            print(form.body.data, datetime.utcnow(), user)
            newpost = Post(body=form.body.data, author=user)
            db.session.add(newpost)
            db.session.commit()
            return redirect(url_for('myprofile'))
        posts = Post.query.filter_by(author=user)
        return render_template('myprofile.html', posts=posts, form=form)
    return redirect(url_for('login'))
