from tracker.application import Application
import pytest


application1 = Application(1, "Connor", "SWE")


def test_creation():
    assert application1.application_id == 1
    assert application1.company_name == "Connor"
    assert application1.position == "SWE"


def test_visualization():
    assert str(application1) == ("Application #1 at Connor for the SWE position")
    assert repr(application1) == ("Application(1, Connor, SWE)")


def test_equality():
    application2 = Application(1, "Connor", "SWE")
    assert application1 is not application2
    assert application1 == application2
    assert hash(application1) == hash(application2)


def test_source_assignment():
    application1.source = "Linkedin"
    assert application1.source == "Linkedin"
    with pytest.raises(ValueError) as excinfo:
        application1.source = "Testing"
    assert str(excinfo.value) == "This isn't a proper source"


def test_status_assignment():
    application1.status = "Applied"
    assert application1.status == "Applied"
    with pytest.raises(ValueError) as excinfo:
        application1.status = "Testing"
    assert str(excinfo.value) == "This isn't a valid status"
