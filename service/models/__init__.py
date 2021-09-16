"""
Model Package
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

from .account import Account
from .address import Address
from .exceptions import DataValidationError
