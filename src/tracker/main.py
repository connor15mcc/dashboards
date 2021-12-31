from typing import List
from tracker.tracker import Tracker
import pickle


def unpickle_trackers() -> List[Tracker]:
    try:
        with open("tracker.p", "rb") as pickler:
            return pickle.load(pickler)
    except Exception:
        return []


def pickle_trackers(trkrs: List[Tracker]) -> None:
    with open("tracker.p", "wb") as pickler:
        pickle.dump(trkrs, pickler)
