import json

from timeit import default_timer
from re import sub
from shutil import rmtree
from os import makedirs, path
from bs4 import BeautifulSoup
from models import Article
from utils import convert_ago_to_date, clone_page, create_article_from_tr_tag
    

start = default_timer()
page = 1
url = "https://news.ycombinator.com/news"
response = clone_page(url, page)
html_doc = response.text
# html_doc = ""
# res_text = response.text
# while "class=\"morelink\"" in res_text:
#     html_doc += res_text
#     page += 1
#     response = clone_page(url, page)
#     res_text = response.text
main_soup = BeautifulSoup(html_doc, 'lxml')

articles = list(
                map(create_article_from_tr_tag, main_soup.select('tr.athing')))

td_tags = main_soup.find_all("td", attrs={'class' : ["title", "subtext"]})
index_article = 0
for td_tag in td_tags:
    str_td_tag = str(td_tag)
    if ("align=\"right\"" in str_td_tag
        or "class=\"morelink\"" in str_td_tag):      
        continue
    else:
        if "class=\"title\"" in str_td_tag:
            title = td_tag.a.string
            content_url = td_tag.a.get("href")

            articles[index_article].title = title
            articles[index_article].content_url = content_url

        elif "class=\"subtext\"" in str_td_tag:
            span_tag = td_tag.span

            points = 0
            author = "" 
            created_date = ""
            number_comments = 0
            if span_tag.get("class")[0] == "score":
                points = int(
                            span_tag.string.replace("points", "").strip())

                a_tag = td_tag.a
                author = a_tag.string

                next_span = span_tag.find_next_siblings("span")
                created_date = convert_ago_to_date(next_span[0].string)

                next_a = a_tag.find_next_siblings("a")                
                extracting_comments = next_a[1].string
                if extracting_comments != "discuss":
                    number_comments = int(
                                        sub(
                                            "comments|comment", "", 
                                            extracting_comments))
            else:
                created_date = convert_ago_to_date(span_tag.string)

            articles[index_article].points = points
            articles[index_article].author = author
            articles[index_article].created_date = created_date
            articles[index_article].number_comments = number_comments
            index_article += 1


stop = default_timer()

dir = 'results'
if path.exists(dir):
    rmtree(dir)
makedirs(dir)

with open('results/result.txt', 'w') as result, \
        open('results/compiling_time.txt', 'w') as compiling_time:
    json_articles = json.dump(
                            [article.__dict__ for article in articles], result, 
                            indent = 4)

    compiling_time.write('Compiling time: {time}'.format(time = stop - start))