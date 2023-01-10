from pydantic import BaseModel, constr


class UserSchema(BaseModel):
    email: constr(min_length=3, max_length=30)
    password: constr(min_length=3, max_length=20)
    first_name: constr(min_length=1, max_length=50)
    last_name: constr(min_length=1, max_length=50)


class AddressSchema(BaseModel):
    country: str
    city: str
    street: str
    postal_code: str

