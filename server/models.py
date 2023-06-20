from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, UniqueConstraint
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import datetime

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False) #must have a name
    email = db.Column(db.String, nullable=False, unique=True) #must have a unique email

##Customer Relationships:
# - A Customer has many Reservations
    reservations = db.relationship('Reservation', back_populates='customer')

##Customer Association Proxy:
# - A Customer has been to many Locations through Reservations
    locations = association_proxy('reservations', 'location')

##Validations
# - Customer must have a name
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) <1:
            raise ValueError('Customer must have a name')
        return name
# - Customer must have a unique email
    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError('Failed simple email validation')
        return email


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

class Location(db.Model, SerializerMixin):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    max_party_size = db.Column(db.Integer) 

    ##Location relationship:
    # - A Location has many Reservations
    reservations = db.relationship('Reservation', back_populates='location')
    ##Location association proxy:
    # - A Location has many Customers through Reservations
    customers = association_proxy('reservations', 'customer')

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
class Reservation(db.Model, SerializerMixin):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    party_name = db.Column(db.String)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    party_size = db.Column(db.Integer)
    reservation_date = db.Column(db.Date)
##A Reservation belongs to a Customer and a Location
    customer = db.relationship('Customer', back_populates='reservations')
    location = db.relationship('Location', back_populates='reservations')