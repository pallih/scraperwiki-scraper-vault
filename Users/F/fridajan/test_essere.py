import scraperwiki

search = scraperwiki.swimport('twitter_search_extended').search

search(['essere'], num_pages=5)