# Introduction

StoreMaster is an application allowing users to manage their stores, such as, list the orders, customers, and products, and modify them.

To test it, please run the following commands in sequence:

    python manage.py

    FLASK_APP=project

    flask run

# Highlights

## UI/UX design

### Authentication

* Users are allowed to sign up and log in the system. 

* Duplicated users are not allowed.

* Users are allowed to choose if to be remembered, if yes, although they close the browser they don't need to sign in again in a specific time period.

* Different acess permissions are set to different pages based on users login status, that is, being logged in or not. 


### Multiple Process Strategies

Users are allowed to choose different process strategies "adjust", "ignore" or "reject" for a specific order

## Security Consideration

###  Passwords are hashed.


## Work with REST API to implement CRUD 

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

### Send a PUT Request
*  update a customer's balance

    `http://localhost:5000/api/customers/<id>`

     Data example: `{"balance":10}`

### Send a DELETE Request

*  delete a customer

    `http://localhost:5000/api/customers/<id>`