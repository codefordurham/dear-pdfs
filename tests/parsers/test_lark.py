from ciprs_reader.parser.lark.parser import OffenseSectionParser

DISTRICT_KEY = "District Court Offense Information"
SUPERIOR_KEY = "Superior Court Offense Information"


def test_lark_charged(report, state):
    string = """
        District Court Offense Information

        Current Jurisdiction: DISTRICT COURT

        #                        Description                    Severity                 Law

        01  CHARGED         SPEEDING(80 mph in a 65 mph zone)            MISDEMEANOR        G.S. 14-33(C)(2)

            CONVICTED                          -                        -                  -

        Plea: -                Verdict: -                         Disposed on: 08/22/3022

        Disposition Method: DISMISSAL WITHOUT LEAVE BY DA

        Superior Court Offense Information

        This case does not have a record in Superior Court.

        Disclaimer
    """
    OffenseSectionParser(report, state).find(string)
    assert report, "Failed to extract data"
    assert DISTRICT_KEY in report and len(report[DISTRICT_KEY]) == 1, "Expected one offense"

    offense_info = report[DISTRICT_KEY][0]
    assert "Records" in offense_info and len(offense_info["Records"]) == 1, "Expected one offense line"

    assert offense_info["Disposed On"] == "3022-08-22"
    assert offense_info["Disposition Method"] == "DISMISSAL WITHOUT LEAVE BY DA"
    assert "Plea" not in offense_info
    assert "Verdict" not in offense_info

    offense_line = offense_info["Records"][0]
    assert offense_line["Action"] == "CHARGED"
    assert offense_line["Description"] == "SPEEDING(80 mph in a 65 mph zone)"
    assert offense_line["Severity"] == "MISDEMEANOR"
    assert offense_line["Law"] == "G.S. 14-33(C)(2)"


def test_lark_convicted(report, state):
    string = """
        District Court Offense Information
        Current Jurisdiction: DISTRICT COURT

        #                                         Description                              Severity                  Law
        01  CHARGED       POS/CON F-WN/LQ/MXBV UNATH PR          TRAFFIC            G.S. 20-130.1
            CONVICTED     POS/CON F-WN/LQ/MXBV UNATH PR     TRAFFIC         G.S. 20-130.1

        Plea: GUILTY          Verdict: GUILTY             Disposed on: 10/01/2009
        Disposition Method: DISPOSED BY JUDGE

        Superior Court Offense Information
        This case does not have a record in Superior Court.
        Disclaimer
    """
    OffenseSectionParser(report, state).find(string)
    assert report, "Failed to extract data"
    assert DISTRICT_KEY in report and len(report[DISTRICT_KEY]) == 1, "Expected one offense"

    offense_info = report[DISTRICT_KEY][0]
    assert "Records" in offense_info and len(offense_info["Records"]) == 2, "Expected two offense lines"

    assert offense_info["Disposed On"] == "2009-10-01"
    assert offense_info["Disposition Method"] == "DISPOSED BY JUDGE"
    assert offense_info["Plea"] == "GUILTY"
    assert offense_info["Verdict"] == "GUILTY"

    for i, offense_line in enumerate(offense_info["Records"]):
        assert offense_line["Action"] == "CHARGED" if i == 0 else "CONVICTED"
        assert offense_line["Description"] == "POS/CON F-WN/LQ/MXBV UNATH PR"
        assert offense_line["Severity"] == "TRAFFIC"
        assert offense_line["Law"] == "G.S. 20-130.1"


def test_lark_superior(report, state):
    string = """
        District Court Offense Information
        #                                         Description                              Severity                   Law
        51  CHARGED         ASSAULT ON A FEMALE        MISDEMEANOR          G.S.        14-33(C)(2)
            CONVICTED       ASSAULT ON A FEMALE        MISDEMEANOR          G.S.        14-33(C)(2)
        Plea: GUILTY           Verdict: PRAYER  FOR JUDGMENT      Disposed  on:  12/31/2000
        Disposition Method: DISPOSED BY JUDGE

        Superior Court Offense Information
        Current Jurisdiction: SUPERIOR COURT
        #                                         Description                              Severity                   Law
        51  CHARGED         ASSAULT ON A FEMALE        MISDEMEANOR          G.S.        14-33(C)(2)
            CONVICTED       ASSAULT ON A FEMALE        MISDEMEANOR          G.S.        14-33(C)(2)
        Plea: GUILTY           Verdict: PRAYER  FOR JUDGMENT      Disposed  on:  12/31/2000
        Disposition Method: DISPOSED BY JUDGE
    """
    OffenseSectionParser(report, state).find(string)
    assert report, "Failed to extract data"
    for jurisdiction in [DISTRICT_KEY, SUPERIOR_KEY]:
        assert jurisdiction in report and len(report[jurisdiction]) == 1, "Expected one offense"

        offense_info = report[jurisdiction][0]
        assert "Records" in offense_info and len(offense_info["Records"]) == 2, "Expected two offense lines"

        assert offense_info["Disposed On"] == "2000-12-31"
        assert offense_info["Disposition Method"] == "DISPOSED BY JUDGE"
        assert offense_info["Plea"] == "GUILTY"
        assert offense_info["Verdict"] == "PRAYER FOR JUDGMENT"

        for i, offense_line in enumerate(offense_info["Records"]):
            assert offense_line["Action"] == "CHARGED" if i == 0 else "CONVICTED"
            assert offense_line["Description"] == "ASSAULT ON A FEMALE"
            assert offense_line["Severity"] == "MISDEMEANOR"
            assert offense_line["Law"] == "G.S. 14-33(C)(2)"


def test_lark_multiline(report, state):
    string = """
        District Court Offense Information
        Current Jurisdiction: DISTRICT COURT
        #                                         Description                           Severity                  Law

        01  CHARGED     OPEN CONT AFTER CONS ALC 1ST(Blood    Alcohol  =     TRAFFIC         G.S. 20-138.7(A)

                            NOT REQUIRED)

            CONVICTED                       -                       -                    -

        Plea: -                    Verdict: -             Disposed on: 01/01/2001
        Disposition Method: DISMISSAL WITHOUT LEAVE BY DA

        Superior Court Offense Information
        This case does not have a record in Superior Court.

        Disclaimer
    """
    OffenseSectionParser(report, state).find(string)
    assert report, "Failed to extract data"
    assert DISTRICT_KEY in report and len(report[DISTRICT_KEY]) == 1, "Expected one offense"

    offense_info = report[DISTRICT_KEY][0]
    assert "Records" in offense_info and len(offense_info["Records"]) == 1, "Expected one offense line"

    assert offense_info["Disposed On"] == "2001-01-01"
    assert offense_info["Disposition Method"] == "DISMISSAL WITHOUT LEAVE BY DA"
    assert "Plea" not in offense_info
    assert "Verdict" not in offense_info

    offense_line = offense_info["Records"][0]
    assert offense_line["Action"] == "CHARGED"
    assert offense_line["Description"] == "OPEN CONT AFTER CONS ALC 1ST(Blood Alcohol = NOT REQUIRED)"
    assert offense_line["Severity"] == "TRAFFIC"
    assert offense_line["Law"] == "G.S. 20-138.7(A)"


def test_lark_no_data(report, state):
    string = """
        Case Summary for Court Case: DURHAM 09CR704582
    """
    OffenseSectionParser(report, state).find(string)
    assert not report, "Expected to extract no data"
