from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from kriskap import db
from kriskap.models import Product
from kriskap.products.forms import ProductForm, UpdateProductForm
from kriskap.products.utils import save_product_picture
from kriskap.users.utils import admin_only

products = Blueprint("products", __name__)


@products.route("/product")
@login_required
@admin_only
def product():
    form = ProductForm()
    products = Product.query.all()
    return render_template(
        "product.html", title="Products", products=products, form=form
    )


@products.route("/new-product", methods=["GET", "POST"])
@login_required
@admin_only
def new_product():
    products = Product.query.all()
    form = ProductForm()
    if form.validate_on_submit():
        image_f = save_product_picture(form.image_f.data)
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
        "create_product.html", title="Add Products", form=form, products=products
    )


@products.route("/product/<int:product_id>/update", methods=["GET", "POST"])
@login_required
@admin_only
def update_product(product_id):
    form = UpdateProductForm()
    products = Product.query.all()
    product = Product.query.get_or_404(product_id)
    product_name = Product.query.filter_by(name=form.name.data).first()
    if form.validate_on_submit():
        if form.name.data != product.name:
            if product_name:
                flash(
                    "That product name is taken. Please choose different one.", "danger"
                )
                return redirect(url_for("products.product"))
        image_f = save_product_picture(form.image_f.data)
        product.image_file = image_f
        product.name = form.name.data
        product.stock = form.stock.data
        product.price = form.price.data
        db.session.commit()
        flash("Product has been updated.", "success")
        return redirect(url_for("products.product"))
    return render_template(
        "product.html", title="Products", products=products, form=form
    )


@products.route("/product/<int:product_id>/<string:product_name>/delete")
@login_required
@admin_only
def delete_product(product_id, product_name):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash(f"{product_name} has been deleted!", "success")
    return redirect(url_for("products.product"))
