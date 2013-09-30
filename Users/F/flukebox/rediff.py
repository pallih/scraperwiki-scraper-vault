import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

def bootstrap(soup):
    img = soup.findAll("img", {"id":"zoomImage"})[0]
    imgsrc= img["src"]
    br.open(imgsrc)
    soup = BeautifulSoup(br.response().read())
    print soup

base_url = 'http://shopping.rediff.com/product/lemon-/-nimboo/10411212'
br = mechanize.Browser()

# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(base_url)
soup = BeautifulSoup(br.response().read())
# Have a look at 'soup': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.
print soup 
# start scraping
bootstrap(soup)
import scraperwiki
import mechanize
from BeautifulSoup import BeautifulSoup

def bootstrap(soup):
    img = soup.findAll("img", {"id":"zoomImage"})[0]
    imgsrc= img["src"]
    br.open(imgsrc)
    soup = BeautifulSoup(br.response().read())
    print soup

base_url = 'http://shopping.rediff.com/product/lemon-/-nimboo/10411212'
br = mechanize.Browser()

# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(base_url)
soup = BeautifulSoup(br.response().read())
# Have a look at 'soup': note the 'onSubmit' JavaScript function that is called when 
# you click on the 'next' link. We'll mimic this in the function above.
print soup 
# start scraping
bootstrap(soup)
