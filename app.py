from flask import Flask
from flask import request

app = Flask(__name__)


@app.post('/registration')
def sign_up():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    first_name = data["first_name"]
    last_name = data["last_name"]
    return {email: password, first_name: last_name}


@app.get('/login')
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    return {email: password}


@app.post('/addAddress')
def add_address():
    data = request.get_json()
    country = data["country"]
    city = data["city"]
    street = data["street"]
    postal_code = data["postcode"]
    return {"Country": country,
            "City": city,
            "Street": street,
            "Postal Code": postal_code
            }


@app.post('/updateAddress')
def update_address():
    data = request.get_json()
    country = data["country"]
    city = data["city"]
    street = data["street"]
    postal_code = data["postcode"]
    unique_id = data["id"]
    return {"Country": country,
            "City": city,
            "Street": street,
            "Postal Code": postal_code,
            "id": unique_id
            }


@app.delete('/deleteAddress/<unique_id>')
def delete_address(unique_id: int):
    return {"id": unique_id}


@app.get('/listAddresses/<unique_id>')
def list_addresses(unique_id: int):
    return {"id": unique_id}


if __name__ == '__main__':
    app.run()
