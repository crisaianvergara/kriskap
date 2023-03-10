from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import NumberRange


class CartForm(FlaskForm):
    """
    This class defines the cart form.

    Fields:
    - quantity: A integer field that counts the number of items of the user's want to buy.
    - submit: A submit field for submitting the form.
    """

    quantity = IntegerField("Quantity", validators=[NumberRange(min=1)])
    submit = SubmitField("Add to Cart")
