import re
import os

from timeit import default_timer
from datetime import datetime
from dateutil.relativedelta import relativedelta


def init_results_dir():
    dir = 'results'
    if not os.path.exists(dir):
        os.makedirs(dir)


def clone_page(requests_session, url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11 Linux x86_64)'
                +' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'}
    response = requests_session.get(url, headers = headers)
    print(response)
    return response


def convert_ago_to_date(str_ago):
    value, unit = re.search(
                            r"(\d+) (\w+) ago", str_ago).groups()
    if not unit.endswith("s"):
        unit += "s"
    delta = relativedelta(**{unit: int(value)})
    return (datetime.now() - delta).isoformat()


def calculate_compiling_time(start_time):
    stop_time = default_timer()
    with open('results/compiling_time.txt', 'w') as compiling_time:
        compiling_time.write(
                            'Compiling time: {time}'.format(
                                                            time = stop_time - start_time))


def dump_txt_file(str_content, filename):
    with open("results/" + filename + ".html", "w") as f:
        f.write(str_content)


MULTIPLE_WHITESPACE_PATTERN = re.compile(r"\s+", re.UNICODE)


def normalize_whitespace(text):
    return MULTIPLE_WHITESPACE_PATTERN.sub(replace_whitespace, text)


def replace_whitespace(match):
    text = match.group()
    if "\n" in text or "\r" in text:
        return "\n"
    else:
        return " "