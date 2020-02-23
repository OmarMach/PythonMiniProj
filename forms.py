from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,TextAreaField,SelectField
from wtforms.validators import DataRequired

class AjouterReclamationForm(FlaskForm):
    type = SelectField('Type', choices=[('Message to a colleague ', 'Message to a colleague'),
                                        ('Message to a teacher', 'Message to a teacher'),
                                        ('Ask for an administrative service', 'Ask for an administrative service'),
                                        ('Confession ', 'Confession'),
                                        ('Other ', 'Other'),
                                        ])
    message = TextAreaField('Message', [DataRequired()])
    submit = SubmitField('Send')

class adminConnectionForm(FlaskForm):
    login = StringField('Login', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Login')

class ajouterAdmin(FlaskForm):
    login = StringField('Login', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Create')
