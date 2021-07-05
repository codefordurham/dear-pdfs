from unittest.mock import patch
import pytest

from ciprs_reader.const import ParserMode
from ciprs_reader.reader import PDFToTextReader


@pytest.fixture(name="mock_subprocess")
def fixture_mock_subprocess():
    with patch("ciprs_reader.reader.util.subprocess.run") as mock:
        mock.stdout.decode.return_value = ""
        yield mock


def test_pdftotext_args_v1(mock_subprocess):
    PDFToTextReader("dummy.pdf", mode=ParserMode.V1).parse()
    cmd = mock_subprocess.call_args[0][0]
    assert "-layout" in cmd


def test_pdftotext_args_v2(mock_subprocess):
    PDFToTextReader("dummy.pdf", mode=ParserMode.V2).parse()
    cmd = mock_subprocess.call_args[0][0]
    assert "-table" in cmd
