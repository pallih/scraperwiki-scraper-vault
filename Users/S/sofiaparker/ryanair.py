import scraperwiki

search = scraperwiki.swimport('twitter_search_extended').search

search (['ryanair'], ['webpage'] , num_pages=5)


