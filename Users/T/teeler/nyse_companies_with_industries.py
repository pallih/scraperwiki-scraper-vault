###############################################################################
# Basic scraper
###############################################################################

import scraperwiki

starting_url = 'http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download'
csv = scraperwiki.scrape(starting_url)

# Skip the first, it's the legend.
lines = [l for l in csv.split('\n')[1:] if l]

for line in lines:

    Symbol,Name,LastSale,MarketCap,IPOyear,Sector,Industry,SummaryQuote = \
        [l.replace('"',"").strip() for l in line.split(',')][:8]

    record = {}
    record['symbol'] = Symbol
    record['name'] = Name
    record['industry'] = Industry
    record['sector'] = Sector
    scraperwiki.datastore.save(["symbol"], record)
    ###############################################################################
# Basic scraper
###############################################################################

import scraperwiki

starting_url = 'http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download'
csv = scraperwiki.scrape(starting_url)

# Skip the first, it's the legend.
lines = [l for l in csv.split('\n')[1:] if l]

for line in lines:

    Symbol,Name,LastSale,MarketCap,IPOyear,Sector,Industry,SummaryQuote = \
        [l.replace('"',"").strip() for l in line.split(',')][:8]

    record = {}
    record['symbol'] = Symbol
    record['name'] = Name
    record['industry'] = Industry
    record['sector'] = Sector
    scraperwiki.datastore.save(["symbol"], record)
    