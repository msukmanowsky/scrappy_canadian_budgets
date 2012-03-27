# Scrapy Canadian Budgets

## what is it
[Scrappy](http://scrapy.org/) spiders, pipelines and items for scraping budget release data from the provincial and federal Canadian government websites.

Currently, it has one spider created to scrape Ontario 2011 budget data but the hope is that others can quickly contribute other spiders, pipelines and items.

## usage
Assuming you have installed [scrappy](http://scrapy.org), you can use the Ontario 2011 Budget spider by running:

    scrapy crawl ontario_2011_budget -o ontario_2011.json -t json

Of course you don't have to use `ontario_2011.json` if you would like a different filename.  This output will be a collection of either `Table` or `Summary` items.

`Table` items have three fields: 

* `caption` - the caption of the data table (usually provides a good description of what's in there)
* `data` - a 2x2 matrix with all the data in the table
* `footnote` - a footnote (if included) at the bottom of the table to better describe some element within the data.

`Summary` items correspond to areas where the federal or provincial government are providing summary points.  They have two fields:

* `heading` - the heading of this group of summary points (taken from the `<h3>` tag)
* `bullets` - an array of all the bullet points under this summary heading

## contributing
Please feel free to create additional spiders for other provinces and federal budget information.  I've tried to keep the initial items very basic to suit any budget but this can change.