from dashboards.models import Tracker, Application, Event
from flask import Blueprint
from datetime import datetime
from typing import List

filters = Blueprint("filters", __name__)


# Formatting Datetimes in Jinja:
@filters.app_template_filter("formatdatetime")
def format_datetime(value, format="%B %d, %Y"):
    """Format a date time to (Default): Month Day, LongYear"""
    if value is None:
        return ""
    return value.strftime(format).lstrip("0").replace(" 0", " ")


@filters.app_template_filter("formattimedelta")
def format_timedelta(value):
    """Format a time delta to number of days"""
    return f"{value.days} days"


# Transforming Tracker Names to IDs and Vice Versa:
@filters.app_template_filter("to_nameid")
def to_nameid(name: str) -> str:
    return name.replace(" ", "_").lower()


@filters.app_template_filter("to_name")
def to_name(nameid: str) -> str:
    parts = nameid.replace("_", " ").split(" ")
    return " ".join([word.capitalize() for word in parts])


@filters.app_template_filter("to_nameid_from_trackerid")
def to_nameid_from_trackerid(trackerid: int) -> str:
    (correctTracker,) = Tracker.query.filter_by(tracker_id=trackerid)
    return to_nameid(correctTracker.name)


@filters.app_template_filter("timeSinceUpdate")
def timeSinceUpdate(a: Application) -> datetime:
    srtd = sortedEvents(a)
    if srtd:
        return datetime.now() - srtd[0].date
    else:
        return None


@filters.app_template_filter("daysSinceUpdate")
def daysSinceUpdate(a: Application) -> int:
    return timeSinceUpdate(a).days


@filters.app_template_filter("toBootstrapColor")
def toBootstrapColor(i: int) -> str:
    range = 12
    result = ""
    if i > range // 2:
        result = "bg-danger"
    elif i > range // 4:
        result = "bg-warning"
    return result


@filters.app_template_filter("sortedEvents")
def sortedEvents(a: Application) -> List[Event]:
    result = sorted(a.event_history, key=lambda e: datetime.now() - e.date)
    return result


@filters.app_template_filter("filterAppsNeedAction")
def filterAppsNeedAction(apps: List[Application]) -> List[Application]:
    return [
        a
        for a in apps
        if sortedEvents(a)[0].action_necessary and not a.status == "Rejected"
    ]


@filters.app_template_filter("filterAppsStillValid")
def filterAppsStillValid(apps: List[Application]) -> List[Application]:
    return [
        a
        for a in apps
        if (not sortedEvents(a)[0].action_necessary and not a.status == "Rejected")
    ]


@filters.app_template_filter("filterAppsOther")
def filterAppsOther(apps: List[Application]) -> List[Application]:
    return [a for a in apps if a.status == "Rejected"]


@filters.app_template_filter("sortApps")
def sortApps(apps: List[Application]) -> List[Application]:
    result = sorted(apps, key=lambda a: -daysSinceUpdate(a))
    return result


@filters.app_template_filter("totalAwaitingAction")
def totalAwaitingAction(t: Tracker) -> int:
    apps = filterAppsNeedAction(t.applications)
    return len(apps)


@filters.app_template_filter("totalApplications")
def totalApplications(t: Tracker) -> int:
    apps = t.applications
    return len(apps)
