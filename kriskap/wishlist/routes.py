from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from kriskap import db
from kriskap.models import Wishlist, Product

wishlists = Blueprint("wishlists", __name__)


@wishlists.route("/wishlist")
@login_required
def wishlist():
    """Route that displays the user's wishlist."""

    wishlists = Wishlist.query.filter_by(buyer_id=current_user.id).all()
    return render_template("wishlist.html", title="Wishlist", wishlists=wishlists)


@wishlists.route("/wishlist/<int:product_id>/add")
@login_required
def add_wishlist(product_id):
    """Route that adds a product to the user's wishlist."""

    # Get the requested product from the database
    requested_product = Product.query.get_or_404(product_id)
    # Check if the product is already in the user's wishlist
    if Wishlist.query.filter_by(
        buyer_id=current_user.id, product_id=product_id
    ).first():
        flash("Product is already on your wishlist.", "info")
        return redirect(url_for("main.home"))
    else:
        # Add the product to the user's wishlist
        new_wishlist = Wishlist(wisher=current_user, parent_product=requested_product)
        db.session.add(new_wishlist)
        db.session.commit()
        flash("Product has been added to your wishlist.", "success")
        return redirect(url_for("main.home"))


@wishlists.route("/wishlist/<int:wishlist_id>/remove")
@login_required
def remove_wishlist(wishlist_id):
    """Route that removes a product from the user's wishlist."""

    # Get the wishlist item from the database
    wishlist = Wishlist.query.get_or_404(wishlist_id)
    # Delete the wishlist item from the database
    db.session.delete(wishlist)
    db.session.commit()
    flash("Product removed from your wishlist.", "success")
    return redirect(url_for("wishlists.wishlist"))
