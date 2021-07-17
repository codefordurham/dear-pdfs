import subprocess


def convert_to_text(path):
    """Convert PDF to text using pdftotext library."""
    run = subprocess.run(
        f"pdftotext -table -enc UTF-8 {path} -",
        check=True,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return run.stdout.decode("utf-8")


def multi_summary_record_reader(path):
    """
    Sometimes multiple Summary CIPRS records are combined into a
    single PDF for easier document management by the attorney. This
    method splits records up for individual processing.
    """
    text = convert_to_text(path)
    records = text.split("Case Summary for Court")
    # trim any short records (probably just header text)
    records = [x for x in records if len(x) > 1000]
    # re-add text that was used to split to each record
    records = ["Case Summary for Court" + x for x in records]
    for record in records:
        yield record


def json_default(obj):
    """Helper function to JSON serialize objects when using dumps()."""
    try:
        return obj.__json__()
    except AttributeError as invaild_object_type:
        raise TypeError("{} can not be JSON encoded".format(type(obj))) from invaild_object_type


class LineReader:
    """Wrapper class to iterate over lines in a string."""

    def __init__(self, source):
        self.source = source
        self.lines = iter(source.splitlines())
        self.current = None

    def next(self):
        self.current = next(self.lines, None)
        return self.current

    def __str__(self):
        return self.current or ""
