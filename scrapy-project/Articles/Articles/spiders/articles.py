import scrapy

from Articles.items import ArticlesItem
from Articles.utils import convert_ago_to_date


class ArticlesSpider(scrapy.Spider):
    name = "articles"
    allowed_domains = ["https://news.ycombinator.com/news"]
    start_urls = ["https://news.ycombinator.com/news"]

    def parse(self, response):
        articles = []
        rows = response.xpath("//table[@class='itemlist']/tr")
        i = 0
        for row in rows:
            str_row = str(row)
            if 'class="athing"' in str_row:
                item = ArticlesItem()
                item["id"] = row.xpath("@id").extract_first()

                td_tag = row.xpath("td[@class='title']")

                item["title"] = td_tag.xpath(
                                            "a[@class='storylink']/text()").extract_first()

                item["content_url"] = td_tag.xpath(
                                                "a[@class='storylink']/@href").extract_first()

                articles.append(item)

            elif ('class="morespace"' not in str_row
                    and 'class="spacer"' not in str_row
                    and i < 30):
                item = articles[i]
                td_tag = row.xpath("td[@class='subtext']")

                item["points"] = td_tag.xpath(
                                            "span[@class='score']/text()").extract_first()

                item["created_date"] = convert_ago_to_date(
                                                td_tag
                                                    .xpath("span[@class='age']/a/text()")
                                                        .extract_first())

                item["author"] = td_tag.xpath(
                                            "a[@class='hnuser']/text()").extract_first()

                item["number_comments"] = td_tag.xpath(
                                            "span[@class='score']/text()").extract_first()

                i += 1

        for article in articles:
            yield article
