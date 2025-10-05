from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField, DecimalField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from app.extensions import db
from app.main.models import User
import sqlalchemy as sa

class DateSelectorForm(FlaskForm):
    due_date = DateField('Due date', validators=[DataRequired()])

    def validate_due_date(self, due_date):
        if due_date.data < datetime.now(timezone.utc).date():
            raise ValidationError('Due date must be in the future')

class TaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    start_time = TimeField("Start time", format="%H:%M", validators=[DataRequired()])
    finish_time = TimeField("End time", format="%H:%M", validators=[DataRequired()])

    def validate_finish_time(self, field):
        if self.start_time.data and field.data <= self.start_time.data:
            raise ValidationError("End time must be later than start time.")



