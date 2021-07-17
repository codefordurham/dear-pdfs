# CIPRS Reader
[![Build Status](https://travis-ci.org/deardurham/ciprs-reader.svg?branch=master)](https://travis-ci.org/deardurham/ciprs-reader)

## Setup and Run:

Add pdf file to parse in /ignore folder then run:

```bash
docker build -t ciprs-reader .
docker run --rm -v "${PWD}:/usr/src/app" ciprs-reader python ciprs-reader.py ignore/cypress-example.pdf
```

Example output:

```json
[
    {
        "General": {
            "County": "DURHAM",
            "File No": "00GR000000"
        },
        "Case Information": {
            "Case Status": "DISPOSED",
            "Offense Date": "2018-01-01T20:00:00"
        },
        "Defendant": {
            "Date of Birth/Estimated Age": "1990-01-01",
            "Name": "DOE,JON,BOJACK",
            "Race": "WHITE",
            "Sex": "MALE"
        },
        "District Court Offense Information": [
            {
                "Records": [
                    {
                        "Action": "CHARGED",
                        "Description": "SPEEDING(70 mph in a 50 mph zone)",
                        "Severity": "TRAFFIC",
                        "Law": "20-141(J1)"
                    }
                ],
                "Disposed On": "2010-01-01",
                "Disposition Method": "DISMISSAL WITHOUT LEAVE BY DA"
            }
        ],
        "Superior Court Offense Information": [],
    }
]
```

## Local Setup

Pre-requisites:

```
brew cask install pdftotext
```

Setup:

```bash
pip install -r requirements.txt
pip install -e .
```

Read CIPRS PDF:

```
python ciprs_-eader.py ./cypress-example.pdf
```

Run Jupyter:

```bash
jupyter-lab
```

Run tests:

```bash
pytest --pylint
```

Code for Durham
