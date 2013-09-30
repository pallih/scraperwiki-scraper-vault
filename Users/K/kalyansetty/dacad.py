from mechanize import Browser
from BeautifulSoup import BeautifulSoup

mech = Browser()
url = "http://www.palewire.com/scrape/albums/2007.html"
page = mech.open(url)

html = page.read()
soup = BeautifulSoup(html)
table = soup.find("table", border=1)

for row in table.findAll('tr')[1:]:
    col = row.findAll('td')
    rank = col[0].string
    artist = col[1].string
    album = col[2].string
    cover_link = col[3].img['src']
    record = (rank, artist, album, cover_link)
    print "|".join(record)from mechanize import Browser
from BeautifulSoup import BeautifulSoup

mech = Browser()
url = "http://www.palewire.com/scrape/albums/2007.html"
page = mech.open(url)

html = page.read()
soup = BeautifulSoup(html)
table = soup.find("table", border=1)

for row in table.findAll('tr')[1:]:
    col = row.findAll('td')
    rank = col[0].string
    artist = col[1].string
    album = col[2].string
    cover_link = col[3].img['src']
    record = (rank, artist, album, cover_link)
    print "|".join(record)