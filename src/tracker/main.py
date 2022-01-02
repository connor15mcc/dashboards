from typing import List
from tracker.tracker import Tracker
from tracker.application import Application
import pickle
import os

PICKLE_LOCATION = "tracker.p"


def unpickle_trackers(loc: str) -> List[Tracker]:
    try:
        with open(loc, "rb") as pickler:
            return pickle.load(pickler)
    except Exception:
        return [
            Tracker(
                "Fall_2021",
                "Recruiting for the Summer 2022 internship season",
                [Application(0, "Connor", "SWE"), Application(1, "McCarthy", "SWE")],
            ),
            Tracker(
                "Fall_2022", "Recruiting for the Summer 2023 internship season", []
            ),
        ]


def pickle_trackers(loc: str, trkrs: List[Tracker]) -> None:
    with open(loc, "wb") as pickler:
        pickle.dump(trkrs, pickler)


def remove_pickle(loc: str) -> None:
    os.remove(loc)
