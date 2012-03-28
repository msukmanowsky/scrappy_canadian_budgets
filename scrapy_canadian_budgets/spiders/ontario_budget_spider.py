from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy_canadian_budgets.items import Table, Summary

class OntarioBudgetSpider(CrawlSpider):
	
	allowed_domains = ["www.fin.gov.on.ca"]
	'''
	The following values are defined in inheriting subclasses
	start_urls 			= ["http://www.fin.gov.on.ca/en/budget/ontariobudgets/2011/papers_all.html"]
	rules						= [
		Rule(SgmlLinkExtractor(allow=(r'en/budget/ontariobudgets/2011/ch[0-9][A-Za-z]\.html?')), callback='parse_tables', follow=True)
	]
	'''
	
	def parse_tables(self, response):
		items = []
		summaries = []
		tables = []
		hxs = HtmlXPathSelector(response)
		
		# First we'll extract all the tables
		raw_tables = hxs.select("//table")
		for raw_table in raw_tables:
			table = Table()
			table["caption"] = raw_table.select("caption/text()").extract()
			
			footnote = raw_table.select("following-sibling::div[@class='footnote'][1]/text()").extract()
			if len(footnote) == 0:
				table["footnote"] = ""
			else:
				table["footnote"] = footnote[0]
			
			table["data"] = []
			rows = raw_table.select(".//tr")
			for i,row in enumerate(rows):
				table["data"].append([])
				cells = row.select(".//th/text()|.//td/text()")
				for cell in cells:
					table["data"][i].append(cell.extract())
			tables.append(table)
			
		items.extend(tables)
		self.log("Found %d tables in %s." % (len(tables), response.url))
		
		# Now we'll extract all the summaries
		for heading in hxs.select("//h3"):
			summary = Summary()
			try:
				summary["heading"] = heading.select("text()").extract()[0]
			except IndexError:
				print heading
				summary["heading"] = ""
			summary["bullets"] = []
			
			bullets = heading.select("following-sibling::ul[1]/li/text()")
			if len(bullets) == 0:
				continue
			for bullet in bullets:
				summary["bullets"].append(bullet.extract())
			
			summaries.append(summary)
		
		self.log("Found %d summaries in %s" % (len(summaries), response.url))
		items.extend(summaries)
		
		return items