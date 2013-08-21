import scraperwiki

search = scraperwiki.swimport('twitter_search_extended').search

search(['karlskrona'], num_pages=100)
