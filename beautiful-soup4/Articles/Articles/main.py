from utils import calculate_compiling_time, init_results_dir, dump_objects_to_json_file
from article_services import parse_hacker_news_pages
from timeit import default_timer


if __name__ == "__main__":
    init_results_dir()
    start_time = default_timer()
    start_page = 1
    end_page = 4
    articles = parse_hacker_news_pages(start_page, end_page)
    filename = "articles"
    dump_objects_to_json_file(articles, filename)
    calculate_compiling_time(start_time)