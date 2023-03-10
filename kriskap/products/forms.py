from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError
from kriskap.models import Product


class ProductForm(FlaskForm):
    """Create a new product form."""

    stripe_price = StringField(
        "Price Id", validators=[DataRequired(), Length(min=5, max=60)]
    )
    name = StringField("Name", validators=[DataRequired(), Length(min=5, max=60)])
    stock = IntegerField("Stock")
    price = FloatField("Price")
    image_f = FileField(
        "Image",
        validators=[DataRequired(), FileAllowed(["jpg", "png", "jpeg", "webp"])],
    )
    submit = SubmitField("Submit")

    def validate_name(self, name):
        product_name = Product.query.filter_by(name=name.data).first()
        if product_name:
            raise ValidationError("That name is taken. Please choose a different one.")

    def validate_stripe_price(self, stripe_price):
        stripe_price = Product.query.filter_by(stripe_price=stripe_price.data).first()
        if stripe_price:
            raise ValidationError(
                "That stripe price id is taken. Please choose a different one."
            )


class UpdateProductForm(FlaskForm):
    """Create update product form."""

    stripe_price = StringField(
        "Price ID", validators=[DataRequired(), Length(min=5, max=60)]
    )
    name = StringField("Name", validators=[DataRequired(), Length(min=5, max=60)])
    stock = IntegerField("Stock")
    price = FloatField("Price")
    image_f = FileField(
        "Image",
        validators=[DataRequired(), FileAllowed(["jpg", "png", "jpeg", "webp"])],
    )
    submit = SubmitField("Submit")
