import scrapy

from Articles.items import ArticlesItem

class ArticlesSpider(scrapy.Spider):
    name = 'articles'
    allowed_domains = ['https://news.ycombinator.com/news']
    start_urls = ['https://news.ycombinator.com/news']

    def parse(self, response):
        rows = response.xpath("//tr[@class='athing']")
        for row in rows:
            item = ArticlesItem()
            item['id'] = row.xpath("/@id").extract_first()
            yield item
        pass
