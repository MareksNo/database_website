import hashlib


from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegisterForm, LoginForm, AddProductForm
from config import app, db
from models import User, Product
from flask_login import login_user, current_user, logout_user, login_required

from werkzeug.security import check_password_hash

from flask.views import MethodView

secret_key = 'akufiuyefiquykfbdu234'


class HomePageView(MethodView):
    def get(self):
        products = Product.query.all()

        return render_template('home.html', title='Home', current_page='home', products=products)

    def post(self):
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
            form.save()

            return redirect(url_for('login'))
        else:
            flash(f'Please Check your form', category='danger')
            return render_template('register.html', title='Register', form=form, current_page='register')


class LoginView(MethodView):
    def get(self):
        form = LoginForm()
        return render_template('login.html', title='Login', form=form,
                               current_page='login')
        # rendering the template for LogIn

    def post(self):
        form = LoginForm()  # getting the LogIN form from forms.py and setting to a variable
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()  # searching for the email

            if form.login(user):
                return redirect(url_for('home_page'))

        return render_template('login.html', title='Login', form=form,
                               current_page='login')


class AddProductView(MethodView):
    decorators = [
        login_required,
    ]

    def get(self):
        form = AddProductForm()
        return render_template('add_product.html', title='Add Product', current_page='new_product', form=form)

    def post(self):
        form = AddProductForm()

        product = Product.add_product(product_name=form.product_name.data,
                                      price=form.price.data,
                                      seller_username=current_user.username)

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
