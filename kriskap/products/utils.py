import os
import secrets
from flask import current_app
from PIL import Image


def save_product_picture(form_picture):
    """
    Save a product picture uploaded by a user to the static/img/product_pics directory.

    Generates a unique filename for the picture by combining a random hex string
    with the file extension of the uploaded picture. The picture is then resized
    to a maximum size of 360x360 pixels using the Pillow library. The resized
    picture is saved to the static/img/product_pics directory and the filename
    is returned.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, "static/img/product_pics", picture_fn
    )
    output_size = (360, 360)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
