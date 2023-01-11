from flask_sqlalchemy import SQLAlchemy
import hashlib
from dataclasses import dataclass

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    addresses = db.relationship("Address", backref="User", lazy=True)

    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password = self.__set_password(password)
        self.first_name = first_name
        self.last_name = last_name

    def __set_password(self, password):
        hashed_password = hashlib.sha256()
        hashed_password.update(password.encode())
        return hashed_password.hexdigest()

    def verify_password(self, password):
        hashed_password = hashlib.sha256()
        hashed_password.update(password.encode())
        return hashed_password.hexdigest() == self.password

    def add_address(self, country, city, street, zip_code):
        address = Address(user_id=self.id, country=country, city=city, street=street, zip_code=zip_code)
        db.session.add(address)
        db.session.commit()

    def update_address(self, address_id, country, city, street, zip_code):
        address = Address.query.filter_by(id=address_id, user_id=self.id).first()
        if address:
            address.country = country
            address.city = city
            address.street = street
            address.zip_code = zip_code
            db.session.commit()

    def delete_address(self, address_id):
        address = Address.query.filter_by(id=address_id, user_id=self.id).first()
        if address:
            db.session.delete(address)
            db.session.commit()

    def list_addresses(self):
        return Address.query.filter_by(user_id=self.id).all()


@dataclass
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    country = db.Column(db.String(255))
    city = db.Column(db.String(255))
    street = db.Column(db.String(255))
    zip_code = db.Column(db.String(255))

    def __init__(self, user_id, country, city, street, zip_code):
        self.user_id = user_id
        self.city = city
        self.country = country
        self.street = street
        self.zip_code = zip_code

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def create_database():
    db.create_all()

