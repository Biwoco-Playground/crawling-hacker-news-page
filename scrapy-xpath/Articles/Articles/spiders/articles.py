import scrapy

from Articles.items import ArticlesItem
from Articles.utils import convert_ago_to_date, clean_number_comments, clean_points


class ArticlesSpider(scrapy.Spider):
    name = "articles"
    allowed_domains = ["ycombinator.com"]
    start_urls = ["https://news.ycombinator.com/news"]

    def parse(self, response):
        articles = []
        articles_append = articles.append
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

                articles_append(item)

            elif ('class="morespace"' not in str_row
                    and 'class="spacer"' not in str_row
                    and 'class="title"' not in str_row):
                item = articles[i]
                td_tag = row.xpath("td[@class='subtext']")

                points = clean_points(
                                    td_tag.xpath(
                                            "span[@class='score']/text()").extract_first())
                item["points"] = points

                item["created_date"] = convert_ago_to_date(
                                                        td_tag
                                                            .xpath("span[@class='age']/a/text()")
                                                                .extract_first())

                item["author"] = td_tag.xpath(
                                            "a[@class='hnuser']/text()").extract_first()

                try:
                    number_comments = clean_number_comments(
                                                    td_tag.xpath(
                                                        "a/text()").extract()[2])
                except:
                    number_comments = 0                    
                item["number_comments"] = number_comments

                i += 1

        for article in articles:
            yield article

        next_page = rows.xpath(
                                "td[@class='title']/a[@class='morelink']/@href").extract_first()
        if next_page:
            next_url = 'https://news.ycombinator.com/' + next_page
            print("Next Page URL: ", next_url)
            yield scrapy.Request(next_url, callback = self.parse)