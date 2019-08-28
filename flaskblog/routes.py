from flask import render_template, url_for, flash, redirect, request    # url_for searches for a file in the directory
from flaskblog import app, db, bcrypt                                   # To import from an __init__ file inside a package, use the package name directly
from flaskblog.forms import RegistrationForm, LoginForm                 # Import all classes from the 'forms' file
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


# Posts in the blog. Note how it is written
posts = [
    {
        'author': 'Pavly Salah',
        'title': 'Digizilla Task',
        'date': 'Aug. 27th 2019',
        'content': 'This is Pavly Salah\'s submission for the \
                    Digizilla Task. \
                    Framework used: Flask'
    },
    {
        'author': 'John Doe',
        'title': 'Dummy Title',
        'date': 'Aug. 27th 2019',
        'content': 'Hello, my name is John Doe and I do not really exist!'
    }
]

home_title = 'Home Page'
about_title = 'About Page'
db.create_all()       # To create the database containing User and Post from models.py 


# Home page
@app.route("/")        # Decorator
@app.route("/home")    # Having two decorators for a single page -- '/home' and '/'
def home():
    return render_template('home.html', posts=posts, title=home_title)    # Rendering a template page. Passing the 'posts' variable in order to be able to access it in the HTML template. Note that these paramters are user-defined


# About Page
@app.route("/about")    
def about():
    return render_template('about.html', title=about_title)


# Register page
@app.route("/register", methods=['GET', 'POST'])    # Allow GET and POST methods (allow the user to fill-in the forms and get redirected)
def register():
    # If the user is already logged in
    if current_user.is_authenticated:
        username = current_user.username
        flash(f'You are already logged in as {username}', 'success')
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():                   # If the registration is valid
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')                    # Encrypt the password using Flask-Bcrypt. decode('utf-8') is used to store the pssword as a string, not bytes
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)              # Create a user and save the hashed password instead of the plain-text one
        db.session.add(user)
        db.session.commit()                         # Add the registered user in the database
        flash(f'Account created successfully! You can now login, {form.username.data}!', 'success')        # Flash a message, 'success' (the second argument) is a Bootstrap class
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


# Login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    # If the user is already logged in
    if current_user.is_authenticated:
        username = current_user.username
        flash(f'You are already logged in as {username}', 'success')
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()                      # Get user by email from the DB

        # If a user with the entered email and password exists
        if user and bcrypt.check_password_hash(user.password, form.password.data):      # Member that the password stored in the DB (user.passowrd) is hashed, but check_password_hash un-hashes it
            login_user(user, remember=form.remember.data)                               # Login the user and check if he OR SHE checked the Remember Me checkbox
            flash(f'Log in successful! Welcome, {user.username}', 'success')            # Get the user's username from the DB
            next_page = request.args.get('next')                                        # If the user tried to access a page that required logging-in, he OR SHE will be redirected to it automatically                 
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Log-in unsucessful. Please check your email and password!', 'danger')

    return render_template('login.html', title="Login", form=form)


# Logout page
@app.route("/logout")
def logout():
    logout_user()
    flash('You have been successfully logged-out', 'success')
    return redirect(url_for('home'))


# Account page
@app.route("/account")
@login_required     # Must be logged-in to access this page
def account():
    return render_template('account.html', title="Account")