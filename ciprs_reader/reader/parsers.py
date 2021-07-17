"""
Parsers that PDFToTextReader will use to parse CIPRS records.
"""

from ciprs_reader.parser import lines, state
from ciprs_reader.parser.lark.parser import OffenseSectionParser
from ciprs_reader.parser.section import case_information, defendant, header, offense


LINE_PARSERS = (
    # Start with parsers that only set state
    state.CaseInformation,
    state.DefendantSection,
    state.DistrictCourtOffenseSection,
    state.SuperiorCourtOffenseSection,
    state.DisclaimerSection,
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
)

# v1 line parsers for district/superior offense sections
OFFENSE_SECTION_PARSERS = (
    offense.OffenseRecordRow,
    offense.OffenseRecordRowWithNumber,
    offense.OffenseDisposedDate,
    offense.OffenseDispositionMethod,
    offense.OffensePlea,
    offense.OffenseVerdict,
)

# v2 document parsers
# TODO: Support extracting multiple data sections
LARK_PARSERS = (OffenseSectionParser,)

DOCUMENT_PARSERS = (
    lines.DefendentDOB,
    lines.DistrictSuperiorCourt,
)
