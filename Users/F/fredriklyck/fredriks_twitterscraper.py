import scraperwiki

search = scraperwiki.swimport('twitter_search_extended').search

search(['fredrik lyck'], num_pages=5)

