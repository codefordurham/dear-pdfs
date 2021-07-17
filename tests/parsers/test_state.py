import pytest

from ciprs_reader.const import Section
from ciprs_reader.parser.section import case_information, defendant, header, offense


@pytest.mark.parametrize(
    "Parser",
    [
        case_information.CaseStatus,
        case_information.OffenseDate,
        case_information.OffenseDateTime,
        case_information.CaseWasServedOnDate,
        defendant.DefendantRace,
        defendant.DefendantSex,
        offense.OffenseRecordRowWithNumber,
        offense.OffenseRecordRow,
        offense.OffenseDisposedDate,
        offense.OffenseDispositionMethod,
    ],
)
def test_parser__disabled_by_default(Parser, report, state):
    parser = Parser(report, state)
    assert not parser.is_enabled()


@pytest.mark.parametrize(
    "Parser",
    [
        header.CaseDetails,
        header.DefendantName,
    ],
)
def test_header_parsers__enabled(Parser, report, state):
    state.section = Section.HEADER
    assert Parser(report, state).is_enabled()


@pytest.mark.parametrize(
    "Parser",
    [
        header.CaseDetails,
        header.DefendantName,
    ],
)
def test_header_parsers__disabled(Parser, report, state):
    state.section = "Not Header"
    assert not Parser(report, state).is_enabled()


@pytest.mark.parametrize(
    "Parser",
    [
        case_information.CaseStatus,
        case_information.OffenseDate,
        case_information.OffenseDateTime,
        case_information.CaseWasServedOnDate,
    ],
)
def test_case_information_parsers__enabled(Parser, report, state):
    state.section = Section.CASE_INFORMATION
    assert Parser(report, state).is_enabled()


@pytest.mark.parametrize(
    "Parser",
    [defendant.DefendantRace, defendant.DefendantSex],
)
def test_defendant_parsers__enabled(Parser, report, state):
    state.section = Section.DEFENDANT
    assert Parser(report, state).is_enabled()


@pytest.mark.parametrize(
    "Parser",
    [
        offense.OffenseRecordRowWithNumber,
        offense.OffenseDisposedDate,
        offense.OffenseDispositionMethod,
    ],
)
@pytest.mark.parametrize(
    "section",
    [Section.DISTRICT_OFFENSE, Section.SUPERIOR_OFFENSE],
)
def test_offense_parsers__enabled(Parser, section, report, state):
    state.section = section
    assert Parser(report, state).is_enabled()


@pytest.mark.parametrize(
    "section",
    [Section.DISTRICT_OFFENSE, Section.SUPERIOR_OFFENSE],
)
def test_offense_record_row__enabled(section, report, state):
    state.offense_num = 1
    state.section = section
    assert offense.OffenseRecordRow(report, state).is_enabled()


def test_find__not_enabled(report, state):
    report = {"Defendant": {"Sex": None}}
    state.section = Section.HEADER
    defendant.DefendantSex(report, state).find("Sex: FEMALE")
    assert report["Defendant"]["Sex"] is None
