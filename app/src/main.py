import requests
import json

from bs4 import BeautifulSoup
from models import Article

min_page = 1
max_page = 20
html_doc = ""

for page in range(min_page, max_page):
    print("Cloning page {page}...".format(page=page))
    URL = 'https://news.ycombinator.com/news?p={page}'.format(page=page)
    response = requests.get(URL)
    html_doc += str(response.text)

main_soup = BeautifulSoup(html_doc, 'html.parser')

list_articles = []
tr_tags_id = ""
tr_tags_other = ""

list_tr_tags = main_soup.body.find_all("tr")
for i in range(2, len(list_tr_tags)-3):
    tag_tr = list_tr_tags[i]
    flag = "id=\"pagespace\"" not in str(tag_tr) and "class=\"spacer\"" not in str(
        tag_tr) and "class=\"morespace\"" not in str(tag_tr)
    if flag:
        id = tag_tr.get('id')
        if id is not None:
            tr_tags_id += str(tag_tr)
            new_article = Article()
            new_article.id = id
            list_articles.append(new_article)
        else:
            tr_tags_other += str(tag_tr)

soup_tags_id = BeautifulSoup(tr_tags_id, 'html.parser')

list_td_tags = soup_tags_id.find_all("td", "title")
index_article = 0
for i in range(len(list_td_tags)):
    flag = "align=\"right\"" not in str(list_td_tags[i])
    if flag:
        td_tag = list_td_tags[i]
        title = td_tag.a.string

        content_url = ""
        try:
            content_url = td_tag.span.a.string
        except:
            print("Article {index_article} has not content url".format(
                index_article=index_article+1))

        list_articles[index_article].title = title
        list_articles[index_article].content_url = content_url
        index_article += 1

soup_tags_other = BeautifulSoup(tr_tags_other, 'html.parser')

list_td_tags = soup_tags_other.find_all("td", "subtext")
index_article = 0
for td_tag in list_td_tags:
    span_tag = td_tag.span
    points = ""
    if "class=\"score\"" in str(span_tag):
        points = span_tag.string
    else:
        points = "flag:"+span_tag.string

    a_tag = td_tag.a
    author = ""
    if "flag:" not in points:
        author = a_tag.string
    else:
        print("Article {index_article} has not author".format(
            index_article=index_article+1))

    next_span = span_tag.find_next_siblings("span")
    created_date = ""
    try:
        created_date = next_span[0].string
    except:
        created_date = points.replace("flag:", "")

    points = str(points)
    if "points" in points:
        points = points.replace("points", "").strip()
        points = int(points)
    elif "ago" in points:
        created_date = points
        points = 0

    next_a = a_tag.find_next_siblings("a")
    number_comments = ""
    try:
        number_comments = str(next_a[1].string)
        if number_comments == "discuss":
            number_comments = 0
        else:
            number_comments = int(
                number_comments.replace("comments", "").strip())
    except:
        print("Article {index_article} has not comments".format(
            index_article=index_article+1))

    list_articles[index_article].points = points
    list_articles[index_article].author = author
    list_articles[index_article].created_date = created_date
    list_articles[index_article].number_comments = number_comments

    index_article += 1

json_articles = json.dumps(
    [article.__dict__ for article in list_articles], indent=4)

print(json_articles)
