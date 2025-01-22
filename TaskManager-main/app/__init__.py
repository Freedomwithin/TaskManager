import os
import logging
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from logging.config import dictConfig

# Configure logging
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'default'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file', 'console']
    }
})

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_name=None):
    # Create Flask app instance
    app = Flask(__name__, 
                template_folder='templates', 
                static_folder='static')
    
    # Base directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Configuration
    app.config['SECRET_KEY'] = os.urandom(32)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "tasks.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # CSRF Configuration
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for development
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False
    
    # Environment-specific configurations
    if config_name == 'production':
        app.config['DEBUG'] = False
        app.config['WTF_CSRF_ENABLED'] = True  # Enable in production
    else:
        app.config['DEBUG'] = True
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    # Import routes and models within app context
    with app.app_context():
        from .routes import init_routes
        from .models import Task
        
        # Initialize routes
        init_routes(app)
        
        # Create database tables if they don't exist
        db.create_all()
    
    return app

