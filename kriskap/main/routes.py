from flask import render_template, Blueprint

main = Blueprint("main", __name__)


products = [
    {
        "product_image": "https://cdn.shopify.com/s/files/1/0500/2867/5227/products/1000393592-01_f6fda8cd-5ce4-4770-ba8d-c96c9a9fade8_1024x1024@2x.jpg?v=1647226526",
        "product_name": "Elite Flex Cap Head Gear",
        "product_price": "1,791.00",
    },
    {
        "product_image": "https://cdn.shopify.com/s/files/1/0500/2867/5227/products/1000393582-01_1024x1024@2x.jpg?v=1647226415",
        "product_name": "Badger2snap Head Gear",
        "product_price": "1,611.00",
    },
    {
        "product_image": "https://cdn.shopify.com/s/files/1/0500/2867/5227/products/1000393585-01_1024x1024@2x.jpg?v=1657074187",
        "product_name": "Cap Star 3d Head Gear Black",
        "product_price": "1,611.00",
    },
    {
        "product_image": "https://cdn.shopify.com/s/files/1/0500/2867/5227/products/1000393587-01_49730c4d-12cc-4a65-9502-e1bb8198af7c_1024x1024@2x.jpg?v=1647226481",
        "product_name": "Cap Star 3d Head Gear White",
        "product_price": "1,611.00",
    },
    {
        "product_image": "https://cdn.shopify.com/s/files/1/0500/2867/5227/products/1000398652-01_1024x1024@2x.jpg?v=1657074117",
        "product_name": "Haze Snapback Black",
        "product_price": "1,611.00",
    },
    {
        "product_image": "https://cdn.shopify.com/s/files/1/0500/2867/5227/products/1000398653-01_ab919585-8235-4872-96d4-607fd3e99de0_1024x1024@2x.jpg?v=1653976632",
        "product_name": "Haze Snapback Brown",
        "product_price": "1,611.00",
    },
]


@main.route("/home")
@main.route("/")
def home():
    return render_template("index.html", products=products)
