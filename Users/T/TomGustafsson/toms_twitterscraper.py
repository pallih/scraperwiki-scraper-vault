import scraperwiki

search = scraperwiki.swimport('twitter_search_extended').search

search(['Idle2active'], num_pages=5)
