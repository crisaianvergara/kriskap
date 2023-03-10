from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired, Length
from kriskap.addresses.utils import search_province


class AddressForm(FlaskForm):
    """
    This class defines the address form.

    Fields:
    - house: A string field for the user's house number.
    - province: A select field for the user's province.
    - submit: A submit field for submitting the form.
    """

    house = StringField(
        "House/Unit/Flr #, Bldg Name, Blk or Lot #",
        validators=[DataRequired(), Length(min=5, max=200)],
    )
    province = SelectField(
        "Province",
        choices=search_province(),
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit", render_kw={"disabled": "disabled"})
