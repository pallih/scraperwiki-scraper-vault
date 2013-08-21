import scraperwiki
from bs4 import BeautifulSoup

for i in range(1, 2):
    html_doc = "http://www.knightfoundation.org/grants/?page={0}&view=list".format(i)
    soup = BeautifulSoup(html_doc)
    print(soup.prettify())
    for link in soup.find_all('a'):
        print(link.get('href'))
