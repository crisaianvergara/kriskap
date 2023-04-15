from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError, URL
from kriskap.models import Product


class ProductForm(FlaskForm):
    """
    This class defines the product form.

    Fields:
    - stripe_price: A string field for the product's stripe price id.
    - name: A string field for the product's name.
    - stock: A integer field for the product's available stock.
    - price: A float field for the product's price.
    - image_f = A file field for the product's image.
    - submit: A submit field for submitting the form.
    """

    stripe_price = StringField(
        "Price Id", validators=[DataRequired(), Length(min=5, max=60)]
    )
    name = StringField("Name", validators=[DataRequired(), Length(min=5, max=60)])
    stock = IntegerField("Stock")
    price = FloatField("Price")
    image_f = StringField("Image URL", validators=[DataRequired(), URL()])
    submit = SubmitField("Submit")

    def validate_name(self, name):
        """
        Validate that the product name does not already exist in the database.

        Parameters:
        - name: The product name to validate.

        Raises:
        - ValidationError: If the product name already exists in the database.
        """

        product_name = Product.query.filter_by(name=name.data).first()
        if product_name:
            raise ValidationError("That name is taken. Please choose a different one.")

    def validate_stripe_price(self, stripe_price):
        """
        Validate that the product's stripe price id does not already exist in the database.

        Parameters:
        - stripe_price: The product's stripe price id to validate.

        Raises:
        - ValidationError: If the product's stripe price id already exists in the database.
        """
        stripe_price = Product.query.filter_by(stripe_price=stripe_price.data).first()
        if stripe_price:
            raise ValidationError(
                "That stripe price id is taken. Please choose a different one."
            )


class UpdateProductForm(FlaskForm):
    """
    This defines the update product form

    Fields:
    - stripe_price: A string field for the product's new stripe price id.
    - name: A string field for the product's new name.
    - stock: A integer field for the product's new available stock.
    - price: A float field for the product's new price.
    - image_f = A file field for the product's new image.
    - submit: A submit field for submitting the form.
    """

    stripe_price = StringField(
        "Price ID", validators=[DataRequired(), Length(min=5, max=60)]
    )
    name = StringField("Name", validators=[DataRequired(), Length(min=5, max=60)])
    stock = IntegerField("Stock")
    price = FloatField("Price")
    image_f = StringField("Image URL", validators=[DataRequired(), URL()])
    submit = SubmitField("Submit")
