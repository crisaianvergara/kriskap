from flask import Blueprint, render_template, redirect, url_for, flash
from sqlalchemy import desc
from flask_login import login_required
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
    products = Product.query.order_by(desc("id")).all()
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
        flash("Product has been added!", "success")
        return redirect(url_for("products.product"))
    return render_template(
        "create_product.html", title="New Product", form=form, products=products
    )


@products.route("/product/<int:product_id>/update", methods=["GET", "POST"])
@login_required
@admin_only
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = UpdateProductForm(
        name=product.name,
        stock=product.stock,
        price=product.price,
        image_f=product.image_file,
    )
    if form.validate_on_submit():
        if form.name.data != product.name:
            if Product.query.filter_by(name=form.name.data).first():
                flash(
                    "That product name is taken. Please choose different one.", "danger"
                )
                return redirect(url_for("products.product"))
        if form.image_f.data != product.image_file:
            image_f = save_product_picture(form.image_f.data)
            product.image_file = image_f
        product.name = form.name.data
        product.stock = form.stock.data
        product.price = form.price.data
        db.session.commit()
        flash("Product has been updated.", "success")
        return redirect(url_for("products.product"))
    image_file = url_for("static", filename="img/product_pics/" + product.image_file)
    return render_template(
        "create_product.html",
        title="Update Product",
        product=product,
        form=form,
        image_file=image_file,
        product_id=product_id,
    )


@products.route("/product/<int:product_id>/delete")
@login_required
@admin_only
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash(f"{product.name} has been deleted!", "success")
    return redirect(url_for("products.product"))
