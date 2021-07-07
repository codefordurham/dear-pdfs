"""
Parsers that PDFToTextReader will use to parse CIPRS records.
"""

from ciprs_reader.parser import lines, state
from ciprs_reader.parser.section import case_information, defendant, header, offense


LINE_PARSERS = (
    # Start with parsers that only set state
    state.CaseInformation,
    state.DefendantSection,
    state.DistrictCourtOffenseSection,
    state.SuperiorCourtOffenseSection,
    # Section: General/Header
    header.CaseDetails,
    header.DefendantName,
    # Section: Case Information
    case_information.CaseStatus,
    case_information.OffenseDate,
    case_information.OffenseDateTime,
    case_information.CaseWasServedOnDate,
    # Section: Defendant
    defendant.DefendantRace,
    defendant.DefendantSex,
    # Section: Offenses (District & Superior)
    offense.OffenseRecordRow,
    offense.OffenseRecordRowWithNumber,
    offense.OffenseDisposedDate,
    offense.OffenseDispositionMethod,
    offense.OffensePlea,
    offense.OffenseVerdict,
)

DOCUMENT_PARSERS = (
    lines.DefendentDOB,
    lines.DistrictSuperiorCourt,
    lines.AdditionalOffenses,
)
