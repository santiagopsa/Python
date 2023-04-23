from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from email_validator import validate_email, EmailNotValidError
from flask_login import login_required
from flask import request, redirect, url_for, flash
from app.models import Debtor
import os
import binascii


app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(24))
app.config['DEBUG'] = True
app.config['ENV'] = 'production'
os.environ['DATABASE_URL'] = 'mysql+mysqlconnector://credcnqu_santiagopsa:Santgo33_@localhost/credcnqu_debtor'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#os.environ['DATABASE_URL'] = 'mysql+mysqlconnector://credcnqu_santiagopsa:Santgo33_@localhost/credcnqu_debt'
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)

migrate = Migrate(app, db)
# Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # This should be the name of your login route function

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        existing_user = User.query.filter_by(email=email).first()

        if existing_user is None:
            user = User(username=username, email=email)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))

        else:
            flash('A user with that email already exists.', 'error')

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Create an instance of the LoginForm class
    form = LoginForm()

    # Check if the request method is POST (i.e., the user has submitted the login form)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate the credentials (you can customize this part to match your user model and database)
        try:
            valid = validate_email(email)
            email = valid.email
            user = User.query.filter_by(email=email).first()
        except EmailNotValidError as e:
            flash(str(e), 'error')
            return redirect(url_for('login'))

        if user and user.check_password(password):
            # Log in the user and redirect them to the desired page
            login_user(user)
            return redirect(url_for('dashboard'))  # Or any other route you'd like to redirect the user to after successful login

    # Render the login template and pass the LoginForm instance to it
    return render_template('login.html', form=form)

@app.route('/add_debtor', methods=['POST'])
@login_required
def add_debtor():
# Get form data and create a new Debtor object
# Save the debtor to the database

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)

    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)



class Debtor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    debt = db.Column(db.Float, nullable=False)
    email_enabled = db.Column(db.Boolean, default=False)
    sms_enabled = db.Column(db.Boolean, default=False)
    reminder_interval = db.Column(db.Integer, default=7)
    last_email_date = db.Column(db.Date, default=datetime.now().date())
    last_sms_date = db.Column(db.Date, default=datetime.now().date())
    messages = db.Column(db.Text, default="")

def send_email(debtor):
    # Implementation for sending email reminders
    # Append new message to debtor's messages list
    debtor.messages += f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Reminder email sent.\n"

def send_sms(debtor):
    # Implementation for sending SMS reminders
    # Append new message to debtor's messages list
    debtor.messages += f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Reminder SMS sent.\n"

@app.route('/')
@login_required
def index():
    if request.method == 'POST' and 'name' in request.form and 'phone' in request.form and 'email' in request.form and 'debt' in request.form and 'reminder_interval' in request.form and 'email_enabled' in request.form and 'sms_enabled' in request.form:
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        debt = float(request.form['debt'])
        reminder_interval = int(request.form['reminder_interval'])
        email_enabled = True if request.form.get('email_enabled') == 'on' else False
        sms_enabled = True if request.form.get('sms_enabled') == 'on' else False

        new_debtor = Debtor(
            name=name,
            phone=phone,
            email=email,
            debt=debt,
            reminder_interval=reminder_interval,
            email_enabled=email_enabled,
            sms_enabled=sms_enabled
        )

        db.session.add(new_debtor)
        db.session.commit()

        return redirect(url_for('index'))

    else:
        debtors = Debtor.query.all()
        return render_template('index.html', debtors=debtors)

@app.route('/dashboard')
@login_required
def dashboard():
    debtors = Debtor.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', debtors=debtors)


@app.route('/delete/<int:id>')
def delete(id):
    debtor_to_delete = Debtor.query.get_or_404(id)

    db.session.delete(debtor_to_delete)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/view_messages/<int:id>')
def view_messages(id):
    # Retrieve the debtor from the database
    debtor = Debtor.query.get_or_404(id)
    # Strip the messages string of any leading or trailing whitespaces before splitting it into a list
    messages = debtor.messages.strip().split("\n")
    # Remove the last empty string in the list
    messages.pop()
    # Reverse the list so that the most recent messages appear first
    messages.reverse()
    return render_template('messages.html', debtor=debtor, messages=messages)

def schedule_daily_reminders():
    # Calculate the next reminder date for each debtor and schedule the reminder
    # This function should be run once a day
    today = datetime.now().date()

    debtors = Debtor.query.all()

    for debtor in debtors:
        if debtor.email_enabled:
            next_email_date = debtor.last_email_date + timedelta(days=debtor.reminder_interval)
            while next_email_date <= today:
                # If the next email date has already passed, add the reminder and calculate the next email date
                send_email(debtor)
                debtor.last_email_date = next_email_date
                next_email_date = debtor.last_email_date + timedelta(days=debtor.reminder_interval)

        if debtor.sms_enabled:
            next_sms_date = debtor.last_sms_date + timedelta(days=debtor.reminder_interval)
            while next_sms_date <= today:
                # If the next SMS date has already passed, add the reminder and calculate the next SMS date
                send_sms(debtor)
                debtor.last_sms_date = next_sms_date
                next_sms_date = debtor.last_sms_date + timedelta(days=debtor.reminder_interval)

        db.session.commit()
