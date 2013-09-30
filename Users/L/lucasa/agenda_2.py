import scraperwiki
import lxml.html           
import BeautifulSoup

data = "28/05/2011"
html = scraperwiki.scrape("http://www.queb.com.br/agenda.php?tp=6&dt="+data)
#print html

soup = BeautifulSoup.BeautifulSoup(html)
divs = soup.findAll('div', {"class" : "tbgal01", "style" : "padding-left:20px"})
for div in divs:
    print divimport scraperwiki
import lxml.html           
import BeautifulSoup

data = "28/05/2011"
html = scraperwiki.scrape("http://www.queb.com.br/agenda.php?tp=6&dt="+data)
#print html

soup = BeautifulSoup.BeautifulSoup(html)
divs = soup.findAll('div', {"class" : "tbgal01", "style" : "padding-left:20px"})
for div in divs:
    print div