from flask import Blueprint, redirect, url_for, render_template, jsonify, request, flash
from flask_login import login_required, current_user
from kriskap.addresses.forms import AddressForm
from kriskap.addresses.utils import (
    search_municipality,
    search_barangay,
    search_province,
)
from kriskap import db
from kriskap.models import Address


addresses = Blueprint("addresses", __name__)


@addresses.route("/address")
@login_required
def address():
    """Route for displaying addresses of the current user."""

    addresses = (
        Address.query.filter_by(buyer_id=current_user.id)
        .order_by(Address.default)
        .all()
    )
    return render_template("address.html", title="Address", addresses=addresses)


@addresses.route("/address/add", methods=["GET", "POST"])
@login_required
def add_address():
    """Route for adding new delivery addresses for the current user."""

    form = AddressForm()
    # If the user has an existing address, the new address is not set as the default.
    # Otherwise, the new address is set as the default.
    if Address.query.filter_by(buyer_id=current_user.id).first():
        default = "not_default"
    else:
        default = "default"
    if form.validate_on_submit():
        cities = search_municipality(request.form["province"])
        barangays = search_barangay(request.form["city"])
        new_address = Address(
            default=default,
            buyer=current_user,
            house=form.house.data,
            province=dict(search_province()).get(form.province.data),
            city=dict(cities).get(request.form["city"]),
            barangay=dict(barangays).get(request.form["barangay"]),
        )
        db.session.add(new_address)
        db.session.commit()
        flash("Delivery address added successfully", "success")
        return redirect(url_for("addresses.address"))
    return render_template("add_address.html", title="Add Address", form=form)


@addresses.route("/address/<int:address_id>/edit", methods=["GET", "POST"])
@login_required
def edit_address(address_id):
    """Route for editing an existing delivery address for the current user."""

    address = Address.query.get_or_404(address_id)
    form = AddressForm(house=address.house)
    if form.validate_on_submit():
        cities = search_municipality(request.form["province"])
        barangays = search_barangay(request.form["city"])
        address.house = form.house.data
        address.province = dict(search_province()).get(form.province.data)
        address.city = dict(cities).get(request.form["city"])
        address.barangay = dict(barangays).get(request.form["barangay"])
        db.session.commit()
        flash("Address edited successfully.", "success")
        return redirect(url_for("addresses.address"))
    return render_template(
        "add_address.html", title="Edit Address", address_id=address_id, form=form
    )


@addresses.route("/address/<int:address_id>/delete")
@login_required
def delete_address(address_id):
    """Route for deleting an existing delivery address for the current user."""

    address = Address.query.get_or_404(address_id)
    db.session.delete(address)
    db.session.commit()
    flash("Address deleted.", "success")
    return redirect(url_for("addresses.address"))


@addresses.route("/address/<int:address_id>/default_address")
@login_required
def default_address(address_id):
    """Set a specific address as the default address for the current user."""

    address = Address.query.get_or_404(address_id)
    # Find any existing default addresses for the user.
    is_exist = Address.query.filter_by(
        buyer_id=current_user.id, default="default"
    ).first()
    # If there's an existing default address, set it to not default.
    if is_exist:
        is_exist.default = "not_default"
        db.session.commit()

    # Set the specified address as the default address.
    address.default = "default"
    db.session.commit()
    return redirect(url_for("addresses.address"))


@addresses.route("/address/search-city", methods=["POST"])
@login_required
def search_city():
    """AJAX request to search for a cities/municipalities."""

    province_code = request.form["province_code"]
    cities = search_municipality(province_code)
    return jsonify({"result": "success", "cities": cities})


@addresses.route("/address/search-barangay", methods=["POST"])
@login_required
def search_home_address():
    """AJAX request to search for barangays."""

    city_code = request.form["city_code"]
    barangays = search_barangay(city_code)
    return jsonify({"result": "success", "barangays": barangays})
