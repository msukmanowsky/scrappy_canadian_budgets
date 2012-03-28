# Scrapy Canadian Budgets

## what is it
[Scrapy](http://scrapy.org/) spiders, pipelines and items for scraping budget release data from the provincial and federal Canadian government websites.

Currently, it has one spider created to scrape Ontario 2011 budget data but the hope is that others can quickly contribute other spiders, pipelines and items.

## usage
Assuming you have installed [scrapy](http://scrapy.org), first add a `settings.py` file under `scrapy_canadian_budgets` which should look something like this:

    BOT_NAME 					= 'scrapy_canadian_budgets'
    BOT_VERSION 			= '1.0'

    SPIDER_MODULES 		= ['scrapy_canadian_budgets.spiders']
    NEWSPIDER_MODULE 	= 'scrapy_canadian_budgets.spiders'
    USER_AGENT 			= '%s/%s' % (BOT_NAME, BOT_VERSION)
    #ITEM_PIPELINES 	= ['scrapy_canadian_budgets.pipelines.OntarioBudgetPipeline']
    ITEM_PIPELINES 		= ['scrapy_canadian_budgets.pipelines.MongoDBPipeline']

    MONGODB_SERVER 		= "localhost"
    MONGODB_PORT		= 123456
    MONGODB_DB			= "playground"
    MONGODB_USERNAME 	= "username"
    MONGODB_PASSWORD 	= "password"

Notice that I'm using the MongoDBPipeline above as opposed to the OntarioBudgetPipeline which should be used for JSON output.  This file has been removed from the project as it contains MongoDB details.  

Assuming you want a JSON output (e.g. `ITEM_PIPELINES = ['scrapy_canadian_budgets.pipelines.OntarioBudgetPipeline']`), you can use the Ontario 2012 Budget spider by running:

    scrapy crawl ontario_2012_budget -o ontario_2011.json -t json

This output will be a collection of either `Table` or `Summary` items.

`Table` items have three fields: 

* `caption` - the caption of the data table (usually provides a good description of what's in there)
* `data` - a 2x2 matrix with all the data in the table
* `footnote` - a footnote (if included) at the bottom of the table to better describe some element within the data.

`Summary` items correspond to areas where the federal or provincial government are providing summary points.  They have two fields:

* `heading` - the heading of this group of summary points (taken from the `<h3>` tag)
* `bullets` - an array of all the bullet points under this summary heading

## contributing
Please feel free to create additional spiders for other provinces and federal budget information.  I've tried to keep the initial items very basic to suit any budget but this can change.