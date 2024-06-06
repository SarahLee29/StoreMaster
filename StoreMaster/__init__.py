from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# create a database instance
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # secret_key is used to security session cookie
    app.secret_key = 'thisisseceretkey'
    # This will make Flask use a 'sqlite' database with the filename provided
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///storage.db"
    # This will make Flask store the database file in the path provided
    app.instance_path = Path("./StoreMaster/database").resolve()

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user

        user = User.query.get(int(user_id))
        if user:
            print("find user",user_id)
            return user


    # blueprint for non-auth parts of app
    from .app import app as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api_customers_bp, api_products_bp, api_orders_bp
    app.register_blueprint(api_customers_bp, url_prefix="/api/customers")
    app.register_blueprint(api_products_bp, url_prefix="/api/products")
    app.register_blueprint(api_orders_bp, url_prefix="/api/orders")
    
    from .web_interface import customers_bp, products_bp, orders_bp, home_bp
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(orders_bp, url_prefix="/orders")
    app.register_blueprint(home_bp)

    # blueprint for auth parts of app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app