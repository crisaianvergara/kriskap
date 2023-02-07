from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from kriskap import db
from kriskap.models import Product
from kriskap.products.forms import ProductForm
from kriskap.products.utils import save_profile_picture

products = Blueprint("products", __name__)


@products.route("/new-product", methods=["GET", "POST"])
@login_required
def new_product():
    products = Product.query.all()
    form = ProductForm()
    if form.validate_on_submit():
        image_f = save_profile_picture(form.image_f.data)
        new_product = Product(
            name=form.name.data,
            stock=form.stock.data,
            price=form.price.data,
            image_file=image_f,
        )
        db.session.add(new_product)
        db.session.commit()
        flash("Your product has been created!", "success")
        return redirect(url_for("products.new_product"))
    return render_template(
        "product.html", title="Products", form=form, products=products
    )


@products.route("/product/<int:product_id>/update")
@login_required
def update_product():
    pass


@products.route("/product/<int:product_id>/delete")
@login_required
def delete_product():
    pass
