from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy_canadian_budgets.items import Table, Summary
from scrapy_canadian_budgets.spiders.ontario_budget_spider import OntarioBudgetSpider

class Ontario2012BudgetSpider(OntarioBudgetSpider):
	name				= "ontario_2012_budget"
	start_urls 	= ["http://www.fin.gov.on.ca/en/budget/ontariobudgets/2012/papers_all.html"]
	rules				= [
		Rule(SgmlLinkExtractor(allow=(r'en/budget/ontariobudgets/2012/ch[0-9][A-Za-z]?\.html?')), callback='parse_tables', follow=True)
	]