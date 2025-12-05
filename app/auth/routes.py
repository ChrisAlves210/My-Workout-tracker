from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.auth.forms import SignupForm, LoginForm
from app.models import User
from app.extensions import db

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('main.dashboard'))
	form = SignupForm()
	if form.validate_on_submit():
		if User.query.filter((User.email == form.email.data) | (User.username == form.username.data)).first():
			flash('Email or username already exists', 'warning')
		else:
			user = User(email=form.email.data, username=form.username.data)
			user.set_password(form.password.data)
			db.session.add(user)
			db.session.commit()
			flash('Account created! Please log in.', 'success')
			return redirect(url_for('auth.login'))
	return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.dashboard'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and user.check_password(form.password.data):
			login_user(user)
			flash('Logged in successfully.', 'success')
			next_page = request.args.get('next')
			return redirect(next_page or url_for('main.dashboard'))
		flash('Invalid credentials', 'danger')
	return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('Logged out.', 'info')
	return redirect(url_for('auth.login'))