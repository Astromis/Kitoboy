from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired#, 
from wtforms import SelectField, HiddenField, SubmitField, IntegerField, StringField
from wtforms.validators import InputRequired
from config import Config

OUTER_STATS = {}

class SocnetUploadForm(FlaskForm):
    file = FileField(validators=[FileRequired()])

class StatusForm(FlaskForm):
    id = HiddenField("id")
    status = SelectField("status", choices=Config.SUICIDAL_RATING)
    submit = SubmitField('Update Record')

class AddRealUser(FlaskForm):
    first_name = StringField("first_name", validators=[ InputRequired()])
    last_name = StringField("last_name", validators=[ InputRequired()])
    middle_name = StringField("middle_name", validators=[ InputRequired()])
    age = StringField("age", validators=[ InputRequired()])
    from_country = StringField("from_country", validators=[ InputRequired()])
    study_level = StringField("study_level", validators=[ InputRequired()])
    status = StringField("status", validators=[ InputRequired()])

class AddDigitalUser(FlaskForm):
    id_real = HiddenField("id_real")
    
    socnet_id = StringField("socnet_id", validators=[ InputRequired()])
    socnet_name = StringField("socnet_name", validators=[ InputRequired()])
    account_status = StringField("account_status", validators=[ InputRequired()])
    suicide_rating = StringField("suicide_rating", validators=[ InputRequired()])

class AddLog(FlaskForm):
    id_real = HiddenField("id_real")
    log_text = StringField("log_text", validators=[ InputRequired()])