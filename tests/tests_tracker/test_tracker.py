from tracker.tracker import Tracker


def test_construction():
    assert Tracker("Summer 2022", []).name == "Summer 2022"
    assert len(Tracker("Summer 2022", []).applications) == 0
