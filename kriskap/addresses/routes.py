from flask import Blueprint, redirect, url_for, render_template, jsonify, request
from flask_login import login_required
from kriskap.addresses.forms import AddressForm
from kriskap.addresses.utils import (
    search_municipality,
    search_barangay,
)


addresses = Blueprint("addresses", __name__)


@addresses.route("/address")
@login_required
def address():
    return render_template("address.html", title="Address")


@addresses.route("/address/add", methods=["GET", "POST"])
@login_required
def add_address():
    form = AddressForm()
    return render_template("add_address.html", title="Add Address", form=form)


@addresses.route("/address/search-city", methods=["POST"])
@login_required
def search_city():
    province_code = request.form["province_code"]
    cities = search_municipality(province_code)
    return jsonify({"result": "success", "cities": cities})


@addresses.route("/address/search-barangay", methods=["POST"])
@login_required
def search_home_address():
    city_code = request.form["city_code"]
    barangays = search_barangay(city_code)
    return jsonify({"result": "success", "barangays": barangays})
