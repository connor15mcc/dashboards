from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_breadcrumbs import Breadcrumbs
from flask_scss import Scss
from dashboards.config import Config, ConfigTest


db = SQLAlchemy()


def create_app(testing):
    app = Flask(__name__)
    if testing:
        app.config.from_object(ConfigTest)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    Breadcrumbs(app)
    Scss(app)

    # Importing Blueprints #
    from dashboards.main.routes import main  # noqa: E402
    from dashboards.errors.handlers import errors  # noqa: E402

    # Application Tracker Blueprints
    from dashboards.appTracker.applications.routes import applications  # noqa: E402
    from dashboards.appTracker.events.routes import events  # noqa: E402
    from dashboards.appTracker.trackers.routes import trackers  # noqa: E402
    from dashboards.appTracker.filters.filters import filters  # noqa: E402

    # Account Management Blueprints
    from dashboards.manageAcct.routes import manageAcct  # noqa: E402

    # Registering Blueprints #
    app.register_blueprint(main)
    app.register_blueprint(errors)

    # Application Tracker Blueprints
    app.register_blueprint(applications, url_prefix="/application-tracker/")
    app.register_blueprint(events, url_prefix="/application-tracker/")
    app.register_blueprint(trackers, url_prefix="/application-tracker/")
    app.register_blueprint(filters)

    # Account Management Blueprints
    app.register_blueprint(manageAcct)

    return app
