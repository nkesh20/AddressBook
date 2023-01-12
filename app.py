from flask import Flask
from flask import request, jsonify
from schemas import UserSchema, AddressSchema, LoginSchema
from database import db, User, create_database
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, create_refresh_token


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
    raw_data = request.json
    data = UserSchema(**raw_data)
    user = User(**raw_data)
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session().rollback()
        return ({"error": "User with this email already exists"}), 400

    return {"message": "User registered successfully"}


@app.route('/login', methods=["GET"])
def login():
    login_data = LoginSchema(**request.json)
    email = login_data.email
    password = login_data.password
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        return {"access_token": access_token,
                "refresh_token": refresh_token}, 200

    return {"error": "Invalid email or password"}, 401


@app.route('/address', methods=["POST"])
@jwt_required()
def add_address():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if user:
        data = request.json
        address = AddressSchema(**data)
        user.add_address(**data)
        return {"message": "Address added successfully"}, 201
    return {"error": "Invalid User"}, 400


@app.route('/address/<address_id>', methods=["PATCH"])
@jwt_required()
def update_address(address_id: int):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if user:
        data = request.json
        address = AddressSchema(**data)
        user.update_address(address_id, **data)
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


