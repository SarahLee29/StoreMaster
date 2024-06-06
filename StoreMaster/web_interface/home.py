from flask import Blueprint, jsonify, redirect, request, render_template, url_for
from .. import db
from ..models import Customer, Product


home_bp = Blueprint("home_html", __name__)


@home_bp.route('/', methods=['GET'])
def home():
    return render_template("home.html")


@home_bp.route("/final/customers-warning", methods=["GET"])
def customer_warning_json():
    statement = db.select(Customer).order_by(Customer.cid)
    results = db.session.execute(statement)
    customers = []  # output variable
    for customer in results.scalars():
        if customer.balance <= 0:
            customer_dict = {"name": customer.name, "balance": customer.balance, "url": url_for(
                "api_customers.customer_detail_json")}
            customers.append(customer_dict)
    return jsonify(customers)


@home_bp.route("/final/out-of-stock", methods=["GET"])
def product_warning_json():
    statement = db.select(Product).order_by(Product.pid)
    results = db.session.execute(statement)
    product_names = []
    for product in results.scalars():
        if product.available == 0:
            product_names.append(product.name)
    return jsonify(product_names)
