# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Summary(Item):
	heading		= Field()
	bullets		= Field()

class Table(Item):
	caption		= Field()
	data			= Field()
	footnote 	= Field()