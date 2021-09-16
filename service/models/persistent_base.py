"""
Persistent Base Class

All of the models should subclass this base class
"""
from . import logger, db
from .exceptions import DataValidationError

######################################################################
#  P E R S I S T E N T   B A S E   M O D E L
######################################################################
class PersistentBase():
    """ Base class added persistent methods """

    # @abstractmethod
    # def serialize(self):
    #     """ Serialize an object to a dictionary """
    #     pass

    # @abstractmethod
    # def deserialize(self, data: dict):
    #     """ Deserialize a dictionary to an object """
    #     pass

    def create(self):
        """
        Creates a Account to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a Account to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a Account from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the records in the database """
        logger.info("Processing all records")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a record by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a record by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

