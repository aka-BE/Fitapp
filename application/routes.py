"""Logged-in page routes."""
from flask import Blueprint, render_template, redirect, url_for, session, flash, jsonify, request
from flask_login import login_required, logout_user


from .forms import FeedbackForm, SearchForm, LogForm
from .models import Feedback, Log, Food, db


# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@home_bp.route('/', methods=['GET', 'POST'])
def home():
    """
    User feedback.

    GET requests serve home page.
    POST requests validate form & receive feedback.
    """

    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(
            fullname=form.fullname.data,
            email=form.email.data,
            phone=form.phone.data,
            body=form.body.data
        )
        db.session.add(feedback)
        db.session.commit()
        flash("Feedback received!")
    else:
        flash("Error submiting form")
    
    return render_template(
        'home.html',
        form=form,
        title="Home page.",
        template="home-page",
        body="Home page."
    )


@home_bp.route('/calculator', methods=['GET', 'POST'])
def calculator():
    """
    Calculator page.

    GET requests serve calculator page.
    POST requests receive user calories goal. (# Not implamented yet)
    """

    return render_template(
        'calculator.html',
        title="Calculator page.",
        template="calculator-page",
        body="Calculator page."
    )    


@home_bp.route('/calendar', methods=['GET', 'POST'])
def calendar():
    """
    Calendar page.

    GET requests serve calendar page.
    POST requests receive user calories input.
    """

    return render_template(
        'calendar.html',
        form=form,
        title="Calendar page.",
        template="calendar-page",
        body="Calendar page."
    )


@home_bp.route('/create_log', methods=['POST'])
def create_log():
    """
    Create log.

    POST request add date to calendar page.
    """

    form = LogForm()
    if form.validate_on_submit():
        date = form.date.data
        print(date)

    return redirect(url_for(view))



@home_bp.route('/view', methods=['GET', 'POST'])
def view():
    """
    Calendar view page.

    GET requests serve calendar view page.
    POST requests receive user calories input.
    """

    form = SearchForm()

    return render_template(
        'view.html',
        form=form,
        title="View page.",
        template="View-page",
        body="View page."
    ) 

@home_bp.route('/food', methods=['GET'])
def fooddic():
    """
    Food search view page.

    GET request search suggestions.
    """

    res = Food.query.all()
    list_food = [r.as_dict() for r in res]   
    
    return jsonify(list_food)


@home_bp.route('/logout')
@login_required
def logout():
    """User logout logic."""
    session.pop('user', None)
    logout_user()
    return redirect(url_for('auth_bp.login'))
