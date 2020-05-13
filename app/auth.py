from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from .forms import LoginForm, SignupForm
from .models import db, User
from . import login_manager

auth_bp = Blueprint('auth_bp',__name__, template_folder='templates', static_folder='static')




@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.

    GET: Serve Log-in page.
    POST: Validate form and redirect user to dashboard.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.dashboard'))  # Bypass if user is logged in

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # Validate Login Attempt
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if user.is_admin == 1:
                return redirect(url_for('main_bp.admin'))
            return redirect(next_page or url_for('main_bp.dashboard'))
        flash('Invalid username or password combination')
        return redirect(url_for('auth_bp.login'))
    return render_template('login.jinja2',
                           form=form,
                           title='Log in',
                           template='login-page',
                           body="Log in with your account.")


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
   
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(name=form.name.data,
                        email=form.email.data,
                        is_admin=0)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            return redirect(url_for('main_bp.dashboard'))
        flash('A user already exists with that email address.')
    return render_template('signup.jinja2',
                           title='Create an Account.',
                           form=form,
                           template='signup-page',
                           body="Sign up for a user account.")

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))