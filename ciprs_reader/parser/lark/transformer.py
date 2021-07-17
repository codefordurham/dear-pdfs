from lark import Lark, Transformer
import datetime as dt


def key_string_tuple(key):
    return lambda self, str_list: (key, " ".join(str_list))


list_to_string = lambda self, str_list: " ".join(str_list)


class OffenseSectionTransformer(Transformer):
    def disposed_on(self, items):
        value = " ".join(items)
        date = dt.datetime.strptime(value, "%m/%d/%Y").date()
        return date.isoformat()

    def offense_line(self, items):
        # extract description_extended (if it exists) and combine with descritpion
        # action description severity law description_ext?
        (*fields, last_field) = items
        offense_line_dict = dict(fields)
        (key, value) = last_field
        if key == "Description Extended":
            offense_line_dict["Description"] = " ".join([offense_line_dict["Description"], value])
        else:
            offense_line_dict[key] = value
        return offense_line_dict

    def offense_section(self, items):
        if len(items) < 2:
            return items[0], []
        return items[0], items[1]

    def offense(self, items):
        offense_dict = {
            "Records": [items[0]],
            "Disposed On": items[4],
            "Disposition Method": items[5],
        }
        if items[1] and "Description" in items[1] and items[1]["Description"]:
            offense_dict["Records"].append(items[1])
        if items[2]:
            offense_dict["Plea"] = items[2]
        if items[3]:
            offense_dict["Verdict"] = items[3]
        return offense_dict

    document = dict
    offenses = list

    action = key_string_tuple("Action")
    description = key_string_tuple("Description")
    law = key_string_tuple("Law")
    severity = key_string_tuple("Severity")
    description_ext = key_string_tuple("Description Extended")

    # TODO: some of these should probably just be `str`
    # need to figure out how to get lark to store those as a string instead of list of strings
    # can likely use the `?` operator before rules in the grammar
    jurisdiction = list_to_string
    disposition_method = list_to_string
    plea = list_to_string
    verdict = list_to_string

    JURISDICTION = str
    ACTION = str
    SEVERITY = str
    TEXT = str
    LAW_PRE = str
