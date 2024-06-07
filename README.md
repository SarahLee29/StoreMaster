# Introduction

StoreMaster is an application allowing users to manage their stores, such as, list the orders, customers, and products, and do other CRUD operations on them through REST API, like update customer's balance, place an order, etc.

To test it, please run the following commands in sequence:

    python manage.py (this file seeds the database with testing data) or python setup.py (this file just create an empty database)

    FLASK_APP=StoreMaster

    flask run

    if you run manage.py, please signup with the following info and then login:
    
    email: marry123@gmail.com
    name: anything you want
    ps: anything you want 

# Highlights

## Authentication

* Users are allowed to sign up and log in the system. 

* Duplicated users are not allowed.

* Users are allowed to choose if to be remembered, if yes, although they close the browser they don't need to sign in again in a specific time period.

* Different acess permissions are set to different pages based on users login status, that is, being logged in or not. 

## Token-based Authentication

When you test API with a tool like postman, a token is required.

You can get accesse the token follwoing the steps:
1. login the system
2. got to "localhost:5000/token"
3. add a token with the key "x-access-token" and value of what you get in step2 to the request header, in the tool you use, like postman

## Multiple Process Strategies

Users are allowed to choose different process strategies "adjust", "ignore" or "reject" for a specific order

## Row Level Security

Users are only allowed to access their own data.  

RLS is implemented at the application level using SQLAlchemay, without any other third tool, like PostgreSQL. Data access is restricted based on the logged in users.


##  Passwords are hashed in database


# Work with REST API to implement CRUD 

### Send a GET request

* list all customers' in JSON

    `http://localhost:5000/api/customers` 

* list customer details in JSON

    `http://localhost:5000/api/customers/<id>`

* list products in JSON

    `http://localhost:5000/api/products/` 

### Send a POST Request
*  add a new customer
    
    `http://localhost:5000/api/customers`

    Data example: `{"name":"Marry","phone":"000-000-0000"}`

* make an order

    `http://localhost:5000/api/orders`

    Data example: 
    ```
    {"customer_id": 1, 
        "items": [{"name": "onions", "quantity": 2},
                    {"name": "lemon", "quantity": 1},
                    {"name": "chicken breast", "quantity": 1}]}
    ```
* add products

    `http://localhost:5000/api/products`

    Data example: 

    Data example: `{"name":"Pork","price":5.99}`

### Send a PUT Request
*  update a customer's balance

    `http://localhost:5000/api/customers/<id>`

     Data example: `{"balance":10}`

### Send a DELETE Request

*  delete a customer

    `http://localhost:5000/api/customers/<id>`