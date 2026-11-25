from flask import Flask
from flask_cors import CORS
from sqlalchemy import select

from .config import Config
from .extensions import db
from .routes import health_bp, product_bp, team_bp
from .models import Product, Team, Member


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    # Allow a frontend dev server on another port (e.g. localhost:3001) to call the API.
    CORS(app)

    app.register_blueprint(product_bp, url_prefix="/api/product")
    app.register_blueprint(health_bp, url_prefix="/api/v1")
    app.register_blueprint(team_bp, url_prefix="/api/team")

    return app

def init_db(app):
    with app.app_context():
        db.create_all() # creates all tables based on classes in models.py

        #check if team exists
        cookies = db.session.scalar(
            select(Team).where(Team.name == "Cookies")
        )

        if cookies is None:
            #create team
            cookies = Team(name="Cookies")
            db.session.add(cookies)

            db.session.flush()

            #create team members
            beky = Member(name="Beky", team_id=cookies.id)
            svetla = Member(name="Světla", team_id=cookies.id)
            werca = Member(name="Werča", team_id=cookies.id)

            db.session.add(beky)
            db.session.add(svetla)
            db.session.add(werca)

            db.session.commit()
