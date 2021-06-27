import utils
import requests
import article_services
import stopwords_manager

from models import BuildingBlocksParser


if __name__ == '__main__':
    utils.init_results_dir()
    requests_session = requests.Session()
    # url = "https://vnexpress.net/bo-truong-tai-chinh-gan-du-tien-tiem-vaccine-cho-75-trieu-dan-4299554.html"
    # url = "http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/"
    url = "https://tuoitre.vn/chieu-25-6-ca-nuoc-them-102-ca-covid-19-tp-hcm-co-nhieu-ca-mac-cho-bo-y-te-cong-bo-20210625181028187.htm"
    response = utils.clone_page(requests_session, url)

    str_html = article_services.preprocess(response.text)

    parser = BuildingBlocksParser()
    parser.feed(str_html)

    print(parser.language)
    with open("results/content.txt", "w") as f:
        f.write(
                utils.normalize_whitespace(
                                            str(parser.parts)))