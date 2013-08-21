import scraperwiki

search = scraperwiki.swimport('twitter_search_extended').search

search(['ryanair'],num_pages=200)
