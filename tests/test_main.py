from tracker.main import pickle_trackers, unpickle_trackers
from tracker.tracker import Tracker, Application


def test_pickling():
    tracker1 = Tracker("tracker1", [])
    tracker2 = Tracker(
        "tracker2",
        [Application(0, "testApp1", "SWE"), Application(0, "testApp2", "SDE")],
    )
    assert unpickle_trackers() == []
    pickle_trackers([tracker1, tracker2])
    unpickled = unpickle_trackers()
    assert unpickled[0].name == "tracker1" and unpickled[1].name == "tracker2"
    assert len(unpickled[0].applications) == 0
    assert unpickled[1].applications[0].position == "SWE"
    assert unpickled[1].applications[1].company_name == "testApp2"
