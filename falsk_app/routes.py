from flask import render_template, url_for, flash, redirect, request
from flask_app import app, db, bcrypt
from flask_app.forms import RegistrationForm, LoginForm
from flask_app.models import User, Appointment, Review
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        current_user.username = request.form['username']
        current_user.email = request.form['email']
        current_user.bio = request.form['bio']
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    return render_template('account.html', title='Account')

@app.route("/create_appointment", methods=['POST'])
@login_required
def create_appointment():
    client_id = request.form.get('client_id')
    employer_id = request.form.get('employer_id')
    appointment_date = request.form.get('appointment_date')
    status = request.form.get('status')

    new_appointment = Appointment(client_id=client_id, employer_id=employer_id, appointment_date=appointment_date, status=status)
    db.session.add(new_appointment)
    db.session.commit()

    flash('Appointment created successfully!', 'success')
    return redirect(url_for('home'))

@app.route("/add_review", methods=['POST'])
@login_required
def add_review():
    client_id = request.form.get('client_id')
    employer_id = request.form.get('employer_id')
    comment = request.form.get('comment')
    created_at = datetime.utcnow()

    new_review = Review(client_id=client_id, employer_id=employer_id, comment=comment, created_at=created_at)
    db.session.add(new_review)
    db.session.commit()

    flash('Review added successfully!', 'success')
    return redirect(url_for('home'))
