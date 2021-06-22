from article_services import parse_hacker_news_pages
from utils import init_results_dir, calculate_compiling_time
from timeit import default_timer

if __name__ == "__main__":
    start_time = default_timer()
    init_results_dir()
    start_page = 1
    end_page = 20
    parse_hacker_news_pages(start_page, end_page)
    calculate_compiling_time(start_time)
    
