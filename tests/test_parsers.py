from ciprs_reader.parser import lines as parsers


def test_defendent_dob(report, state):
    string = """     Date of Birth/Estimated Age:     Driver License Information  \n
       01/01/2000       • License State: NC
    """
    matches = parsers.DefendentDOB(report, state).match(string)
    assert matches is not None, "Regex match failed"
    assert matches["value"] == "2000-01-01"


def test_court_type_other(report, state):
    report = {"General": {"File No": "11IF777777"}}
    matches = parsers.DistrictSuperiorCourt(report, state).match("")
    assert matches is not None, "Regex match failed"
    assert matches == {}


def test_court_type_cr(report, state):
    report = {"General": {"File No": "11CR777777"}}
    parser = parsers.DistrictSuperiorCourt(report, state)
    parser.find("")
    assert parser.matches is not None, "Regex match failed"
    assert parser.matches == {"District": "Yes"}
    assert report["General"]["District"] == "Yes"


def test_court_type_crs(report, state):
    report = {"General": {"File No": "11CRS777777"}}
    parser = parsers.DistrictSuperiorCourt(report, state)
    parser.find("")
    assert parser.matches is not None, "Regex match failed"
    assert parser.matches == {"Superior": "Yes"}
    assert report["General"]["Superior"] == "Yes"


def test_additional_offenses(report, state):
    string = """ ***    Additional offenses exist. To see a complete breakdown, view full case detail. * * * """
    matches = parsers.AdditionalOffenses(report, state).match(string)
    assert matches is not None, "Regex match failed"
    assert matches["value"]
