"""Logged-in page routes."""
from flask import Blueprint, render_template, redirect, url_for, session, flash, jsonify, request
from flask_login import login_required, logout_user, current_user
from datetime import datetime


from .forms import FeedbackForm, SearchForm
from .models import Feedback, Log, Food, Prod, log_food, db


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
        flash("შეტყობინება მიღებულია!", 'error')
        return redirect(url_for("home_bp.home", form=form))
    
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


@home_bp.route('/calendar', methods=['GET'])
@login_required
def calendar():
    """
    Calendar page.

    GET requests serve calendar page.
    """

    user = current_user 
    logs = Log.query.filter_by(usr=user).order_by(Log.date.desc()).all() # Get logs for current user

    log_dates = [] # Create list

    for log in logs:            # Loop over every log date
        cal = 0                 # Define total calories as 0
        for prod in log.prods:  # Loop over every product in log
            cal += prod.cal     # Add together calories for looped product per log

        # Create dictionary and add values of the current log and the total accumulated cal respectively
        log_dates.append({
            'log_date' : log,
            'cal' : cal
        })


    return render_template(
        'calendar.html',
        log_dates=log_dates,
        title="Calendar page.",
        template="calendar-page",
        body="Calendar page."
    )


@home_bp.route('/create_log', methods=['POST'])
@login_required
def create_log():
    """
    Create log.

    POST request add date to calendar page.
    """
    user = current_user
    date = request.form.get('date') # Get date from user

    if not date:
        flash('აირჩიეთ თარიღი', 'error')
        return redirect(url_for('home_bp.calendar'))

    log = Log(date=datetime.strptime(date, '%Y-%m-%d'), usr=user) # Add date to model

    db.session.add(log)
    db.session.commit()

    return redirect(url_for('home_bp.view', log_id=log.id))


@home_bp.route('/view/<int:log_id>', methods=['GET', 'POST'])
@login_required
def view(log_id):
    """
    Calendar view page.

    GET requests serve calendar view page.
    POST requests receive user calories input.
    """

    form = SearchForm() # Form for products search
    user = current_user
    log = Log.query.get_or_404(log_id)

    # Checks if the user trying to access the log is the owner of the log
    if user.id != log.user_id:
        return redirect(url_for('home_bp.calendar'))
    
    # If the user is the owner of the log
    else:
        # Get total calories for the log
        total = {
            'cal' : 0
        }

        for prod in log.prods:
            total['cal'] += prod.cal

        return render_template(
            'view.html',
            form=form,
            log=log,
            total=total,
            title="View page.",
            template="View-page",
            body="View page."
        )


@home_bp.route('/remove_log/<int:log_id>')
@login_required
def remove_log(log_id):
    """
    GET requests to remove log.
    """

    user = current_user
    log = Log.query.get_or_404(log_id)

    # Checks if the user trying to access the log is the owner of the log
    if user.id != log.user_id:
        return redirect(url_for('home_bp.calendar'))
    # If user is owenr of the log, delete the log.
    else:    
        db.session.delete(log)
        db.session.commit()

        return redirect(url_for('home_bp.calendar'))


@home_bp.route('/add_food_to_log/<int:log_id>', methods=['POST'])
@login_required
def add_food_to_log(log_id):
    """
    
    POST request to add food to log. 
    """

    log = Log.query.get_or_404(log_id)  # retrieve log by id, return 404 error if not found

    form = SearchForm()
    food_name = form.food.data                          # get the food name from the form data
    food = Food.query.filter_by(name=food_name).first() # retrieve the food from the database by name

    gr = form.gr.data # get the weight of the food in grams from the form data

    cal = gr * food.cal # calculate the number of calories in the food based on the weight

    # create a new Prod object with the food name, calories, and weight
    prod = Prod(name=food.name, cal=cal, gr=gr)
    db.session.add(prod)
    db.session.commit()

    # add the new food to the log_food table, linking the log and prod 
    add_food = log_food.insert().values(
        log_id=log.id,
        prod_id=prod.id
    )
    db.session.execute(add_food)
    db.session.commit()

    return redirect(url_for('home_bp.view', log_id=log_id))


@home_bp.route('/remove_food_from_log/<int:log_id>/<int:prod_id>')
@login_required
def remove_food_from_log(log_id, prod_id):
    """
    
    GET request to remove food from log. 
    """

    user = current_user
    log = Log.query.get_or_404(log_id)

    # Checks if the user trying to access the log is the owner of the log
    if user.id != log.user_id:
        return redirect(url_for('home_bp.calendar'))
    # If user is owenr of the log, delete the log.
    else:

        prod = Prod.query.get(prod_id)

        log.prods.remove(prod)
        db.session.commit()

        return redirect(url_for('home_bp.view', log_id=log_id))


@home_bp.route('/food', methods=['GET'])
@login_required
def fooddic():
    """
    For food search on view page.

    GET request search suggestions.
    """

    res = Food.query.all()
    list_food = [r.as_dict() for r in res]   
    
    return jsonify(list_food)


@home_bp.route('/terms')
def terms():
    """
    Terms page.

    GET requests serve terms page.
    """

    return render_template(
        'terms.html',
        title="Terms page.",
        template="terms-page",
        body="Terms page."
    )   


@home_bp.route('/services')
def services():
    """
    Services page.

    GET requests serve terms page.
    """

    return render_template(
        'services.html',
        title="Services page.",
        template="services-page",
        body="Services page."
    )    


@home_bp.route('/logout')
@login_required
def logout():
    """User logout logic."""
    session.pop('user', None)
    logout_user()
    return redirect(url_for('auth_bp.login'))
