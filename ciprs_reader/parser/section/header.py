from ciprs_reader.const import Section
from ciprs_reader.parser.base import Parser


class HeaderParser(Parser):
    """Only enabled when in intro header section."""

    def is_enabled(self):
        return self.state.section == Section.HEADER


class CaseDetails(HeaderParser):
    """Extract County and File No from header on top of first page"""

    pattern = r"\s*Case (Details|Summary) for Court \s*Case[\s:]+(?P<county>.+) (?P<fileno>\w+)"

    def extract(self, matches, report):
        report["General"]["County"] = matches["county"]
        report["General"]["File No"] = matches["fileno"]


class DefendantName(HeaderParser):

    pattern = r"\s*Defendant: \s*(?P<value>\S+)"
    section = ("Defendant", "Name")

    def clean(self, matches):
        # Change name from last,first,middle to FIRST MIDDLE LAST
        name = matches["value"]
        name_list = name.split(",")
        try:
            if len(name_list) == 2:
                name = "{} {}".format(name_list[1], name_list[0])
            elif len(name_list) == 3:
                name = "{} {} {}".format(name_list[1], name_list[2], name_list[0])
        except:
            name = ""
        matches["value"] = name.upper()
        return matches
