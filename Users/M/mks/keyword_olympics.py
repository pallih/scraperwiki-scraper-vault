import scraperwiki

search = scraperwiki.swimport ("twitter_search_extended").search 

## swimport is a library on scraperwiki which inserts another scraper (the twitter one) ##

search(["#cjam2"], num_pages=8)

