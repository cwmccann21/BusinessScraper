from flask import Flask
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__,
                static_folder='../frontend/static',
                template_folder='../frontend/templates')
    
    # Load config
    from .config import Config
    app.config.from_object(Config)
    
    # Initialize extensions
    csrf.init_app(app)
    
    # Register routes
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app 