from flask import Flask, redirect, url_for, render_template, request, flash
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user
from flask import Blueprint
from app import db
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

auth_blueprint = Blueprint('auth', __name__)

# Flask-Login setup
login_manager = LoginManager()

# User model
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    def get_id(self):
        return str(self.id)

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            app.logger.debug(f"User {user.email} logged in successfully.")
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.')

    return render_template('login.html')


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash('An account with this email address already exists.')
            return redirect(url_for('auth.signup'))

        new_user = User(
            email=email,
            password_hash=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
