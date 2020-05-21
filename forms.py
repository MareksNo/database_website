import hashlib

from flask import flash

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError

from werkzeug.security import check_password_hash

from flask_login import login_user

from config import db
from models import User

secret_key = 'akufiuyefiquykfbdu234'


class RegisterForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=15)])  # username field
    email = StringField('Email',
                        validators=[DataRequired(), Email()])  # email field
    password = PasswordField('Password', validators=[DataRequired()])  # Password field
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                     EqualTo('password')])  # Confirm Password field
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            flash(f'This username is taken!', category='danger')
            raise ValidationError('The username is taken!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            flash(f'This email is taken!', category='danger')
            raise ValidationError('The email is taken!')

    def save(self):

        user = User.create(
            username=self.username.data,
            email=self.email.data,
            password=self.password.data,
        )

        db.session.add(user)
        db.session.commit()

        flash(f'Account Created successfully!', category='success')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            flash(f'Wrong Email', category='danger')
            raise ValidationError('Wrong Credentials(Email)')

    def login(self, user):
        if check_password_hash(user.password, self.password.data):

            flash('Logged in successfully!', category='success')

            login_user(user, remember=self.remember.data)

            return True


class AddProductForm(FlaskForm):
    product_name = StringField('Product Name',
                               validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
