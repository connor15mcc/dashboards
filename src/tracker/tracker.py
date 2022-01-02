from dataclasses import dataclass
from typing import List
from tracker.application import Application


@dataclass(slots=True)
class Tracker:
    name: str
    desc: str
    applications: List[Application]

    def add_application(self, app: Application) -> None:
        self.applications.append(app)
