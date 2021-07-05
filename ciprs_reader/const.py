# pylint: disable=too-few-public-methods
from enum import IntEnum


class ParserMode(IntEnum):
    V1 = 1
    V2 = 2


class Section:
    """Section headers within a CIPRS record."""

    HEADER = "Header"
    CASE_INFORMATION = "Case Information"
    VIOLATION_OF_COURT_ORDERS = "Violation of Court Orders"
    DEFENDANT = "Defendant"
    WITNESS = "Witnesses"
    DISTRICT_OFFENSE = "District Court Offense Information"
    SUPERIOR_OFFENSE = "Superior Court Offense Information"
