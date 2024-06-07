from flask import Blueprint, jsonify, redirect, request, render_template, url_for
from flask_login import login_required, current_user
from .. import db
from ..models import Order, ProductOrder

orders_bp = Blueprint("orders_html", __name__)

# list orders
# prefix: /orders


@orders_bp.route('/', methods=['GET'])
@login_required
def order_list():
    statement = db.select(Order).order_by(Order.oid)
    records = db.session.execute(statement)
    orders = records.scalars()
    return render_template("order.html", orders=orders,current_user=current_user)


# access a specific order by customer_id
# prefix: /orders
@orders_bp.route('/customer/<int:customer_id>', methods=['GET'])
def order_customer_detail(customer_id):
    statement = db.select(Order).where(Order.customer_id == customer_id)
    records = db.session.execute(statement)
    results = records.scalars()
    return render_template("order.html", orders=results)


# access a specific order by order_id
# prefix: /orders
@orders_bp.route('/order/<int:order_id>', methods=['GET'])
def order_detail(order_id):
    # check an order exits
    order = db.get_or_404(Order, order_id,
                          description="The order is not found!")
    return render_template("order_detail.html", order=order)


# delete an order using the button
# prefix: /orders
@orders_bp.route('/<int:order_id>/delete', methods=['POST'])
def orders_delete(order_id):
    order = db.get_or_404(Order, order_id)
    if not order.processed:
        db.session.delete(order)
        db.session.commit()
    return redirect(url_for("orders_html.order_list"))


# process an order
# prefix: /orders
@orders_bp.route('/<int:order_id>/process', methods=['POST'])
def orders_process(order_id):
    order = db.get_or_404(Order, order_id)
    # print("strategy", request.form.get("strategy"))
    # only when the order has not been processed, a "process" button shows up, so argument passed from
    # web interface is "true (bollean)" by default
    response = order.process_order(True, request.form.get("strategy"))
    db.session.commit()
    if response == True:
        response = "successfully processed!"

    return render_template("process_result.html", response=response)
