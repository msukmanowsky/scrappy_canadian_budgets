# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Summary(Item):
	heading		= Field()
	bullets		= Field()
	
	def __str__(self):
		return "Summary: heading='%s' with %d bullet(s)" % (self['heading'], len(self['bullets']))

class Table(Item):
	caption		= Field()
	data			= Field()
	footnote 	= Field()
	
	def __str__(self):
		if type(self['data']) == list:
			if type(self['data'][0]) == list:
				return "Table: caption='%s' with %d rows x %d cols" % (self['caption'], len(self['data']), len(self['data'][0]))
		return "Table: caption=%s" % self['caption']