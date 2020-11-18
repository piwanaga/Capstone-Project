from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    """Form to register a new user"""
    
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[Length(min=6)])
    password = PasswordField('Password', validators=[Length(min=6)])
    

class LoginForm(FlaskForm):
    """Form for user to login"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class EditUserForm(FlaskForm):
    """Form to edit user"""

    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    image_url = StringField('Profile Picture') 
    market = SelectField('Region', choices=[('en-AU', 'Australia'), ('en-CA', 'Canada'), ('zh-CN', 'China'), ('en-IN', 'India'), ('ja-JP', 'Japan'), ('en-gb', 'United Kingdom'), ('en-US', 'United States')], default='en-US')
