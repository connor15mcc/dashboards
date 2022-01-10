from tracker.models import Application


def updateStatus(a: Application, formData: str) -> None:
    if "accept" in formData.lower():
        a.status = "Accepted"
    if "reject" in formData.lower():
        a.status = "Rejected"
    if "appl" in formData.lower():
        a.status = "Applied"
