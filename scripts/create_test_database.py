from dashboards import db, create_app, bcrypt
from dashboards.models import Tracker, Application, Event, User
from datetime import datetime


tracker1 = Tracker(
    name="Testing 2021",
    desc="Testing applications for summer 2022 internships",
    applications=[
        Application(
            application_id="3",
            company_name="Connor's Pizza",
            position_name="DE",
            source="LinkedIn",
            link="https://www.google.com/",
            status="Applied",
            event_history=[
                Event(
                    event_id="5",
                    desc="Rejected",
                    from_me=True,
                    action_necessary=False,
                    date=datetime(2022, 1, 6),
                    of_application="3",
                )
            ],
            of_tracker="fall_2021",
        ),
    ],
)

tracker2 = Tracker(
    name="Testing 2022",
    desc="Testing applications for full-time employment",
    applications=[
        Application(
            application_id="0",
            company_name="Connor's Store",
            position_name="SWE",
            source="Handshake",
            link="https://www.google.com/",
            status="Applied",
            event_history=[
                Event(
                    event_id="1",
                    desc="Applied",
                    from_me=True,
                    action_necessary=False,
                    date=datetime(2021, 12, 5),
                    of_application="0",
                ),
                Event(
                    event_id="2",
                    desc="Rejected",
                    from_me=False,
                    action_necessary=False,
                    date=datetime(2022, 1, 3),
                    of_application="0",
                ),
            ],
            of_tracker="fall_2022",
        ),
        Application(
            application_id="1",
            company_name="Connor's Donuts",
            position_name="SDE",
            source="Other",
            link="https://www.google.com/",
            status="Applied",
            event_history=[
                Event(
                    event_id="7",
                    desc="rejected",
                    from_me=False,
                    action_necessary=False,
                    date=datetime(2020, 10, 4),
                    of_application="1",
                )
            ],
            of_tracker="fall_2022",
        ),
    ],
)

hashed_password = bcrypt.generate_password_hash("password").decode("utf-8")
testUser = User(email="test@gmail.com", password=hashed_password)

app = create_app(True)
with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add(tracker1)
    db.session.add(tracker2)
    db.session.commit()

    User.__table__.drop(db.engine)
    User.__table__.create(db.engine)
    db.session.add(testUser)
    db.session.commit()
