from datetime import datetime
from app.extensions import db, login_manager, bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True, nullable=False)
	username = db.Column(db.String(64), unique=True, nullable=False)
	password_hash = db.Column(db.String(128), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)

	workouts = db.relationship('Workout', backref='user', lazy=True)
	goals = db.relationship('Goal', backref='user', lazy=True)

	def set_password(self, password: str):
		self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

	def check_password(self, password: str) -> bool:
		return bcrypt.check_password_hash(self.password_hash, password)

class Workout(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	date = db.Column(db.Date, default=datetime.utcnow)
	type = db.Column(db.String(64), nullable=False)  # e.g., run, lift, yoga
	sets = db.Column(db.Integer, nullable=False)
	weight = db.Column(db.Integer)  # in pounds or kg
	reps = db.Column(db.Integer)
	calories = db.Column(db.Integer)
	notes = db.Column(db.Text)

class Goal(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	title = db.Column(db.String(128), nullable=False)
	target_value = db.Column(db.Integer, nullable=False)  # e.g., minutes/week, workouts/week
	current_value = db.Column(db.Integer, default=0)
	unit = db.Column(db.String(32), nullable=False)
	due_date = db.Column(db.Date)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)