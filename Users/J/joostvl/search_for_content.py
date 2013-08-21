import scraperwiki
from bs4 import BeautifulSoup

# Only to try some scraping - and it works!
# This scraper searches for .exe-files on my own site www.joostvanleeuwen.nl

mijnhtml=scraperwiki.scrape("https://www.omroepzeeland.nl/enquete-eenvandaag-over-pesten-op-school")
mijnsoup=BeautifulSoup(mijnhtml)


# print(mijnsoup.prettify())


exefiles = mijnsoup.findAll('table')

for n in exefiles:
    print(n['width'])
















