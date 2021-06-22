from article_services import parse_hacker_news_pages
from utils import init_results_dir, calculate_compiling_time, dump_objects_to_json_file
from timeit import default_timer


if __name__ == "__main__":
    start_time = default_timer()
    init_results_dir()
    start_page = 1
    end_page = 4
    articles = parse_hacker_news_pages(start_page, end_page)
    filename = "articles"
    dump_objects_to_json_file(articles, filename)
    calculate_compiling_time(start_time)
    
