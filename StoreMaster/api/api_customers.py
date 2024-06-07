from flask import Blueprint, jsonify, request, session, url_for
from .. import db
from ..models import Customer
from flask_login import current_user,login_required
from ..utils import token_required

api_customers_bp = Blueprint("api_customers", __name__)

# get customers list in JSON
# prefix:/api/customers


@api_customers_bp.route("/", methods=["GET"])
@token_required
def customers_json(current_user):
    statement = db.select(Customer).order_by(Customer.cid)
    results = db.session.execute(statement)
    customers = []  # output variable
    for customer in results.scalars():
        if current_user.email==customer.owner:
            customers.append(customer.to_json())
    return jsonify(customers)

# create a new customer
# prefix:/api/customers


@api_customers_bp.route("/", methods=["POST"])
@token_required
def customers_create(current_user):
    try:
        data = request.json
        if "name" not in data or not isinstance(data["name"], str) or not isinstance(data["phone"], str):
            return "Invalid request", 400
        else:
            customer = Customer(name=data["name"], phone=data["phone"],owner=current_user.email)
            db.session.add(customer)
            db.session.commit()
            return "Successfully added!", 201
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred", 500

# access a specific customer by customer_id
# prefix:/api/customers


@api_customers_bp.route("/<int:customer_id>", methods=["GET"])
@token_required
def customer_detail_json(current_user,customer_id):
    customer = db.get_or_404(Customer, customer_id,
                             description="The customer id is not found!")
    if current_user.email==customer.owner:
        return customer.to_json()
    return "You don't have this customer!"

# delete a specific customer by id
# prefix:/api/customers

@api_customers_bp.route("/<int:customer_id>", methods=["DELETE"])
@token_required
def customer_delete(current_user,customer_id):
    customer = db.get_or_404(Customer, customer_id,
                             description="The customer id is not found!")
    if current_user.email==customer.owner:
        db.session.delete(customer)
        db.session.commit()
        return "", 204
    return "You don't have this customer!"


# when a PUT request is made to this URL, the customer_put function will be invoked
# update a customer with balance
# prefix:/api/customers


@api_customers_bp.route("/<int:customer_id>", methods=["PUT"])
@token_required
def customer_put(current_user,customer_id):
    data = request.json
    customer = db.get_or_404(Customer, customer_id,
                             description="The customer id is not found!")
    if "balance" not in data or not isinstance(data["balance"], (float, int)):
        return "Invalid request", 400

    else:
        if current_user.email==customer.owner:
            customer.balance = data["balance"]
            db.session.commit()
            return "", 204
        return "You don't have this customer!"