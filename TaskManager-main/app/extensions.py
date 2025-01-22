from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()  # Create the SQLAlchemy instance here
migrate = Migrate()
