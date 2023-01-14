import os
from flask import Flask


def create_app(db):
    """Create and configure the app

    Returns:
        Flask app
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.postgresql'),
        SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123456@localhost:5432/AutomobileCompany"
    )

    # create database
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register blueprints
    from . import auth, customer, marketing, dealer
    app.register_blueprint(auth.bp)
    app.register_blueprint(customer.bp)
    app.register_blueprint(marketing.bp)
    app.register_blueprint(dealer.bp)

    app.add_url_rule("/", endpoint="index")

    return app