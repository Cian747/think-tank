from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.fields.core import IntegerField, SelectField
from wtforms.validators import Required


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')


class PitchForm(FlaskForm):
    pitch = TextAreaField('Write your pitch here:',validators = [Required()])
    category = SelectField('Pick a field',choices=[('Business','Business'),('Sports','sports'),('Creative','Creative'),('youth','youth')],validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment here: ',validators=[Required()])
    submit = SubmitField('Submit')