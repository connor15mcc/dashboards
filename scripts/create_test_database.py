from tracker import db
from tracker.models import Tracker, Application, Event
from datetime import datetime

tracker1 = Tracker(
    name="Fall 2021",
    desc="Applications for summer 2022 internships",
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
                    desc="rejected",
                    from_me=True,
                    date=datetime.utcnow(),
                    of_application="3",
                )
            ],
            of_tracker="fall_2021",
        ),
    ],
)

tracker2 = Tracker(
    name="Fall 2022",
    desc="Applications for full-time employment",
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
                    desc="applied",
                    from_me=True,
                    date=datetime.utcnow(),
                    of_application="0",
                ),
                Event(
                    event_id="2",
                    desc="rejected",
                    from_me=False,
                    date=datetime.utcnow(),
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
                    date=datetime.utcnow(),
                    of_application="1",
                )
            ],
            of_tracker="fall_2022",
        ),
    ],
)

db.drop_all()
db.create_all()
db.session.add(tracker1)
db.session.add(tracker2)
db.session.commit()
