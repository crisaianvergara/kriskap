from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired
from kriskap.addresses.utils import search_province


class AddressForm(FlaskForm):
    house = StringField(
        "House/Unit/Flr #, Bldg Name, Blk or Lot #", validators=[DataRequired()]
    )
    city = SelectField("City/Municipality", validators=[DataRequired()])
    province = SelectField(
        "Province", choices=search_province(), validators=[DataRequired()]
    )
    city = SelectField("City/Municipality", validators=[DataRequired()])
    barangay = SelectField("Barangay", validators=[DataRequired()])
    submit = SubmitField("Save")
