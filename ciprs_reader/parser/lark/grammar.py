GRAMMAR = r"""
    document        : ((offense_section | _IGNORE) | _NEWLINE)*

    _IGNORE.-1      : (/[^\n]/)+
    _ignore_line   : _IGNORE _NEWLINE

    offense_section : jurisdiction (_ignore_line+ offenses |_missing_offenses)
    jurisdiction    : JURISDICTION "Court" "Offense" "Information" _NEWLINE
    _missing_offenses : "This" "case" "does" "not" "have" "a" "record" _IGNORE

    offenses        : offense+
    offense         : offense_line ~ 2 _offense_info disposition_method _NEWLINE

    offense_line    : _RECORD_NUM? action (_some_offense | _no_offense)
    _RECORD_NUM.0   : INT
    action          : ACTION
    _no_offense     : _MINUS+ _NEWLINE

    _some_offense   : description severity law _NEWLINE (description_ext _NEWLINE)*
    description     : TEXT+
    severity        : SEVERITY
    law             : LAW_PRE TEXT+
    description_ext : (/(?!Plea:|CONVICTED)\S+/)+

    _offense_info   : "Plea:" plea "Verdict:" verdict "Disposed" "on:" disposed_on _NEWLINE
    plea            : (/(?!Verdict:)\S+/)+ | _MINUS
    verdict         : (/(?!Disposed)\S+/)+ | _MINUS
    disposed_on     : TEXT+ | _MINUS

    disposition_method : "Disposition" "Method:" TEXT+

    JURISDICTION    : "District" | "DISTRICT"
                    | "Superior" | "SUPERIOR"

    ACTION  : "CHARGED"
            | "CONVICTED"
            | "ARRAIGNED"

    SEVERITY    : "TRAFFIC"
                | "INFRACTION"
                | "MISDEMEANOR"
                | "FELONY"

    LAW_PRE     : "G.S."
    TEXT.0      : /\S+/
    _MINUS.0    : "-"

    _NEWLINE    : /[\r\n]/+
    WS_INLINE   : (" "|/\t/|/\f/)+

    %import common.INT
    %ignore WS_INLINE
"""
