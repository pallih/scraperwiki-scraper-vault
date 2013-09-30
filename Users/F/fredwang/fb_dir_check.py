import scraperwiki
import lxml.html

import urllib2
import BeautifulSoup 

############################################################################################
# Helper function to scrape a reports list page and store records.
############################################################################################

def scrape_page(url):
    data = urllib2.urlopen(url).read()
    page = BeautifulSoup.BeautifulSoup(data)
    
    # The reports are in the body rows of the first table 
    dirs = page.findAll('li') 

    for dir in dirs:
        print dir


    for report in reports:
        fields = report.findAll('td')
        title = fields[0].find('h3')
        link = title.find('a')['href']
        title.extract()
        standfirst = fields[0].text
        
        record = { "title" : title.text,
                 "date" : fields[1].text,
                 "location" : fields[2].text,
                 "url" : link,
                  "standfirst" : standfirst,
                 "verified" : fields[3].text
                  }
        scraperwiki.datastore.save(["url"], record)
    
    return page



    
############################################################################################
# Scrape the first reports list page - this also tells us how many more pages to scrape.
############################################################################################

html = scrape_page('http://www.facebook.com/directory/pages/A')



# How many pages in total?
num_pages = int(html.find('ul', { "class" : "pager" }).findAll('li')[-1].text)

for i in range(2, num_pages+1):
    scrape_page('http://cutswatch.guardian.co.uk/ushahidi/reports?page=%s' % i)



'''
<html><body>
<h1>hi</h1>
<p class="cccc">something <strong>good</strong>
<p>Another paragraph</p>
<ul class="LLL">
  <li class="1">first</li>
  <li class="2">second</li>
  <li class="1" id="nimble">third <b>jjj</b></li>junk
</ul>
</body></html>
'''


url = "http://www.facebook.com/directory/pages/A"
samplehtml = scraperwiki.scrape(url)
root = lxml.html.fromstring(samplehtml)  # an lxml.etree.Element object

# To load directly from a url, use
#root = lxml.html.parse('http://www.google.com')

# Whenever you have an lxml element, you can convert it back to a string like so:
#print lxml.etree.tostring(root)

html = scraperwiki.scrape("https://facebook.com/directory/pages/A")
root = lxml.html.fromstring(html)
for el in root.cssselect(".fbDirectoryBoxColumnItem"):           
    print el
    print el.attrib['href']


#for link in soup.find_all("li", "fbDirectoryBoxColumnItem"):
#    print link


html = scraperwiki.scrape("https://scraperwiki.com/")
root = lxml.html.fromstring(html)
for el in root.cssselect("div.featured a"):           
    print el
    print el.attrib['href']

import scraperwiki
import lxml.html

import urllib2
import BeautifulSoup 

############################################################################################
# Helper function to scrape a reports list page and store records.
############################################################################################

def scrape_page(url):
    data = urllib2.urlopen(url).read()
    page = BeautifulSoup.BeautifulSoup(data)
    
    # The reports are in the body rows of the first table 
    dirs = page.findAll('li') 

    for dir in dirs:
        print dir


    for report in reports:
        fields = report.findAll('td')
        title = fields[0].find('h3')
        link = title.find('a')['href']
        title.extract()
        standfirst = fields[0].text
        
        record = { "title" : title.text,
                 "date" : fields[1].text,
                 "location" : fields[2].text,
                 "url" : link,
                  "standfirst" : standfirst,
                 "verified" : fields[3].text
                  }
        scraperwiki.datastore.save(["url"], record)
    
    return page



    
############################################################################################
# Scrape the first reports list page - this also tells us how many more pages to scrape.
############################################################################################

html = scrape_page('http://www.facebook.com/directory/pages/A')



# How many pages in total?
num_pages = int(html.find('ul', { "class" : "pager" }).findAll('li')[-1].text)

for i in range(2, num_pages+1):
    scrape_page('http://cutswatch.guardian.co.uk/ushahidi/reports?page=%s' % i)



'''
<html><body>
<h1>hi</h1>
<p class="cccc">something <strong>good</strong>
<p>Another paragraph</p>
<ul class="LLL">
  <li class="1">first</li>
  <li class="2">second</li>
  <li class="1" id="nimble">third <b>jjj</b></li>junk
</ul>
</body></html>
'''


url = "http://www.facebook.com/directory/pages/A"
samplehtml = scraperwiki.scrape(url)
root = lxml.html.fromstring(samplehtml)  # an lxml.etree.Element object

# To load directly from a url, use
#root = lxml.html.parse('http://www.google.com')

# Whenever you have an lxml element, you can convert it back to a string like so:
#print lxml.etree.tostring(root)

html = scraperwiki.scrape("https://facebook.com/directory/pages/A")
root = lxml.html.fromstring(html)
for el in root.cssselect(".fbDirectoryBoxColumnItem"):           
    print el
    print el.attrib['href']


#for link in soup.find_all("li", "fbDirectoryBoxColumnItem"):
#    print link


html = scraperwiki.scrape("https://scraperwiki.com/")
root = lxml.html.fromstring(html)
for el in root.cssselect("div.featured a"):           
    print el
    print el.attrib['href']

