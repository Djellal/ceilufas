from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateTimeLocalField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Role', choices=[('student', 'Student'), ('teacher', 'Teacher'), ('admin', 'Admin')])
    submit = SubmitField('Create')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')


class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('student', 'Student'), ('teacher', 'Teacher'), ('admin', 'Admin')])
    submit = SubmitField('Update')


class StateForm(FlaskForm):
    id = StringField('Code', validators=[DataRequired(), Length(max=10)])
    name = StringField('Name', validators=[DataRequired(), Length(max=250)])
    name_ar = StringField('Name (Arabic)', validators=[DataRequired(), Length(max=250)])
    submit = SubmitField('Save')


class MunicipalityForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=250)])
    name_ar = StringField('Name (Arabic)', validators=[DataRequired(), Length(max=250)])
    submit = SubmitField('Save')


class SessionForm(FlaskForm):
    session_code = StringField('Session Code', validators=[DataRequired(), Length(max=30)])
    session_name = StringField('Session Name', validators=[DataRequired(), Length(max=250)])
    session_name_ar = StringField('Session Name (Arabic)', validators=[DataRequired(), Length(max=250)])
    start_date = DateTimeLocalField('Start Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_date = DateTimeLocalField('End Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Save')


class ProfessionForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=300)])
    name_ar = StringField('Name (Arabic)', validators=[DataRequired(), Length(max=300)])
    fee_value = DecimalField('Default Fee Value', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Save')
