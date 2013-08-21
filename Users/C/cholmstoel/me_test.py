import scraperwiki

search = scraperwiki.swimport('twitter_search_extended').search

search(['hyper%20island'], num_pages=5)

