import scraperwiki

# Blank Python

search = scraperwiki.swimport('twitter_search_extended').search

search(['olympics'], num_pages=5)