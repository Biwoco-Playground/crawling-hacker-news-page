import json

from models import Article
from utils import clean_number_comments, clean_points, convert_ago_to_date, clone_page
from pyquery import PyQuery

def create_articles_from_tr_tags(tr_tags):
    articles = []
    articles_append = articles.append
    i = 0
    for row in tr_tags:
        str_row = str(row)
        if 'class="athing"' in str_row:
            article = Article()

            article.id = row.attr("id")

            article.title = row.find("a.storylink").text()

            article.content_url = row.find("a.storylink").attr("href")

            articles_append(article)

        elif ('class="morespace"' not in str_row
                and 'class="spacer"' not in str_row
                and 'class="title"' not in str_row):
            article = articles[i]

            points = clean_points(
                                    row.find("span.score").text())
            article.points = points

            article.created_date = convert_ago_to_date(
                                                        row.find("span.age a").text())

            article.author = row.find("a.hnuser").text()

            number_comments = clean_number_comments(
                                                    row.find("a:eq(3)").text())
            article.number_comments = number_comments

            i += 1
    
    return articles

def parse_hacker_news_pages(start_page, end_page):
    url = "https://news.ycombinator.com/news"
    html_doc = ""
    for page_index in range(start_page, end_page + 1):
        page = clone_page(url, page_index)
        html_doc += page.html()

    pages = PyQuery(html_doc)
    tr_tags = pages.find("table.itemlist tr").items()
    articles = create_articles_from_tr_tags(tr_tags)

    with open("results/articles.json", "w") as result:
        json.dump(
                [article.__dict__ for article in articles], result, 
                indent=4)