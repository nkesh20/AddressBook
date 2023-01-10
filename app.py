from flask import Flask
from flask import request
from schemas import UserSchema, AddressSchema
from flask_pydantic import validate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))


session = db.session

with app.app_context():
    db.create_all()


@app.post('/register')
@validate()
def sign_up():
    data = request.json
    user = UserSchema(**data)
    email = user.email
    password = user.password
    first_name = user.first_name
    last_name = user.last_name
    return {email: password, first_name: last_name}


@app.get('/login')
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    return {email: password}


@app.post('/addAddress')
@validate()
def add_address():
    data = request.json
    address = AddressSchema(**data)
    country = address.country
    city = address.city
    street = address.street
    postal_code = address.postal_code
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


