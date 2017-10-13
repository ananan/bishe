from scrapy.spiders import Spider
from testcase1.items import DoubanItem
from scrapy import Request

class DoubanSpider(Spider):
	name = "douban_movie_top250"
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"}
	
	def start_requests(self):
		url = "https://movie.douban.com/top250"
		yield Request(url, headers = self.headers)	

	
	def parse(self,response):
		item = DoubanItem()
		movies = response.xpath('//ol[@class="grid_view"]/li')
		for movie in movies:
			item["ranking"] = movie.xpath('.//div[@class="pic"]/em/text()').extract()[0]
			item["movie_name"] = movie.xpath('.//div[@class="hd"]/a/span[1]/text()').extract()[0]
			item["score"] = movie.xpath('.//div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
			item["score_num"] = movie.xpath('.//div[@class="star"]/span[last()]/text()').extract()[0]
			try:
				item["quote"] = movie.xpath('.//p[@class="quote"]/span/text()').extract()
			except:
				item["quote"] = "no quote !!"
			yield item
	
		next_url = response.xpath('//span[@class="next"]/a/@href').extract()
		try:	
			next_url = "https://movie.douban.com/top250"+next_url[0]
			yield Request(next_url, headers = self.headers)
		except:
			print("crawl finished !!!!!!!!")
