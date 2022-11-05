from flask import Blueprint, render_template, request, flash, redirect, url_for, session

from website import views
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Checks first if current user is already logged in
    # Authenticated users cannot go to the login page but will be redirected to the Home page
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    # Processes the Login form
    if request.method == 'POST':
        # Gets the user input
        email = request.form.get('email')
        password = request.form.get('password')

        # Checks if the email entered is existing in the database
        user = User.query.filter_by(email=email).first()

        # If the email was found, it will now undergo validations
        if user:
            # Checks if the password entered matches the one in the database
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # If password matches, it will now log in the user
                # 'remember' is set to True to prevent the user from being logged out
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
@login_required
def sign_up():
    # Validates is the user is Admin or not
    if current_user.id > 3:
        return redirect(url_for('views.home'))

    # Processes the create account form
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Searches the database if the email is already existing
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Please input a valid e-mail.', category='error')
            pass
        elif len(firstName) < 2:
            flash('Please input a valid First Name', category='error')
            pass
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
            pass
        elif len(password1) < 7:
            flash('Please input a valid password.', category='error')
            pass
        else:
            # Add user to database
            newUser = User(email=email, firstName=firstName,
                           password=generate_password_hash(password1, method='sha256'))
            db.session.add(newUser)
            db.session.commit()
            flash('Account successfully created.', category='success')
            return redirect(url_for('auth.sign_up'))
    return render_template("sign_up.html", user=current_user)
