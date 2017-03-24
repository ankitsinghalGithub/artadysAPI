import scrapy

class MyntraSpider(scrapy.Spider):
    name = "Myntra"
    #allowed_domains = ["myntra.com"]
    start_urls = ["http://www.myntra.com/",]

    def parse(self, response):
        hxs = scrapy.Selector(response)
        # extract all links from page
        all_links = hxs.xpath('*//a/@href').extract()
        # iterate over links
        for link in all_links:
            next_page = response.urljoin(link)
            #print ('############: ',next_page)
            yield {
                'link':response.urljoin(link)
            }
            #yield scrapy.Request(url=next_page, callback=self.parse)
