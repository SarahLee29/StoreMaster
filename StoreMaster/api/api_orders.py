from flask import Blueprint, jsonify, request
from .. import db
from ..models import Order, Customer, ProductOrder, Product

api_orders_bp = Blueprint("api_orders", __name__)

# create an order with customer_id and at least one item with name and quantity
# prefix: /api/orders


@api_orders_bp.route('/', methods=['POST'])
def orders_create():
    data = request.json
    # got error??????????????
    # cust = db.get_or_404(Customer, data["customer_id"])

    # check if the customer exits
    if not db.session.execute(db.select(Customer).where(Customer.cid == data["customer_id"])).scalar():
        return "Cannot find this customer!", 404

    # check if the product exits
    for item in data["items"]:
        if not db.session.execute(db.select(Product).where(Product.name == item["name"])).scalar():
            return f"Cannot find the product: {item["name"]}", 404

    # check data format
    if "customer_id" not in data or "items" not in data or len(data["items"]) < 1 or not any("name" in item for item in data["items"]) or not any("quantity" in item for item in data["items"]) or len([item for item in data["items"] if item["quantity"] <= 0]) > 0:
        return "Invalid request", 400

    else:
        order = Order(customer_id=data["customer_id"])
        db.session.add(order)
        for item in data["items"]:
            product = db.session.execute(db.select(Product).where(
                Product.name == item["name"])).scalar()
            product_order = ProductOrder(
                order_id=order.oid, product_id=product.pid, quantity=item["quantity"])
            db.session.add(product_order)
        db.session.commit()
        return f"Successfully added! The number of orders is {db.session.query(Order).count()}.", 201

# process an order with id
# prefix: /api/orders


@api_orders_bp.route('/<int:order_id>', methods=['PUT'])
def order_process(order_id):
    data = request.json
    if "process" not in data:
        return "Invalid request, must provide 'process'", 400
    order = db.get_or_404(Order, order_id)
    # list comprehension
    # if no strategy is provided in request, the strategy will be set to "adjust"
    strategy = data["strategy"] if "strategy" in data else "adjust"
    response = order.process_order(data["process"], strategy)
    db.session.commit()
    if response == True:
        return "successfully processed!"
    else:
        return response
