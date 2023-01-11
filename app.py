from flask import Flask
from flask import request, jsonify
from schemas import UserSchema, AddressSchema
from database import db, User, create_database
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


app = Flask(__name__)
jwt = JWTManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Nika:mysecretpassword@localhost/main'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret"
db.init_app(app)
with app.app_context():
    create_database()


@app.route('/register', methods=["POST"])
def sign_up():
    data = request.json
    user = UserSchema(**data)
    email = user.email
    password = user.password
    first_name = user.first_name
    last_name = user.last_name

    user = User(email, password, first_name, last_name)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session().rollback()
        return ({"error": "User with this email already exists"}), 400

    return {"message": "User registered successfully"}


@app.route('/login', methods=["GET"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        access_token = create_access_token(identity=email)
        return {"access_token": access_token}, 200

    return {"error": "Invalid email or password"}, 401


@app.route('/address', methods=["POST"])
@jwt_required()
def add_address():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if user:
        data = request.json
        country = data['country']
        city = data['city']
        street = data['street']
        zip_code = data['zip_code']
        user.add_address(country, city, street, zip_code)
        return {"message": "Address added successfully"}, 201
    return {"error": "Invalid User"}, 400


@app.route('/address/<address_id>', methods=["PATCH"])
@jwt_required()
def update_address(address_id: int):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if user:
        data = request.json
        country = data['country']
        city = data['city']
        street = data['street']
        zip_code = data.get('zip_code')
        user.update_address(address_id, country, city, street, zip_code)
        return {"message": "Address updated successfully"}, 200
    return {"error": "Invalid User or Address ID"}, 400


@app.route('/address/<address_id>', methods=["DELETE"])
@jwt_required()
def delete_address(address_id: int):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if user:
        user.delete_address(address_id)
        return {"message": "Address deleted successfully"}, 200
    return {"error": "Invalid User or Address ID"}, 400


@app.route('/address', methods=["GET"])
@jwt_required()
def list_addresses():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if user:
        addresses = user.list_addresses()
        return jsonify([address.to_dict() for address in addresses]), 200
    return {"error": "Invalid User or Address ID"}, 400


if __name__ == '__main__':
    app.run()


