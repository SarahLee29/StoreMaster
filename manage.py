import random
from StoreMaster import db, create_app
# from .app import app
from StoreMaster.models import  Customer, Product, Order, ProductOrder
import csv
from sqlalchemy.sql import functions as func

app=create_app()

def main():
    # the following operation for database is not in request-response context,
    # so create a context in which the Flask application app is accessible
    # inside which block interact with app
    with app.app_context():
        db.drop_all()
        db.create_all()

        with open('data/customers.csv', newline='') as cusfile:
            customers_csv = csv.DictReader(cusfile)  # a list of dictionaries
            for customer in customers_csv:
                customer_instance = Customer(
                    # create objects to store in the database
                    name=customer["name"], phone=customer["phone"],owner=customer["owner"])
                db.session.add(customer_instance)

        with open('data/products_only.csv', newline='') as profile:
            products_csv = csv.DictReader(profile)
            for product in products_csv:
                product_instance = Product(
                    name=product["name"], price=product["price"],owner=product["owner"])
                db.session.add(product_instance)

        # with open('data/products.csv', newline='') as profile:
        #     cat_csv = csv.DictReader(profile)
        #     for cat in cat_csv:
        #         cat_instance = Category(
        #             name=cat["name"], price=cat["price"], category=cat["category"])
        #         db.session.add(cat_instance)


# ================ randomly create orders =====================
        # customers = []
        # orders = []
        # products = []
        # items = []
        # for i in range(1, 11):
        #     # Find a random customer
        #     cust_stmt = db.select(Customer).order_by(func.random()).limit(1)
        #     rand_customer = db.session.execute(cust_stmt).scalar()
        #     customers.append(rand_customer)
        #     # Make an order
        #     rand_order = Order(customer=rand_customer)
        #     orders.append(rand_order)
        #     db.session.add(rand_order)
        #     # Find a random product
        #     prod_stmt = db.select(Product).order_by(func.random()).limit(1)
        #     rand_product_1 = db.session.execute(prod_stmt).scalar()
        #     # Find a random quantity
        #     rand_qty_1 = random.randint(10, 20)
        #     # make a record
        #     rand_record_1 = ProductOrder(
        #         order=rand_order, product=rand_product_1, quantity=rand_qty_1)
        #     db.session.add(rand_record_1)

        #     prod_stmt = db.select(Product).order_by(func.random()).limit(1)
        #     rand_product_2 = db.session.execute(prod_stmt).scalar()
        #     products.append(rand_product_1)
        #     products.append(rand_product_2)
        #     rand_qty_2 = random.randint(10, 20)
        #     rand_record_2 = ProductOrder(
        #         order=rand_order, product=rand_product_2, quantity=rand_qty_2)
        #     items.append(rand_record_1)
        #     items.append(rand_record_2)
        #     db.session.add(rand_record_2)

        db.session.commit()


# ============= to check if the models are all set correctly ==============
        # for c in customers:
        #     print(c.orders)
        # for o in orders:
        #     print(o.customer)
        #     print(o.records)
        #     print(o.records[0].product.name)
        #     print(o.records[0].quantity)
        #     print(o.records[0].order.customer_id)
        # print(products)
        # print(items)
        # for product in products:
        #     print(product.price)
        # print(o.estimate_total(products, items))
        # print(products)
        # print(items)
        # orders[0].estimate_total(items)


# =======or check in Sqlite editor with "PRAGMA foreign_key_list("product_order");"


if __name__ == "__main__":
    main()
