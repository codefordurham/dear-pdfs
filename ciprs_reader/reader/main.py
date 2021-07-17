import json
import logging

from ciprs_reader.parser.state import ParserState
from ciprs_reader.parser.models import Offenses
from ciprs_reader.reader.parsers import DOCUMENT_PARSERS, LINE_PARSERS, LARK_PARSERS
from ciprs_reader.reader import util


logger = logging.getLogger(__name__)


class PDFToTextReader:
    """Prase CIPRS Summary records into entity-extract JSON."""

    def __init__(self, path):
        self.path = path
        self.records = []

    def parse(self, save_source=False):
        for source in util.multi_summary_record_reader(self.path):
            reader = SummaryRecordReader(source)
            record = reader.parse(save_source)
            self.records.append(record)

    def json(self):
        return json.dumps(self.records, indent=4, default=util.json_default)


# pylint: disable=too-few-public-methods
class SummaryRecordReader:
    """Read through Summary record and perform entity extraction using parsers."""

    def __init__(self, text):
        self.text = text
        # skelton JSON structure for parser-extracted entities
        self.report = {
            "General": {},
            "Case Information": {},
            "Defendant": {},
            "District Court Offense Information": Offenses(),
            "Superior Court Offense Information": Offenses(),
            "_meta": {},
        }
        # object that stores state that's accessible between parsers
        self.state = ParserState()
        # line parsers are run against every line within a document
        self.line_parsers = []
        for parser in LINE_PARSERS:
            self.line_parsers.append(parser(self.report, self.state))

        self.document_parsers = []
        # document parsers are run once against an entire document
        for parser in DOCUMENT_PARSERS:
            self.document_parsers.append(parser(self.report, self.state))

        for parser in LARK_PARSERS:
            self.document_parsers.append(parser(self.report, self.state))

    def parse(self, save_source=False):
        logger.debug("pdftotext: %s", self.text)
        if save_source:
            # save output of pdftotext for later inspection, if desired
            self.report["_meta"]["source"] = self.text
        reader = util.LineReader(self.text)
        # pylint: disable=not-callable
        while reader.next() is not None:
            for parser in self.line_parsers:
                parser.find(reader)
        for parser in self.document_parsers:
            parser.find(reader.source)
        return self.report
