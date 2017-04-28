from flask_wtf import Form 
from wtforms import StringField , PasswordField,SubmitField
class UserForm(Form):
	firs_name = StringField("first Name")
	last_name = StringField("last Name")
	password = PasswordField("Password")
	submit = SubmitField("Sign Up")
		