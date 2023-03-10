from flask import Blueprint, render_template, request
from sqlalchemy import desc
from kriskap.models import Product

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    """Route for displaying all products with pagination."""

    page = request.args.get("page", 1, type=int)
    products = Product.query.order_by(desc("id")).paginate(page=page, per_page=12)
    return render_template("index.html", products=products)
