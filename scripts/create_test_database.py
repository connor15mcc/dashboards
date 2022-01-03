from tracker import db
from tracker.models import Tracker, Application, Event
from datetime import datetime

tracker1 = Tracker(
    name_id="fall_2021",
    name="Fall 2021",
    desc="Applications for summer 2022 internships",
    applications=[],
)

tracker2 = Tracker(
    name_id="fall_2022",
    name="Fall 2022",
    desc="Applications for full-time employment",
    applications=[
        Application(
            application_id="0",
            company_name="Connor's Store",
            position_name="SWE",
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
            event_history=[],
            of_tracker="fall_2022",
        ),
    ],
)

db.create_all()
db.session.add(tracker1)
db.session.add(tracker2)
db.session.commit()
