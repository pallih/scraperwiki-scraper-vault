import scraperwiki
from bs4 import BeautifulSoup

# Only to try some scraping - and it works!
# This scraper searches for .exe-files on my own site www.joostvanleeuwen.nl

mijnhtml=scraperwiki.scrape("http://www.joostvanleeuwen.nl")
mijnsoup=BeautifulSoup(mijnhtml)


# print(mijnsoup.prettify())


exefiles = mijnsoup.findAll('a')

for n in exefiles:
    print(n['href'])
















