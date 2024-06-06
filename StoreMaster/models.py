import datetime
from sqlalchemy import  Float, Numeric, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import mapped_column, relationship
from . import db
from decimal import Decimal
from flask_login import UserMixin


# define a SQLAlchemy model named Customer
class Customer(db.Model):
    __tablename__ = 'customer'
    cid = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False, unique=True)
    phone = mapped_column(String(20), nullable=False)
    balance = mapped_column(Numeric(10, 2), nullable=False, default=200)
    owner= mapped_column(String(200),nullable=False,default="null")
    orders = relationship("Order", back_populates="customer",
                          cascade="all, delete")

    def to_json(self):
        return {
            "id": self.cid,
            "name": self.name,
            "phone": self.phone,
            "balance": self.balance,
        }

    def __repr__(self):
        return f"Customer {self.name}"


class Product(db.Model):
    pid = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False, unique=True)
    price = mapped_column(Float, nullable=False)
    available = mapped_column(Integer, nullable=False, default=500)
    records = relationship("ProductOrder", back_populates="product",
                           cascade="all, delete")

    def to_json(self):
        return {
            "id": self.pid,
            "name": self.name,
            "price": self.price,
            "available": self.available,
        }

    # return a string representation of the object
    def __repr__(self):
        return f"Product {self.name}"

    def warning_json(self, threshold, products):
        return {
            "threshold": threshold,
            "products": products
        }


class Order(db.Model):

    oid = mapped_column(Integer, primary_key=True)
    customer_id = mapped_column(
        Integer, ForeignKey("customer.cid", ondelete="CASCADE"), nullable=False)
    total = mapped_column(Numeric(10, 2), nullable=True)
    created = mapped_column(DateTime, nullable=False,
                            default=datetime.datetime.now())
    processed = mapped_column(DateTime, nullable=True)
    customer = relationship(
        "Customer", back_populates="orders")
    records = relationship(
        "ProductOrder", back_populates="order", cascade="all, delete")

    # ================ calculate estimate total but don't change total until the order is processed
    def estimate_total(self):
        estimate_total = 0
        for item in self.records:
            estimate_total += item.product.price*item.quantity
        return round(estimate_total, 2)

    # =================process an order=================
    def process_order(self, process, strategy):
        # check if this order is processed
        if self.processed:
            return "This order has already been processed!"
        if not process:
            return "This order cannot be processed!"
        # check if the balance is <=0
        if not isinstance(process, bool):
            return "The process type is not correct, please input true or false!"
        if self.customer.balance <= 0:
            return "The customer's balance is less than or equal to 0 !"
        # check if strategy is correct
        if strategy not in ("adjust", "ignore", "reject"):
            return "The strategy is not correct."

        order_price = 0
        # as long as "reject" is selected, no matter what the other products' situations are, the order is rejected
        for record in self.records:
            if record.quantity > record.product.available and strategy == "reject":
                return "The customer rejects to continute process this order."
        # check other two strategies
        for record in self.records:
            if record.quantity > record.product.available:
                if strategy == "adjust":
                    record.quantity = record.product.available
                elif strategy == "ignore":
                    record.quantity = 0
            record.product.available -= record.quantity
            record_price = record.product.price*record.quantity
            order_price += record_price

        self.total = order_price
        self.customer.balance -= Decimal(order_price)
        self.processed = datetime.datetime.now()

        return True


class ProductOrder(db.Model):
    iid = mapped_column(Integer, primary_key=True, nullable=False)
    order_id = mapped_column(Integer, ForeignKey(
        "order.oid", ondelete="CASCADE"), nullable=False)
    product_id = mapped_column(Integer, ForeignKey(
        "product.pid", ondelete="CASCADE"), nullable=False)
    quantity = mapped_column(Integer, nullable=False)
    order = relationship("Order", back_populates="records")

    product = relationship("Product", back_populates="records")



class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
