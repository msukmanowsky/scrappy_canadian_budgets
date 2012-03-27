# Scrapy settings for scrapy_budget_2012 project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'scrapy_budget_2012'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['scrapy_canadian_budgets.spiders']
NEWSPIDER_MODULE = 'scrapy_canadian_budgets.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
ITEM_PIPELINES = ['scrapy_canadian_budgets.pipelines.OntarioBudgetPipeline']

