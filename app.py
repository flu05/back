from flask import Flask
from flask_migrate import Migrate

from blueprints import api_bp
from VeriTabani import *


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://himalayaUser@localhost:5432/himalaya'

    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)

    @app.route('/')
    def index():
        return {"Sunucu": "HİMALAYA"}

    app.register_blueprint(api_bp, url_prefix='/api')

    return app
