from datetime import datetime
from dashboards import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def get_id(self):
        return self.user_id


def __repr__(self):
    return f"User('{self.user_id}', {self.username})'"


class Tracker(db.Model):
    tracker_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    desc = db.Column(db.String, nullable=False)
    applications = db.relationship("Application", backref="tracker", lazy=True)

    def __repr__(self):
        return f"Tracker('{self.name_id}', '{self.desc}')"


class Application(db.Model):
    application_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String, nullable=False)
    position_name = db.Column(db.String, nullable=False)
    source = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)

    coverletter = db.Column(db.String)
    addr1 = db.Column(db.String)
    addr2 = db.Column(db.String)

    notes = db.Column(db.String)

    of_tracker = db.Column(
        db.String, db.ForeignKey("tracker.tracker_id"), nullable=False
    )
    event_history = db.relationship("Event", backref="application", lazy=True)

    def __repr__(self):
        return (
            f"Application('{self.application_id}', '{self.company_name}', "
            f"'{self.position_name}')"
        )


class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String, nullable=False)
    from_me = db.Column(db.Boolean, nullable=False)
    action_necessary = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    of_application = db.Column(
        db.Integer, db.ForeignKey("application.application_id"), nullable=False
    )

    def __repr__(self):
        return f"Event('{self.event_id}', '{self.desc}', '{self.date}')"
