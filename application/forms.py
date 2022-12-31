"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange
)


class SignupForm(FlaskForm):
    """User Sign-up Form."""
    fullname = StringField('Fullname',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email', validators=[Length(min=10), Email(message='Enter a valid email.'), DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=9, message='Use valid number')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('რეგისტრაცია')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField('Email', validators=[DataRequired(), Email(message='Enter a valid email.')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('შესვლა')


class FeedbackForm(FlaskForm):
    """Feedback Form."""
    fullname = StringField('Fullname', validators=[DataRequired()])
    email = StringField('Email', validators=[Length(min=10), Email(message='Enter a valid email.'), DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=9, message='Use valid number')])
    body = StringField('Message', validators=[DataRequired(),Length(min=4, message='Your message is too short')])
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    food = StringField('Food', validators=[DataRequired(), Length(max=40)])
    gr = IntegerField('Gr', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('დამატება')


class LogForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('დამატება')
