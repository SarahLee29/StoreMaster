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

if __name__ == "__main__":
    main()
