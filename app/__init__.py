from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# Extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


def create_app():
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static'
    )

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/test_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'secret-key'

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints

    # Frontend (HTML pages) - register first to take precedence
    from app.routes.frontend_routes import frontend_bp
    app.register_blueprint(frontend_bp)  
    # pages => /login , /invoices

    # Auth (JWT Login)
    from app.auth.auth_routes import auth_bp
    app.register_blueprint(auth_bp)  
    # login => POST /login

    # API (Invoices CRUD) - register after frontend with prefix
    from app.routes.invoice_routes import invoice_bp
    app.register_blueprint(invoice_bp, url_prefix='/api')  
    # invoices => /api/invoices (API)

    return app
