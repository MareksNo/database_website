from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from models import User


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


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
