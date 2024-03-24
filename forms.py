from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, IntegerField
from wtforms.validators import DataRequired, AnyOf, URL, Email

class SpecimenForm(Form):
    animal_id = IntegerField(
        'Animal ID', validators=[DataRequired()]
    )
    institution_id = IntegerField(
        'Institution ID', validators=[DataRequired()]
    )
    sightingdate = DateTimeField(
        'Sighting Date',
        validators=[DataRequired()],
        default=datetime.today()
    )


class AnimalForm(Form):
    genus = StringField(
        'Genus', validators=[DataRequired()]
    )
    species = StringField(
        'Species', validators=[DataRequired()]
    )


class InstitutionForm(Form):
    name = StringField(
        'Name', validators=[DataRequired()]
    )

      
# TODO update schema