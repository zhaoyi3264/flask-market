import io

from flask import flash, render_template, redirect, url_for, request, send_file
from flask_login import login_user, logout_user, login_required, current_user

from market import app, db
from market.form import LoginForm, RegisterForm, PurchaseItemForm, SellItemForm
from market.model import Item, User

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()
    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        print(purchased_item)
        p = Item.query.filter_by(name=purchased_item).first()
        if p:
            if current_user.can_purchase(p):
                p.buy(current_user)
                flash(f'Congratulations! Your purchased {p.name} for ${p.price}', category='success')
            else:
                flash(f'Unfortunately, you don\'t have enough money to purchase {p.name}', category='danger')
        sold_item = request.form.get('sold_item')
        s = Item.query.filter_by(name=sold_item).first()
        if s:
            if current_user.can_sell(s):
                s.sell(current_user)
                flash(f'Congratulations! Your sold {s.name} for ${s.price}', category='success')
            else:
                flash(f'Something went wrong with selling {s.name}', category='danger')
        return redirect(url_for('market_page'))
    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)

        return render_template('market.html', items=items, purchase_form=purchase_form,
            owned_items=owned_items, sell_form=sell_form)

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

@app.route('/logo.png')
def logo():
    with open('./market/img/logo.png', 'rb') as img:
        return send_file(io.BytesIO(img.read()), mimetype='image/png')
