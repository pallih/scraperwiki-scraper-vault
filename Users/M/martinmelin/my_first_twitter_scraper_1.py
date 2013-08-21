import scraperwiki

search = scraperwiki.swimport('twitter_search_extended').search

try:
    search(['olympics'], num_pages=5)
except TypeError:
    print "Twitter API rate limited - please try again later!"