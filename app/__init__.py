from flask import Flask
from .extensions import db, migrate
from .extensions import login_manager
import pymysql
pymysql.install_as_MySQLdb()
from models.user import User


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    #initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from models.user import User
    from models.donor import Donor
    from models.donor_health import DonorHealth
    from models.bloodbanks import BloodBank
    from models.bloodbanks import BloodStock
    from models.user import BloodRequest

    from routes.auth import auth
    from routes.home import home_bp
    from routes.donor import donor_bp
    from routes.dashboard import dashboard_bp
    from routes.request import request_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(donor_bp, url_prefix='/donor')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(request_bp, url_prefix='/request')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))