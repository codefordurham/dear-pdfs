from lark import Lark
from .grammar import GRAMMAR
from .transformer import OffenseSectionTransformer

PARSER = Lark(GRAMMAR, start="document", parser="lalr")


class OffenseSectionParser:
    """Parses entire document and outputs offense section info."""

    def __init__(self, report, state):
        self.state = state
        self.report = report

    def find(self, document):
        tree = PARSER.parse(document)
        data = OffenseSectionTransformer().transform(tree)
        self.extract(data)

    def extract(self, raw_data):
        if "District" in raw_data:
            self.report["District Court Offense Information"] = raw_data["District"]
        if "Superior" in raw_data:
            self.report["Superior Court Offense Information"] = raw_data["Superior"]
