import pytest

from ciprs_reader.parser.section import offense


def test_offense_record_charged(report, state):
    string = """
        CHARGED     SPEEDING(80 mph in a 65 mph zone)    INFRACTION    G.S. 20-141(B)
    """
    matches = offense.OffenseRecordRow(report, state).match(string)
    assert matches is not None, "Regex match failed"
    assert matches["action"] == "CHARGED"
    assert matches["desc"] == "SPEEDING(80 mph in a 65 mph zone)"
    assert matches["severity"] == "INFRACTION"
    assert matches["law"] == "G.S. 20-141(B)"


def test_offense_record_charged_with_number(report, state):
    string = """
        54  CHARGED       SPEEDING(80 mph in a 65 mph zone)    INFRACTION    G.S. 20-141(B)    
    """
    matches = offense.OffenseRecordRowWithNumber(report, state).match(string)
    assert matches is not None, "Regex match failed"
    assert matches["action"] == "CHARGED"
    assert matches["desc"] == "SPEEDING(80 mph in a 65 mph zone)"
    assert matches["severity"] == "INFRACTION"
    assert matches["law"] == "G.S. 20-141(B)"


def test_offense_record_arrainged(report, state):
    string = """
        ARRAIGNED SPEEDING(80 mph in a 65 mph zone)        INFRACTION    G.S. 20-141(B)
    """
    matches = offense.OffenseRecordRow(report, state).match(string)
    assert matches is not None, "Regex match failed"
    assert matches["action"] == "ARRAIGNED"
    assert matches["desc"] == "SPEEDING(80 mph in a 65 mph zone)"
    assert matches["severity"] == "INFRACTION"
    assert matches["law"] == "G.S. 20-141(B)"


def test_offense_record_with_slashes(report, state):
    string = """
        CONVICTED  CITY/TOWN VIOLATION (I)  INFRACTION  LOCAL ORDINANCE
    """
    matches = offense.OffenseRecordRow(report, state).match(string)
    assert matches is not None, "Regex match failed"
    assert matches["desc"] == "CITY/TOWN VIOLATION (I)"


@pytest.mark.xfail(reason="parser v1 known issue")
def test_offense_record_with_multiline_description(report, state):
    string = """
            01 CHARGED   OPEN  CONT AFTER CONS    ALC 1ST(Blood Alcohol =    TRAFFIC    G.S. 20-138.7(A)
    NOT REQUIRED)
    TEST
            CONVICTED - - -
    """
    matches = offense.OffenseRecordRowWithNumber(report, state).match(string)
    assert matches is not None, "Regex match failed"
    assert "NOT REQUIRED" in matches["desc"]


def test_offense_record_convicted(report, state):
    string = """
        CONVICTED IMPROPER EQUIP - SPEEDOMETER             INFRACTION    G.S. 20-123.2
    """
    matches = offense.OffenseRecordRow(report, state).match(string)
    assert matches is not None, "Regex match failed"
    assert matches["action"] == "CONVICTED"
    assert matches["desc"] == "IMPROPER EQUIP - SPEEDOMETER"
    assert matches["severity"] == "INFRACTION"
    assert matches["law"] == "G.S. 20-123.2"


@pytest.mark.parametrize(
    "expected,val",
    (
        ("2000-01-01", "      Disposed on: 01/01/2000   "),
        (
            "2016-07-20",
            "    Plea: RESPONSIBLE                         Verdict: RESPONSIBLE             Disposed on: 07/20/2016   ",
        ),
    ),
)
def test_offense_disposed_date(expected, val, report, state):
    matches = offense.OffenseDisposedDate(report, state).match(val)
    assert matches is not None, "Regex match failed"
    assert matches["value"] == expected


def test_known_offense_disposition_method(report, state):
    string = """
        Disposition Method: WAIVER - MAGISTRATE    
    """
    matches = offense.OffenseDispositionMethod(report, state).match(string)
    assert matches is not None, "Regex match failed"
    assert matches["value"] == "WAIVER - MAGISTRATE"


def test_plea(report, state):
    string = """
        Plea: NOT GUILTY                     Verdict:                             Disposed on:    
    """
    matches = offense.OffensePlea(report, state).match(string)
    assert matches is not None, "Regex match failed"
    assert matches["value"] == "NOT GUILTY"


def test_verdict(report, state):
    string = "Plea: GUILTY                       Verdict: NOT GUILTY                       Disposed on: "
    matches = offense.OffenseVerdict(report, state).match(string)
    assert matches is not None, "Regex match failed"
    assert matches["value"] == "NOT GUILTY"
