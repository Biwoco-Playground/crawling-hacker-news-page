import re
import requests

from datetime import datetime
from dateutil.relativedelta import relativedelta


ss = requests.Session()
def clone_page(url, page):
    print("Cloning page {page}...".format(page = page))
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
                +' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
    payload = {'p' : page}
    response = ss.get(
                        url, params = payload, 
                        headers=headers)
    print(response)
    return response


def convert_ago_to_date(str_ago):
    value, unit = re.search(
                            r"(\d+) (\w+) ago", str_ago).groups()
    if not unit.endswith("s"):
        unit += "s"
    delta = relativedelta(**{unit: int(value)})
    return (datetime.now() - delta).isoformat()
