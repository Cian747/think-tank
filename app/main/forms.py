from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.fields.core import IntegerField
from wtforms.validators import Required


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')


class PitchForm(FlaskForm):
    pitch = TextAreaField('Write yor pitch here:',validators = [Required()])
    category = IntegerField('Category ID')
    submit = SubmitField('Submit')