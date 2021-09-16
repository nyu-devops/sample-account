"""
Models for Address

All of the models are stored in this module
"""
from . import logger, db
from .exceptions import DataValidationError
from .persistent_base import PersistentBase


######################################################################
#  A D D R E S S   M O D E L
######################################################################
class Address(PersistentBase, db.Model):
    """
    Class that represents an Address
    """

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    name = db.Column(db.String(64)) # e.g., work, home, vacation, etc.
    street = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(2))
    postalcode = db.Column(db.String(16))

    def __repr__(self):
        return "<Address %r id=[%s] account[%s]>" % (self.name, self.id, self.account_id)

    def __str__(self):
        return "%s: %s, %s, %s %s" % (self.name, self.street, self.city, self.state, self.postalcode)

    def serialize(self):
        """ Serializes a Address into a dictionary """
        return {
            "id": self.id,
            "account_id": self.account_id,
            "name": self.name,
            "street": self.street,
            "city": self.city,
            "state": self.state,
            "postalcode": self.postalcode
        }

    def deserialize(self, data: dict):
        """
        Deserializes a Address from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.account_id = data["account_id"]
            self.name = data["name"]
            self.street = data["street"]
            self.city = data["city"]
            self.state = data["state"]
            self.postalcode = data["postalcode"]
        except KeyError as error:
            raise DataValidationError("Invalid Address: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Account: body of request contained bad or no data " + str(error)
            )
        return self
