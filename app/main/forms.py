from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class WorkoutForm(FlaskForm):
	date = DateField('Date', validators=[DataRequired()])
	type = StringField('Type', validators=[DataRequired(), Length(max=64)])
	duration_minutes = IntegerField('Duration (min)', validators=[DataRequired(), NumberRange(min=1)])
	calories = IntegerField('Calories', validators=[NumberRange(min=0)])
	notes = TextAreaField('Notes', validators=[Length(max=500)])
	submit = SubmitField('Save Workout')

class GoalForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired(), Length(max=128)])
	target_value = IntegerField('Target Value', validators=[DataRequired(), NumberRange(min=1)])
	unit = StringField('Unit', validators=[DataRequired(), Length(max=32)])
	submit = SubmitField('Save Goal')