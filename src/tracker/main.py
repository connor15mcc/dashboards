from typing import List
from tracker.tracker import Tracker
import pickle
import os

PICKLE_LOCATION = "tracker.p"


def unpickle_trackers(loc: str) -> List[Tracker]:
    try:
        with open(loc, "rb") as pickler:
            return pickle.load(pickler)
    except Exception:
        return []


def pickle_trackers(loc: str, trkrs: List[Tracker]) -> None:
    with open(loc, "wb") as pickler:
        pickle.dump(trkrs, pickler)


def remove_pickle(loc: str) -> None:
    os.remove(loc)
