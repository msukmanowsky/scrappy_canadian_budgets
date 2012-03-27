from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy_canadian_budgets.items import Table, Summary

class Ontario2011BudgetSpider(CrawlSpider):
	name 						= "ontario_2011_budget"
	allowed_domains = ["fin.gov.on.ca", "www.fin.gov.on.ca"]
	start_urls 			= ["http://www.fin.gov.on.ca/en/budget/ontariobudgets/2011/papers_all.html"]
	# We only want URLs of the form http://www.fin.gov.on.ca/en/budget/ontariobudgets/2011/ch1a.html#c1_secA_table1
	rules						= [
		Rule(SgmlLinkExtractor(allow=(r'en/budget/ontariobudgets/2011/ch[0-9][A-Za-z]\.html?')), callback='parse_tables', follow=True)
		#Rule(SgmlLinkExtractor(allow=(r'en/budget/ontariobudgets/2011/ch2c.html?')), callback='parse_tables', follow=True)
	]
	
	def parse_tables(self, response):
		items = []
		summaries = []
		tables = []
		hxs = HtmlXPathSelector(response)
		
		# First we'll extract all the tables
		raw_tables = hxs.select("//table")
		for raw_table in raw_tables:
			table = Table()
			table["caption"] = raw_table.select("caption/text()").extract()[0]
			table["footnote"] = raw_table.select("following-sibling::div[@class='footnote'][1]/text()").extract()[0]
			
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
			summary["heading"] = heading.select("text()").extract()[0]
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