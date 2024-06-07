from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required,current_user
from .. import db
from ..models import Product

products_bp = Blueprint("products_html", __name__)

# list products
# prefix: /products


@products_bp.route('/', methods=["GET"])
@login_required
def product_list():
    # we need what is shown on website comes from the database
    statement = db.select(Product).order_by(Product.pid)  # create a query
    records = db.session.execute(statement)  # run the query
    results = list(records.scalars())
    return render_template("product.html", products=results,current_user=current_user)
