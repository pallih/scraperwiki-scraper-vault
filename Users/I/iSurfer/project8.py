import scraperwiki

search = scraperwiki.swimport('twitter_search_extended').search

search(['#project8'], num_pages=5)
