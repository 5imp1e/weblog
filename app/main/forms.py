from flask.ext.wtf import Form
from flask.ext.pagedown.fields import PageDownField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class PostForm(Form):
    body = PageDownField('It is time to write what is in your mind!',
                         validators=[Required()])
    submit = SubmitField('Submit')


class CommentForm(Form):
    body = PageDownField('', validators=[Required()])
    submit = SubmitField('Submit')
