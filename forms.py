from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,FileField,EmailField,TextAreaField, SelectField
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


class StoryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()],render_kw={"class": "form-control", "placeholder": "Title"})
    category = SelectField('Category', choices=[('love', 'Love'), ('romantic', 'Romantic'), ('horror', 'Horror'), ('adventure', 'Adventure')], validators=[DataRequired()],render_kw={"class": "form-control"})
    content = TextAreaField('Content', validators=[DataRequired()],render_kw={"class": "form-control", "placeholder": "Type here ...","rows": 10})        
    submit = SubmitField('Publish', render_kw={"class": "btn btn-primary"})




