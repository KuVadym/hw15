import scrapy
from ..items import ExportToDB

class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['zakarpattya.net.ua', 'uzhgorod.net.ua']
    start_urls = ['https://zakarpattya.net.ua/', 'https://uzhgorod.net.ua/', ]
    

    def parse(self, response):
        items = ExportToDB()
        for news in response.xpath("/html//div[@class='block']/ul/li") or response.xpath("/html//table[@class='news']/tr"):
            if news:
                links = 0
                for link in news.xpath("td"):
                    links +=1
                    if links % 2 == 0:
                        y = link.xpath("a/text()").get()
                        if y:
                            items['news'] = link.xpath("a/em/text()").get() or link.xpath("a/text()").get()
                            items["link"] = [self.start_urls[0], str(link.xpath("a/@href").get())] 
                            # print(f'\n\n\n\n{y}\n\n\n\n')
                            yield items
            if news:
                y = news.xpath("a/text()").get()
                if y:
                    items['news'] = y
                    items["link"] = [self.start_urls[1], str(news.xpath("a/@href").get())]
                    yield items