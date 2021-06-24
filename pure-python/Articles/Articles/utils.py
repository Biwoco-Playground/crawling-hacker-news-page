import re
import json

from timeit import default_timer
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

def dump_objects_to_json_file(objects, filename):
    with open('results/' + filename + '.json', 'w') as result:
        json.dump(
                [object.__dict__ for object in objects], result, 
                indent = 4)

def count_tags(tag, str_html):
    result = 0
    start_tag = "<" + tag
    for sub in str_html.split(" "):
        if start_tag in sub:
            result += 1

    return result

# def get_tags(tag, str_html):
#     result = []
#     result_append = result.append
#     count_tr_tags = count_tags(tag, str_html)
#     start_tag = "<" + tag
#     end_tag = "</" + tag + ">"
#     rows = count_tr_tags + 1
#     columns = len(str_html.split(" "))
#     tag_html = ""
#     current_start_tag = 0
#     current_end_tag = 0
#     for i in range(rows * columns):
#         row = i // columns
#         if row < 1:
#             continue
#         col = i % columns
#         sub = str_html.split(" ")[col]
#         if start_tag in sub:
#             current_start_tag += 1

#         if current_start_tag == row:
#             tag_html += sub + " "

#         if end_tag in sub:
#             current_end_tag += 1

#         if (col == columns - 1
#             and tag_html != ""):
#             if not tag_html.startswith(start_tag):
#                 tag_html = start_tag + " " + tag_html

#             if not tag_html.rstrip().endswith(end_tag):
#                 tag_html = tag_html + " " + end_tag  

#             result_append(tag_html)
#             tag_html = ""
#             current_start_tag = 0
#             current_end_tag = 0
            
#     return result
    
def get_tags(tag, str_html):
    result = []
    result_append = result.append
    count_tr_tags = count_tags(tag, str_html)
    start_tag = "<" + tag
    end_tag = "</" + tag + ">"
    for i in range(1, count_tr_tags + 1):
        tag_html = ""
        current_start_tag = 0
        current_end_tag = 0
        for sub in str_html.split(" "):
            if start_tag in sub:
                current_start_tag += 1

            if current_start_tag == i:
                tag_html += sub + " "

            if end_tag in sub:
                current_end_tag += 1

        if tag_html != "":
            if not tag_html.startswith(start_tag):
                tag_html = start_tag + " " + tag_html

            if not tag_html.rstrip().endswith(end_tag):
                tag_html = tag_html + " " + end_tag      

            result_append(tag_html)

    return result

def filter_tags_by_classname(classname, str_html):    
    return list(
                filter(
                        lambda tag: classname in str(tag), str_html))

def get_attr_from_tag(attr_name, str_html):
    result = ""
    count = 0
    for sub in str_html.split(" "):
        if attr_name in sub:
            result += sub

            if "\"" in sub:
                count += 1

            if sub.endswith("\""):
                count += 1

            if (count == 2 
                or ">" in sub):
                break

    result = (result.replace(attr_name, "")
                    .replace("\"", "")
                    .replace(">", "")
                    .replace("=", "")
                    .replace("\n", ""))
    return result