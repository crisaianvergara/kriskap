from flask import request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import NumberRange


class CartForm(FlaskForm):
    quantity = IntegerField("Quantity", validators=[NumberRange(min=1)])
    submit = SubmitField("Add to Cart")
