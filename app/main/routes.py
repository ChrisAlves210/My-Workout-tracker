from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.main.forms import WorkoutForm, GoalForm
from app.models import Workout, Goal
from app.extensions import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
	workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.date.desc()).limit(10).all()
	goals = Goal.query.filter_by(user_id=current_user.id).all()
	return render_template('dashboard.html', workouts=workouts, goals=goals)

@main.route('/workouts/new', methods=['GET', 'POST'])
@login_required
def new_workout():
	form = WorkoutForm()
	if form.validate_on_submit():
		workout = Workout(
			user_id=current_user.id,
			date=form.date.data,
			type=form.type.data,
			duration_minutes=form.duration_minutes.data,
			calories=form.calories.data,
			notes=form.notes.data,
		)
		db.session.add(workout)
		db.session.commit()
		flash('Workout logged!', 'success')
		return redirect(url_for('main.dashboard'))
	return render_template('workout_form.html', form=form)

@main.route('/goals/new', methods=['GET', 'POST'])
@login_required
def new_goal():
	form = GoalForm()
	if form.validate_on_submit():
		goal = Goal(
			user_id=current_user.id,
			title=form.title.data,
			target_value=form.target_value.data,
			unit=form.unit.data,
		)
		db.session.add(goal)
		db.session.commit()
		flash('Goal created!', 'success')
		return redirect(url_for('main.dashboard'))
	return render_template('goal_form.html', form=form)

@main.route('/workouts')
@login_required
def workouts_list():
	workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.date.desc()).all()
	return render_template('workouts.html', workouts=workouts)