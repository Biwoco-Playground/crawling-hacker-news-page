from utils import calculate_compiling_time, init_results_dir
from article_services import parse_hacker_news_pages
from timeit import default_timer

if __name__ == "__main__":
    init_results_dir()
    start_time = default_timer()
    start_page = 1
    end_page = 4
    parse_hacker_news_pages(start_page, end_page)
    calculate_compiling_time(start_time)