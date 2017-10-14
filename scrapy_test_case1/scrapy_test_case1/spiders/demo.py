import scrapy

class demoSpider(scrapy.Spider):
	name = "demo"
	start_urls = ["http://www.lativ.com/MEN",]
	def parse(self,response):
		title = response.xpath('//title/text()')
		name = response.xpath('//ul')
		print(title,name)
