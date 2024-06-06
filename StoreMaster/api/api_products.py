from flask import Blueprint, jsonify, request
from .. import db
from ..models import Product

api_products_bp = Blueprint("api_products", __name__)

# show product list in JSON
# prefix: /api/products


@api_products_bp.route("/", methods=["GET"])
def products_json():
    statement = db.select(Product).order_by(Product.pid)
    results = db.session.execute(statement)
    products = []
    for product in results.scalars():
        products.append(product.to_json())
    return jsonify(products)


# show a specific product in JSON
# prefix: /api/products


@api_products_bp.route("/<int:product_id>", methods=["GET"])
def product_detail_json(product_id):
    # check the product exits
    product = db.get_or_404(Product, product_id,
                            description="The product id is not found!")
    # another way
    # statement = db.select(product).where(product.id == product_id)
    # result = db.session.execute(statement)
    # product = result.scalar()
    return product.to_json()


# create new products
# prefix: /api/products

@api_products_bp.route("/", methods=["POST"])
def products_create():
    data = request.json
    if "name" not in data or "price" not in data or not isinstance(data["name"], str) or not isinstance(data["price"], (int, float)) or (data["price"] <= 0):
        return "Invalid request", 400
    else:
        product = Product(name=data["name"], price=data["price"])
        db.session.add(product)
        db.session.commit()
        return f"Successfully added! The number of products is {db.session.query(Product).count()}.", 201


# update a specific product's name, price or available
# prefix: /api/products


@api_products_bp.route("/<int:product_id>", methods=["PUT"])
def product_put(product_id):
    data = request.json
    product = db.get_or_404(Product, product_id,
                            description="The product id is not found!")
    if "name" not in data or not isinstance(data["name"], str):
        return "Invalid request", 400
    else:
        product.name = data["name"]
        if "price" in data and isinstance(data["price"], (float, int)) and data["price"] > 0:
            product.price = data["price"]
        if "available" in data and isinstance(data["available"], int) and data["available"] >= 0:
            product.available = data["available"]
        db.session.commit()
        return "", 204


# delete a specific product's name, price or available
# prefix: /api/products


@api_products_bp.route("/<int:product_id>", methods=["DELETE"])
def product_delete(product_id):
    product = db.get_or_404(Product, product_id,
                            description="The product id is not found!")
    db.session.delete(product)
    db.session.commit()
    return "", 204


@api_products_bp.route("/final/warning", methods=["POST"])
def products_final_waring_json():
    statement = db.select(Product).order_by(Product.pid)
    results = db.session.execute(statement)
    products = []
    data = request.json
    for product in results.scalars():
        if product.available < data["threshold"]:
            product_dict = {"name": product.name,
                            "available": product.available}
            products.append(product_dict)

    return product.warning_json(data["threshold"], products)
