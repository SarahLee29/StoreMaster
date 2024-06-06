from flask import Blueprint, jsonify, request, url_for
from .. import db
from ..models import Customer

api_customers_bp = Blueprint("api_customers", __name__)

# get customers list in JSON
# prefix:/api/customers


@api_customers_bp.route("/", methods=["GET"])
def customers_json():
    statement = db.select(Customer).order_by(Customer.cid)
    results = db.session.execute(statement)
    customers = []  # output variable
    for customer in results.scalars():
        customers.append(customer.to_json())
    return jsonify(customers)

# create a new customer
# prefix:/api/customers


@api_customers_bp.route("/", methods=["POST"])
def customers_create():
    data = request.json
    if "name" not in data or not isinstance(data["name"], str) or not isinstance(data["phone"], str):
        return "Invalid request", 400
    else:
        customer = Customer(name=data["name"], phone=data["phone"])
        db.session.add(customer)
        db.session.commit()
        return f"Successfully added! The number of customers is {db.session.query(Customer).count()}.", 201

# access a specific customer by customer_id
# prefix:/api/customers


@api_customers_bp.route("/<int:customer_id>", methods=["GET"])
def customer_detail_json(customer_id):
    customer = db.get_or_404(Customer, customer_id,
                             description="The customer id is not found!")
    return customer.to_json()


# delete a specific customer by id
# prefix:/api/customers

@api_customers_bp.route("/<int:customer_id>", methods=["DELETE"])
def customer_delete(customer_id):
    customer = db.get_or_404(Customer, customer_id,
                             description="The customer id is not found!")
    db.session.delete(customer)
    db.session.commit()
    return "", 204


# when a PUT request is made to this URL, the customer_put function will be invoked
# update a customer with balance
# prefix:/api/customers


@api_customers_bp.route("/<int:customer_id>", methods=["PUT"])
def customer_put(customer_id):
    data = request.json
    customer = db.get_or_404(Customer, customer_id,
                             description="The customer id is not found!")
    if "balance" not in data or not isinstance(data["balance"], (float, int)):
        return "Invalid request", 400

    else:
        customer.balance = data["balance"]
        db.session.commit()
        return "", 204
