
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL
from ..models.UserModel import User


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    checklicense = BooleanField('I agree to the license terms.')
    submit = SubmitField('Sign Up')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('That email is taken. Please login')


class LoginForm(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UploadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    sub_title = StringField('Sub Title', validators=[DataRequired()])
    cover_image = StringField('Cover Image Link', validators=[DataRequired(), URL()])
    cta_title = StringField('CTA Title', validators=[DataRequired()])
    keywords = StringField('Keywords', validators=[DataRequired()])
    content = StringField('Contents', validators=[DataRequired()])

class ProfileEditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = StringField('Bio')
    facebook = StringField('Facebook', validators=[URL()])
    instagram = StringField('Instagram', validators=[URL()])
    linkedin = StringField('Linkedin', validators=[URL()])
    twitter = StringField('Twitter', validators=[URL()])
    