#! /usr/bin/env python
from functools import total_ordering


@total_ordering
class Application:
    # application_id: int
    # company_name: str
    # position: str

    # link: str  # or do we want to track linkedin vs handshake etc (ie source)
    # position_type: str
    # status: str
    # application_history: str
    # related_contacts: str

    def __init__(self, a_id: int, c_name: str, pos: str) -> None:
        self.application_id = a_id
        self.company_name = c_name
        self.position = pos

    def __repr__(self) -> str:
        return (
            f"Application({self.application_id}, {self.company_name}, {self.position})"
        )  # type: ignore

    def __str__(self) -> str:
        return (
            f"Application #{self.application_id} "
            f"at {self.company_name} for the {self.position} position"
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Application):
            return NotImplemented
        return (
            self.application_id == o.application_id
            and self.company_name == o.company_name
            and self.position == o.position
        )

    def __hash__(self) -> int:
        return hash((self.application_id, self.company_name, self.position))

    def __lt__(self, o: object) -> bool:
        pass
