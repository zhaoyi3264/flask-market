from flask import flash, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required

from market import app, db
from market.form import LoginForm, RegisterForm
from market.model import Item, User

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
@login_required
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
            email_address=form.email_address.data,
            password=form.password1.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f'Account created successfully! You are logged in as: {user.username}', category='success')
        return redirect(url_for('market_page'))
    if form.errors:
        for err in form.errors.values():
            flash(err, category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'Success! You are logged in as: {user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('User name and password are not match!', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('home_page'))