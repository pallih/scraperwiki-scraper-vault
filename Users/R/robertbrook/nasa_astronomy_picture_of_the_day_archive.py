import scraperwiki
from BeautifulSoup import BeautifulSoup

starting_url = 'http://apod.nasa.gov/apod/archivepix.html'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

a_s = soup.findAll('a') 
for a in a_s:
    date = a.previousSibling[:-3]
    
    if len(date) > 1:
        more_soup = BeautifulSoup(scraperwiki.scrape("http://apod.nasa.gov/apod/" + a['href']))
        more_img = more_soup.find('img')
        if more_img:
            record = { "a" : a.text, "image" : "http://apod.nasa.gov/apod/" + more_img['src'], "date" : a.previousSibling[:-3]}
            scraperwiki.sqlite.save(["a"], record) 
    