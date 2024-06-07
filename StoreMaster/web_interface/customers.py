from flask import Blueprint, jsonify, request, render_template
from .. import db
from ..models import Customer
from flask_login import current_user, login_required, login_user, logout_user

customers_bp = Blueprint("customers_html", __name__)

# list customers
# prefix:/customers

@customers_bp.route("/", methods=["GET"])
@login_required
def customer_list():
    statement = db.select(Customer).order_by(Customer.cid)  # create a query
    records = db.session.execute(statement)  # run the query
    # create an iterable for records containing scalar vaslues
    results = records.scalars()
    return render_template("customer.html", customers=results,current_user=current_user)


# access a specific customer by customer id
# prefix:/customers

@customers_bp.route("/<int:customer_id>", methods=["GET"])
def customer_detail(customer_id):
    customer = db.get_or_404(Customer, customer_id,
                             description="The customer is not found!")
    # another way:
    # statement = db.select(Customer).where(Customer.id == customer_id)
    # result = db.session.execute(statement)
    # record = result.scalar()
    return render_template("customer_detail.html", target_customer=customer)
