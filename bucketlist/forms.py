from flask_wtf import FlaskForm

from wtforms import StringField, BooleanField, PasswordField, TextAreaField, SubmitField, DateField

from wtforms.validators import DataRequired, Email, EqualTo

class SignUpForm(FlaskForm):
    fullname = StringField('Fullname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                     EqualTo('password')])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField("Login")

class BucketlistForm(FlaskForm):
    bucketlistname = StringField('Bucketlist name', validators=[DataRequired()])
    simple_description = TextAreaField("Simple Description", validators=[DataRequired()])
    submit = SubmitField("Add Bucketlist")

class BucketlistFormUpdate(FlaskForm):
    bucketlistname = StringField('Bucketlist name', validators=[DataRequired()])
    simple_description = TextAreaField("Simple Description", validators=[DataRequired()])
    submit = SubmitField("Update Bucketlist")

class ActivityForm(FlaskForm):
    bucketlist_activity_name = StringField('Bucketlist Activity Name', validators=[DataRequired()])
    date = StringField("Have this done by", validators=[DataRequired()])
    submit = SubmitField("Add Activity")

class ActivityFormUpdate(FlaskForm):
    bucketlist_activity_name = StringField('Bucketlist Activity Name', validators=[DataRequired()])
    date = StringField("Have this done by", validators=[DataRequired()])
    submit = SubmitField("Update Activity")