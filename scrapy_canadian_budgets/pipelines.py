import pymongo
import re
from scrapy.conf import settings
from scrapy_canadian_budgets.items import Table, Summary
from scrapy_canadian_budgets.spiders.ontario_2011_budget_spider import Ontario2011BudgetSpider
from scrapy_canadian_budgets.spiders.ontario_2012_budget_spider import Ontario2012BudgetSpider

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

class MongoDBPipeline(object):
	def __init__(self):
		connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
		self.db = connection[settings['MONGODB_DB']]
		self.db.authenticate(settings['MONGODB_USERNAME'], settings['MONGODB_PASSWORD'])
		self.db.drop_collection('ontario_2012_budget_summary')
		self.db.drop_collection('ontario_2012_budget_sable')
		self.db.drop_collection('ontario_2011_budget_summary')
		self.db.drop_collection('ontario_2011_budget_sable')
		
	
	def process_item(self, item, spider):
		cleaned_item = self.clean_item(item, spider)
		collection_name = '_'.join([spider.name, cleaned_item.__class__.__name__]).lower()
		collection = self.db[collection_name]
		collection.insert(dict(cleaned_item))
	
	def clean_item(self, item, spider):
		if type(item) == Table:
			item["caption"] = self.clean_html(item["caption"])
			item["footnote"] = self.clean_html(item["footnote"])
		elif type(item) == Summary:
			item["heading"] = self.clean_html(item["heading"])
			item["bullets"] = [re.sub(r'\s+', r' ', s) for s in item["bullets"]]
				
		return item
	
	def clean_html(self, bad_html):
		if type(bad_html) == str:
			return bad_html
		
		s = bad_html
		s = re.sub(r'<.*?>', r'', s)
		s = re.sub(r'\s+', r' ', s)
		return s

class OntarioBudgetPipeline(object):
	def process_item(self, item, spider):
		if type(spider) == Ontario2011BudgetSpider or type(spider) == Ontario2012BudgetSpider:
			return self.process_ontario(item, spider)
		else:
			return item
	
	def process_ontario(self, item, spider):
		if type(item) == Table:
			item["caption"] = self.clean_html(item["caption"])
			item["footnote"] = self.clean_html(item["footnote"])
		elif type(item) == Summary:
			item["heading"] = self.clean_html(item["heading"])
			item["bullets"] = [re.sub(r'\s+', r' ', s) for s in item["bullets"]]
				
		return item
	
	@staticmethod
	def clean_html(bad_html):
		if type(bad_html) == str:
			return bad_html
		
		s = bad_html
		s = re.sub(r'<.*?>', r'', s)
		s = re.sub(r'\s+', r' ', s)
		return s
