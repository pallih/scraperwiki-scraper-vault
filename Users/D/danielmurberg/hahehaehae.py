import scraperwiki

search = scraperwiki.swimport('twitter_search_extended').search

search(['olympics', 'hej'], num_pages=5)

