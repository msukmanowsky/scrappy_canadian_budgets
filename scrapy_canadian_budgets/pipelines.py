import re
from scrapy_canadian_budgets.items import Table, Summary
from scrapy_canadian_budgets.spiders.ontario_2011_budget_spider import Ontario2011BudgetSpider

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

class OntarioBudgetPipeline(object):
	def process_item(self, item, spider):
		if type(spider) == Ontario2011BudgetSpider:
			return self.process_ontario_2011(item, spider)
		else:
			return item
	
	def process_ontario_2011(self, item, spider):
		if type(item) == Table:
			item["caption"] = self.clean_html(item["caption"])
			item["footnote"] = self.clean_html(item["footnote"])
		elif type(item) == Summary:
			item["heading"] = self.clean_html(item["heading"])
			item["bullets"] = [re.sub(r'\s+', r' ', s) for s in item["bullets"]]
				
		return item
	
	@staticmethod
	def clean_html(bad_html):
		if bad_html is not str:
			return bad_html
		
		s = bad_html
		s = re.sub(r'<.*?>', r'', s)
		s = re.sub(r'\s+', r' ', s)
		return s
