from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import User
from models.donor import Donor
from app.extensions import db
from flask_login import login_user, login_required, current_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method=='POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #validation
        if password1!=password2:
            flash('Password Missmatched', category="error")
            return redirect(url_for('auth.sign_up'))
        
        #check is user already exist
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', category='error')
            return redirect(url_for('auth.sign_up'))
            
        #hashing password
        hashed_password = generate_password_hash(password1)

        #create user object
        new_user = User(
            fullname = fullname,
            email = email,
            password = hashed_password,
            role = 'nuser'
        )

        #save to database
        db.session.add(new_user)
        db.session.commit()

        flash('Account created succesfully!', category='success')
        return redirect(url_for('auth.login'))

    return render_template('sign_up.html')

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Sorry, We couldn't find any user with this email! Consider signing up", category='error')
        elif user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home.home_page'))
        else:
            flash("Invalid email or password", category='error')
    
    return render_template('login.html')

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
