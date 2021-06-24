import re

from datetime import datetime
from dateutil.relativedelta import relativedelta


def convert_ago_to_date(str_ago):
    value, unit = re.search(
                            r"(\d+) (\w+) ago", str_ago).groups()
    if not unit.endswith("s"):
        unit += "s"
    delta = relativedelta(**{unit: int(value)})
    return (datetime.now() - delta).isoformat()

def clean_points(str_points):
    if str_points is not None:
        return int(
                    re.sub("points|point", "", 
                            str_points))
    return 0

def clean_number_comments(str_number_comments):
    if (str_number_comments is not None
            and str_number_comments != "hide"
            and str_number_comments != "discuss"):
        return int(
                    re.sub("\u00a0comments|\u00a0comment", "", 
                            str_number_comments))
    return 0