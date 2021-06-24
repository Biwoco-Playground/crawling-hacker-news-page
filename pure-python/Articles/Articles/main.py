from article_services import parse_hacker_news_pages
from utils import init_results_dir, dump_objects_to_json_file


if __name__ == "__main__":
    init_results_dir()
    start_page = 1
    end_page = 1
    articles = parse_hacker_news_pages(start_page, end_page)
    dump_objects_to_json_file(articles, "articles")