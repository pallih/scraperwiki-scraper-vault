import scraperwiki
from BeautifulSoup import BeautifulSoup

starting_url = 'http://beehive.uwaterloo.ca/etc/wwwowwwws.prev.html'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

a_s = soup.findAll('a') 
for a in a_s:

    href = a['href'] if a.has_key('href') else ""

    text = a.text if a.text else ""

    record = { "text" : text, "href" : href }
    scraperwiki.sqlite.save(["text"], record) 
    import scraperwiki
from BeautifulSoup import BeautifulSoup

starting_url = 'http://beehive.uwaterloo.ca/etc/wwwowwwws.prev.html'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

a_s = soup.findAll('a') 
for a in a_s:

    href = a['href'] if a.has_key('href') else ""

    text = a.text if a.text else ""

    record = { "text" : text, "href" : href }
    scraperwiki.sqlite.save(["text"], record) 
    