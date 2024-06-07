from flask import Blueprint, jsonify, request

from ..utils import token_required
from .. import db
from ..models import Product

api_products_bp = Blueprint("api_products", __name__)

# show product list in JSON
# prefix: /api/products


@api_products_bp.route("/", methods=["GET"])
@token_required
def products_json(current_user):
    statement = db.select(Product).order_by(Product.pid)
    results = db.session.execute(statement)
    products = []
    for product in results.scalars():
        if current_user.email==product.owner:
            products.append(product.to_json())
    return jsonify(products)


# show a specific product in JSON
# prefix: /api/products


@api_products_bp.route("/<int:product_id>", methods=["GET"])
@token_required
def product_detail_json(current_user,product_id):
    # check the product exits
    product = db.get_or_404(Product, product_id,
                            description="The product id is not found!")
    if current_user.email==product.owner:
        return product.to_json()
    return "You don't have this product!"


# create new products
# prefix: /api/products

@api_products_bp.route("/", methods=["POST"])
@token_required
def products_create(current_user):
    data = request.json
    if "name" not in data or "price" not in data or not isinstance(data["name"], str) or not isinstance(data["price"], (int, float)) or (data["price"] <= 0):
        return "Invalid request", 400
    else:
        product = Product(name=data["name"], price=data["price"],owner=current_user.email)
        db.session.add(product)
        db.session.commit()
        return f"Successfully added! The number of products is {db.session.query(Product).count()}.", 201


# update a specific product's name, price or available
# prefix: /api/products


@api_products_bp.route("/<int:product_id>", methods=["PUT"])
@token_required
def product_put(current_user,product_id):
    data = request.json
    product = db.get_or_404(Product, product_id,
                            description="The product id is not found!")
    if "name" not in data or not isinstance(data["name"], str):
        return "Invalid request", 400
    else:
        if current_user.email==product.owner:
            product.name = data["name"]
            if "price" in data and isinstance(data["price"], (float, int)) and data["price"] > 0:
                product.price = data["price"]
            if "available" in data and isinstance(data["available"], int) and data["available"] >= 0:
                product.available = data["available"]
            db.session.commit()
            return "", 204
        return "You don't have this product!"


# delete a specific product's name, price or available
# prefix: /api/products


@api_products_bp.route("/<int:product_id>", methods=["DELETE"])
@token_required
def product_delete(current_user,product_id):
    product = db.get_or_404(Product, product_id,
                            description="The product id is not found!")
    if current_user.email==product.owner:
        db.session.delete(product)
        db.session.commit()
        return "", 204
    return "You don't have this product!"


@api_products_bp.route("/final/warning", methods=["POST"])
@token_required
def products_final_waring_json(current_user):
    statement = db.select(Product).order_by(Product.pid)
    results = db.session.execute(statement)
    products = []
    data = request.json
    for product in results.scalars():
        if current_user.email==product.owner:
            if product.available < data["threshold"]:
                product_dict = {"name": product.name,
                                "available": product.available}
                products.append(product_dict)

    return product.warning_json(data["threshold"], products)
