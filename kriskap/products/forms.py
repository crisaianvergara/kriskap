from flask import request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from kriskap.models import Product


class ProductForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=5, max=60)])
    stock = IntegerField("Stock", validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])
    image_f = FileField(
        "Image",
        validators=[DataRequired(), FileAllowed(["jpg", "png", "jpeg", "webp"])],
    )
    submit = SubmitField("Submit")

    def validate_name(self, name):
        product_name = Product.query.filter_by(name=name.data).first()
        if product_name:
            raise ValidationError("That name is taken. Please choose a different one.")


class UpdateProductForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=5, max=60)])
    stock = IntegerField("Stock", validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])
    image_f = FileField(
        "Image",
        validators=[DataRequired(), FileAllowed(["jpg", "png", "jpeg", "webp"])],
    )
    submit = SubmitField("Submit")