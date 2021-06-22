import scrapy

from Articles.items import ArticlesItem
from Articles.utils import convert_ago_to_date, clean_number_comments, clean_points

class ArticlesSpider(scrapy.Spider):
    name = 'articles'
    allowed_domains = ['ycombinator.com']
    start_urls = ['https://news.ycombinator.com/news']

    def parse(self, response):
        articles = []
        articles_append = articles.append 

        rows = response.css("table[class='itemlist'] > tr")       
        i = 0
        for row in rows:
            str_row = str(row)
            if 'class="athing"' in str_row:
                item = ArticlesItem()
                item['id'] = row.css("tr[class='athing']::attr('id')").extract_first()

                item["title"] = row.css("a[class='storylink']::text").extract_first()

                item["content_url"] = row.css("a[class='storylink']::attr(href)").extract_first()

                articles_append(item)

            elif ('class="morespace"' not in str_row
                    and 'class="spacer"' not in str_row
                    and 'class="t' not in str_row):
                item = articles[i]
                
                points = clean_points(row.css("span[class='score']::text").extract_first())
                item["points"] = points

                item["created_date"] = convert_ago_to_date(
                                                        row.css("span[class='age'] > a::text")
                                                            .extract_first())

                item["author"] = row.css("a[class='hnuser']::text").extract_first()

                number_comments = clean_number_comments(
                                                    row.css("td[class='subtext'] > a:last-child::text")
                                                        .extract_first())
                item["number_comments"] = number_comments

                i += 1

        for article in articles:
            yield article

        next_page = rows.css(
                            "td[class='title'] > a[class='morelink']::attr(href)").extract_first()
        if next_page:
            next_url = 'https://news.ycombinator.com/' + next_page
            print("Next Page URL: ", next_url)
            yield scrapy.Request(next_url, callback = self.parse)
