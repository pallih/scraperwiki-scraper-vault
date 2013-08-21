import scraperwiki

search = scraperwiki.swimport('twitter_search_extended').search

search(['viaplay'], num_pages=25)
