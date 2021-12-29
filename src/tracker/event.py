from dataclasses import dataclass, field
from functools import total_ordering
from datetime import datetime


@dataclass
@total_ordering
class Event:
    action: str
    from_me: bool
    date: datetime = field(default_factory=datetime.today)

    def __str__(self) -> str:
        who = "I" if self.from_me else "They"
        return f"Event: {who} {self.action} on {self.date}"

    def __lt__(self, o: object) -> bool:
        if not isinstance(o, Event):
            return NotImplemented
        return self.date < o.date
