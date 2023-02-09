from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField


class CartForm(FlaskForm):
    quantity = IntegerField("Quantity")
    submit = SubmitField("Add to Cart")
