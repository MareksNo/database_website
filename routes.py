import hashlib
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegisterForm, LoginForm
from config import app, db
from models import User, Product
from flask_login import login_user, current_user, logout_user, login_required


from flask.views import MethodView

secret_key = 'akufiuyefiquykfbdu234'


def hash_data(data_input):

    input_salt = data_input + secret_key

    hasher = hashlib.sha256()
    hasher.update(input_salt.encode('utf-8'))

    hashed_in_pass = hasher.hexdigest()

    return hashed_in_pass


class HomePageView(MethodView):
    def get(self):
        products = Product.query.all()
        if request.method == 'GET':
            return render_template('home.html', title='Home', current_page='home', products=products)

    def post(self):
        if request.method == 'POST':
            product_search = request.form.get('name')
            return redirect(url_for('search_product', search_name=product_search))


class RegistrationView(MethodView):
    def get(self):
        form = RegisterForm()  # getting the Register form from forms.py and setting to a variable
        return render_template('register.html', title='Register', form=form,
                               current_page='register')

    def post(self):
        form = RegisterForm()  # getting the Register form from forms.py and setting to a variable
        if form.validate_on_submit():
            hashed_password = hash_data(form.password.data)

            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()

            flash(f'Account Created successfully!', category='success')  # Flash on success

            return redirect(url_for('login'))


class LoginView(MethodView):
    def get(self):
        form = LoginForm()
        return render_template('login.html', title='Login', form=form,
                               current_page='login')  # rendering the template for LogIn

    def post(self):
        form = LoginForm()  # getting the LogIN form from forms.py and setting to a variable
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()  # searching for the email
            if user and user.password == hash_data(
                    form.password.data):  # checks password hashes and if the email exists
                login_user(user, remember=form.remember.data)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('home_page'))
            else:
                flash('Invalid username or password!',
                      category='danger')  # is executed if emails or passwords don't match


class AddProductView(MethodView):
    decorators = [
        login_required,
    ]

    def get(self):
        return render_template('add_product.html', title='Add Product', current_page='new_product')

    def post(self):
        product = Product(product_name=request.form.get('product_name'),
                          price=request.form.get('price'),
                          seller_username=current_user.username)
        db.session.add(product)
        db.session.commit()
        flash('Added a product successfully!', category='success')
        return redirect(url_for('home_page'))


class LogoutView(MethodView):
    decorators = [
        login_required,
    ]

    def get(self):
        return render_template('logout.html', title=f'{current_user.username} Logout', current_page='logout')

    def post(self):
        logout_user()
        return redirect(url_for('login'))


class DisplayProductView(MethodView):
    def get(self, product_id):
        product = Product.query.get_or_404(product_id)
        return render_template('display_product.html', title=product.product_name, product=product)


class SearchProductView(MethodView):
    def get(self, search_name):
        products = Product.query.filter(Product.product_name.contains(search_name))
        return render_template('search_product.html', title=search_name, products=products)

