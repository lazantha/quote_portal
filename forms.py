from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,FileField,EmailField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo

class UserRegisterForm(FlaskForm):
    user_name=StringField('User Name', validators=[DataRequired()])
    email=EmailField('Email')
    password=PasswordField('Password', validators=[DataRequired()])
    con_password=PasswordField('Confirm Password', validators=[DataRequired()])
    dp=FileField('Profile Picture')
    submit=SubmitField('Submit')


class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"class": "form-control", "placeholder": "Email Address"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"class": "form-control", "placeholder": "Password"})
    submit = SubmitField('Login', render_kw={"class": "btn btn-primary"})


