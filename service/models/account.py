"""
Models for Account

All of the models are stored in this module
"""
from datetime import datetime
from . import logger, db
from .exceptions import DataValidationError
from .persistent_base import PersistentBase
from .address import Address

DATETIME_FORMAT='%Y-%m-%d %H:%M:%S.%f'

######################################################################
#  A C C O U N T   M O D E L
######################################################################
class Account(db.Model, PersistentBase):
    """
    Class that represents an Account
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    phone_number = db.Column(db.String(32), nullable=True)  # phone is optional
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    addresses = db.relationship('Address', backref='account', lazy=True)  

    def __repr__(self):
        return "<Account %r id=[%s]>" % (self.name, self.id)

    def serialize(self):
        """ Serializes a Account into a dictionary """
        account = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "date_joined": self.date_joined.strftime(DATETIME_FORMAT),
            "addresses": []
        }
        for address in self.addresses:
            account['addresses'].append(address.serialize())
        return account

    def deserialize(self, data: dict):
        """
        Deserializes a Account from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.phone_number = data.get("phone_number")
            self.date_joined = datetime.strptime(data["date_joined"], DATETIME_FORMAT)
            # handle inner list of addresses
            address_list = data.get("addresses")
            for json_address in address_list:
                address = Address()
                address.deserialize(json_address)
                self.addresses.append(address)
        except KeyError as error:
            raise DataValidationError("Invalid Account: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Account: body of request contained bad or no data " + str(error)
            )
        return self

    @classmethod
    def find_by_name(cls, name):
        """ Returns all Accounts with the given name

        Args:
            name (string): the name of the Accounts you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
