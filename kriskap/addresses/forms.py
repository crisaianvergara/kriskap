from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired, Length
from kriskap.addresses.utils import search_province, search_municipality


class AddressForm(FlaskForm):
    house = StringField(
        "House/Unit/Flr #, Bldg Name, Blk or Lot #",
        validators=[DataRequired(), Length(min=5, max=200)],
    )
    province = SelectField(
        "Province",
        choices=search_province(),
        validators=[DataRequired()],
    )
    submit = SubmitField("Save")
