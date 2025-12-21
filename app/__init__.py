from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'mysql+pymysql://root:@localhost/test_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'secret-key'

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from app.auth.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
