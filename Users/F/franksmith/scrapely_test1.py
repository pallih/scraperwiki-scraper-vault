import urllib, scraperwiki
from scrapely import Scraper

s = Scraper()                             # note how we're *not* using Scraper() - this uses our custom version
url1 = 'http://www.thefest.com/store/beatles-ornaments/the-beatles-applique-stocking-p-3901'
data = {'name': 'THE BEATLES APPLIQUE STOCKING', 'category': 'Beatles Ornaments', 'description': 'BRAND NEW- If you are good, maybe Santa will put something special in this poly/cotton applique stocking - He will have to work overtime to fill this! Measures 19" diagonally from upper left facing to the tip of the toe. This is the first Christmas Beatles Stocking ever offered!', 'price': '$20.00', 'catalog number': '7287'}
s.train(url1,data)
url2 = 'http://www.thefest.com/store/beatles-ornaments/yellow-submarines-light-set-p-3876'
print s.scrape(url2)