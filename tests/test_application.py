from tracker.application import Application


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
