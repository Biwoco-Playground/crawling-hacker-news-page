import re

from datetime import datetime
from dateutil.relativedelta import relativedelta


def clone_page(requests, page):
    print("Cloning page {page}...".format(page=page))
    URL = "https://news.ycombinator.com/news?p={page}".format(page=page)
    response = requests.get(URL)
    return response


def convert_ago_to_date(str_ago):
    value, unit = re.search(
                            r"(\d+) (\w+) ago", str_ago).groups()
    if not unit.endswith("s"):
        unit += "s"
    delta = relativedelta(**{unit: int(value)})
    return datetime.now() - delta
