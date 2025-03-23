from flask import Blueprint, flash, redirect, render_template, request, session, url_for,sessions

from models import User, db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


main = Blueprint("main", __name__)

@main.route('/')
def index():
   return render_template("index.html")

@main.route('/login')
def login():
    return render_template("login.html")

@main.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        flash("Please login first.", "error")
    user = User.query.get(session['user_id'])
    return render_template("dashboard.html", user=user)

@main.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    # Debugging: Print the username and password being received
    print(f"Username: {username}")
    print(f"Password: {password}")
    
    # Check if the user exists
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User does not exist. Please register first.", "error")
        return redirect(url_for('main.login'))  # Redirect to login page

    # Debugging: Print the stored password hash
    print(f"Stored Hash: {user.password}")

    # Check if the password matches the hashed password
    if check_password_hash(user.password, password):
        flash("Login successful!", "success")
        session["user_id"] = user.id  # Store user ID in session
        return redirect(url_for('main.dashboard'))  # Redirect to profile page
    
    flash("Incorrect password. Please try again.", "error")
    return redirect(url_for('main.login'))  # Redirect back to login page



@main.route('/register')
def register():
    return render_template("register.html")


@main.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    password = request.form.get('password')
    fullname = request.form.get('fullname')
    qualification = request.form.get('qualification')

    # Check if user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash("User already exists. Please login instead.", "error")
        return redirect(url_for('main.register'))  # Redirect to register page

    # Hash the password before storing it
    password_hash = generate_password_hash(password)

    # Create a new user in the database
    new_user = User(username=username, password=password_hash, fullname=fullname, qualification=qualification)
    
    db.session.add(new_user)
    db.session.commit()
    
    flash("Registration successful! You can now log in.", "success")
    return redirect(url_for('main.login'))  # Redirect to login page after successful registration
