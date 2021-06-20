# coding=utf-8
"""
extensions
"""
import logging

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)

db = SQLAlchemy(session_options={"autoflush": False})
migrate = Migrate(db=db, directory='migrations')
