import collections

import pytest

from ciprs.parser import lines


@pytest.fixture
def report():
    return {}


@pytest.fixture
def state():
    return collections.defaultdict(str)


def test_offense_record_row__in_state(report, state):
    parser = lines.OffenseRecordRow(report, state)
    assert not parser.in_state()


def test_offense_record_row__not_in_state(report, state):
    state["num"] = 1
    state["section"] = "District Court Offense Information"
    assert lines.OffenseRecordRow(report, state).in_state()