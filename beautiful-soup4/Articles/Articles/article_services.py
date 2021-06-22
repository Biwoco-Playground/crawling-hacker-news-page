import requests

from utils import clone_page, clean_points, convert_ago_to_date, clean_number_comments
from models import Article
from bs4 import BeautifulSoup


def create_articles_from_tr_tags(tr_tags):
    return list(
                map(
                    lambda tr: Article(tr.get("id")) , tr_tags))

def map_attrs_to_articles_from_td_tags(articles, td_tags):
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
                    points = clean_points(span_tag.string)

                    a_tag = td_tag.a
                    author = a_tag.string

                    next_span = span_tag.find_next_sibling("span")
                    created_date = convert_ago_to_date(next_span.string)

                    next_a = a_tag.find_next_siblings("a")  
                    number_comments = clean_number_comments(next_a[1].string)
                else:
                    created_date = convert_ago_to_date(span_tag.string)

                articles[index_article].points = points
                articles[index_article].author = author
                articles[index_article].created_date = created_date
                articles[index_article].number_comments = number_comments
                index_article += 1

def parse_hacker_news_pages(start_page, end_page):
    requests_session = requests.Session()
    url = "https://news.ycombinator.com/news"
    html_doc = ""
    for page in range(start_page, end_page + 1):
        response = clone_page(
                                requests_session, url, 
                                page)
        html_doc += response.text

    main_soup = BeautifulSoup(html_doc, 'html.parser')                                            

    tr_tags = main_soup.select('tr.athing')

    articles = create_articles_from_tr_tags(tr_tags)

    td_tags = main_soup.find_all("td", attrs = {'class' : ["title", "subtext"]})

    map_attrs_to_articles_from_td_tags(articles, td_tags)

    return articles