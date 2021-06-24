import requests
import utils

from models import Article


def create_articles_from_tr_tags(tr_tags):    
    return list(
                map(
                    lambda tr: Article(
                                        utils.get_attr_from_tag("id", tr)) , tr_tags))

def map_attrs_to_articles_from_td_tags(articles, td_tags_title, td_tags_subtext):
    index_article = 0
    for td_tag in td_tags_title:
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
                index_article += 1

            # elif "class=\"subtext\"" in str_td_tag:
            #     span_tag = td_tag.span

            #     points = 0
            #     author = "" 
            #     created_date = ""
            #     number_comments = 0
            #     if span_tag.get("class")[0] == "score":
            #         points = utils.clean_points(span_tag.string)

            #         a_tag = td_tag.a
            #         author = a_tag.string

            #         next_span = span_tag.find_next_sibling("span")
            #         created_date = utils.convert_ago_to_date(next_span.string)

            #         next_a = a_tag.find_next_siblings("a")  
            #         number_comments = utils.clean_number_comments(next_a[1].string)
            #     else:
            #         created_date = utils.convert_ago_to_date(span_tag.string)

            #     articles[index_article].points = points
            #     articles[index_article].author = author
            #     articles[index_article].created_date = created_date
            #     articles[index_article].number_comments = number_comments
            #     index_article += 1

def parse_hacker_news_pages(start_page, end_page):
    articles = []
    requests_session = requests.Session()
    url = "https://news.ycombinator.com/news"
    str_html = ""
    for page in range(start_page, end_page + 1):
        response = utils.clone_page(
                                requests_session, url, 
                                page)
        str_html += response.text

    str_html = (response.text.replace("<", " <")
                                .replace("'", "\""))
    table_tags = utils.get_tags("table", str_html)

    tr_tags = utils.get_tags("tr", table_tags[2])
    tr_tags_athing = utils.filter_tags_by_classname("athing", tr_tags)

    articles = create_articles_from_tr_tags(tr_tags_athing)

    td_tags = utils.get_tags("td", table_tags[2])
    td_tags_title = utils.filter_tags_by_classname("title", td_tags)
    # td_tags_subtext = utils.filter_tags_by_classname("subtext", td_tags)

    # map_attrs_to_articles_from_td_tags(articles, td_tags_title, td_tags_subtext)

    return articles