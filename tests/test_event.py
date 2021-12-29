from tracker.event import Event
import datetime


date1 = datetime.datetime(2020, 5, 17)
date2 = datetime.datetime(2020, 5, 21)


def test_string():
    assert str(Event("test", True, date=date1)) == f"Event: I test on {date1}"
    assert str(Event("tested", False, date=date1)) == f"Event: They tested on {date1}"


def test_ordering():
    assert Event("test", True, date=date1) < Event("applied", False, date=date2)


def test_equality():
    assert Event("applied", True, date=date1) == Event("applied", True, date=date1)
    assert Event("applied", True, date=date1) != Event("applying", True, date=date1)
    assert Event("applied", True, date=date1) != Event("applied", False, date=date1)
    assert Event("applied", True, date=date1) != Event("applied", True, date=date2)
