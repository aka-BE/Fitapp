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
    email = StringField('Email', validators=[DataRequired(), Length(min=10), Email(message='შიყვანეთ მეილი.')])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=9, message='შეიყვანეთ ნომერი.')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='შეიყვანეთ ძლიერი პაროლი.')])
    confirm = PasswordField('Confirm Your Password', validators=[DataRequired(), EqualTo('password', message='პაროლი არ ემთხვევა.')])
    submit = SubmitField('რეგისტრაცია')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('შესვლა')


class FeedbackForm(FlaskForm):
    """Feedback Form."""
    fullname = StringField('Fullname', validators=[DataRequired()])
    email = StringField('Email', validators=[Length(min=10), Email(message='შიყვანეთ სწორი მეილი.'), DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=9, message='შეიყვანეთ ნომერი.')])
    body = StringField('Message', validators=[DataRequired(),Length(min=4, message='შეტყობინება ძალიან მოკლეა')])
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    food = StringField('Food', validators=[DataRequired(), Length(max=40)])
    gr = IntegerField('Gr', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('დამატება')

