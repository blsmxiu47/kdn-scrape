# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import XPathItemLoader
from scrapy.loader.processors import Join, MapCompose
import re
import datetime

import kdn_articles.items as items


class KdnSpyderSpider(scrapy.Spider):
	name = 'kdn_spyder'
	allowed_domains = ['kdnuggets.com']
	start_urls = ['https://www.kdnuggets.com/2020/03/odsc-2020-global-virtual-conference.html']

	# kdn_spyder.py
	def parse(self, response):
		selector = Selector(response)

		# Create Item object
		item = items.KdnArticlesItem()
			

		# Date Published
		pubdate_comment = response.xpath(
			".//div[@class='main_wrapper']/comment()").extract_first()
		pub_date = re.search("\d{1,}-..., \d{4}", pubdate_comment).group(0)
		pub_date = datetime.datetime.strptime(pub_date, "%d-%b, %Y")
		item['date_published'] = pub_date.strftime("%Y-%m-%d")

		# Title
		item['title'] = selector.xpath(
			".//h1[@id='title']/text()").extract_first()
		
		# Author
		# Sometimes there just isn't an author, but the below are possible formats if it exists
		# Author Info
		# often there is no author info, but this'll catch the text around author when it exists

		# Simplest, only very recent articles
		author = selector.xpath(".//div[@class='author-link']/b/a/text()").extract()
		if author:
			author_info = selector.xpath(".//div[@class='author-link']/b/text()").extract()
		# 2015 ~ 2020, mostly
		else:
			author = selector.xpath(".//div[@id='post-']/p[1]/b/a/text()").extract()
			author_info = selector.xpath(".//div[@id='post-']/p[1]/b/text()").extract()
		# Accounting for multiple authors
		if author:
			if len(author) > 1:
				author = ', '.join(author)
			else:
				author = ''.join(author)
		if author_info:
			author_info = ''.join(author_info)

		item['author'] = author
		item['author_info'] = author_info

		# Tags 
		item['tags'] = ', '.join(selector.xpath(".//div[@class='tag-data']/a/text()").extract())

		# Article summary/excerpt
		item['excerpt'] = selector.xpath(
			".//p[@class='excerpt']/text()").extract_first().strip()

		# Full article body
		item['post_text'] = ''.join(selector.xpath(".//div[@id='post-']//text()").extract()).strip()

		# Article page URL
		item['url'] = response.request.url

		yield item


		prev_page = response.xpath(".//div[@class='pagi-left']").css("a::attr(href)").extract_first()
		if prev_page:
			yield scrapy.Request(
				url=response.urljoin(prev_page),
				callback=self.parse
			)