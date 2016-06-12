 # backup

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class ReigstrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 32), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          "Username have ONLY letters,"
                                          'numbers, dots, underscores')])
    password = PasswordField('Password', validators=[
        Required(), Length(6, 32, message='Lenth of password must over 6'),
        EqualTo('password2', message='password must be same as first typed.')])
    password2 = PasswordField('Comfirm password', validator=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(emial=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in user')
