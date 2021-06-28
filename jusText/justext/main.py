import utils
import requests
import article_services


if __name__ == '__main__':
    utils.init_results_dir()
    requests_session = requests.Session()
    # url = "https://vnexpress.net/bo-truong-tai-chinh-gan-du-tien-tiem-vaccine-cho-75-trieu-dan-4299554.html"
    # url = "http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/"
    # url = "https://tuoitre.vn/chieu-25-6-ca-nuoc-them-102-ca-covid-19-tp-hcm-co-nhieu-ca-mac-cho-bo-y-te-cong-bo-20210625181028187.htm"
    # url = "https://vietnamnet.vn/vn/suc-khoe/ca-covid-19-phia-nam-phat-benh-chi-sau-hon-30-gio-tiep-xuc-750859.html"
    url = "https://vtc.vn/phat-30-thang-tu-cuu-trung-uy-cong-an-thu-sung-lam-chet-nam-sinh-vien-ar621012.html"
    response = utils.clone_page(requests_session, url)

    str_html = article_services.preprocess(response.text)
    main_content = article_services.divide_blocks(str_html)
    