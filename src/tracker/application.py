#! /usr/bin/env python
from functools import total_ordering
from typing import List
from tracker.event import Event


@total_ordering
class Application:
    # application_id: int
    # company_name: str
    # position: str

    # source: str
    # link: str  # or do we want to track linkedin vs handshake etc (ie source)
    # position_type: str
    # status: str
    # application_history: str

    __slots__ = (
        "_application_id",
        "_company_name",
        "_position",
        "_source",
        "_link",
        "_position_type",
        "_status",
        "_application_history",
    )

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

    @property
    def application_id(self):
        return self._application_id

    @application_id.setter
    def application_id(self, aid: int):
        self._application_id = aid

    @property
    def company_name(self):
        return self._company_name

    @company_name.setter
    def company_name(self, cname: str):
        self._company_name = cname

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, pos: str):
        self._position = pos

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, src: str):
        if (src not in ["Linkedin", "Handshake", "Indeed", "Career Fair"]) and (
            "Other:" not in src
        ):
            raise ValueError("This isn't a proper source")
        self._source = src

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, lnk: str):
        self._link = lnk

    @property
    def position_type(self):
        return self._position_type

    @position_type.setter
    def position_type(self, ptype: str):
        self._position_type = ptype

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, sts: str):
        if sts in ["Applied", "Accepted", "Rejected"]:
            self._status = sts
        else:
            raise ValueError("This isn't a valid status")

    @property
    def application_history(self):
        return self._application_history

    @application_history.setter
    def application_history(self, ahist: List[Event]):
        self._application_history = ahist
