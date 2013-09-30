import scraperwiki

import mechanize

# Blank Python



response2 = mechanize.urlopen('http://stats.nba.com/scores.html')

print response2.geturl()
print response2.info()  # headers
print response2.read()  # body (readline and readlines work too)
