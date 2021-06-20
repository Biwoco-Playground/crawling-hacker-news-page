import re

from timeit import default_timer
from shutil import rmtree
from os import makedirs, path
from datetime import datetime
from dateutil.relativedelta import relativedelta


def init_results_dir():
    dir = 'results'
    if not path.exists(dir):
        makedirs(dir)

def clone_page(requests_session, url, page):
    print("Cloning page {page}...".format(page = page))
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
                +' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
    payload = {'p' : page}
    response = requests_session.get(
                                    url, params = payload, 
                                    headers = headers)
    print(response)
    return response

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

def calculate_compiling_time(start_time):
    stop_time = default_timer()
    with open('results/compiling_time.txt', 'w') as compiling_time:
        compiling_time.write(
                            'Compiling time: {time}'.format(
                                                            time = stop_time - start_time))