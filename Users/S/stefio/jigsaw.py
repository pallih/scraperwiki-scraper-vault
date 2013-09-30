import scraperwiki,re
from BeautifulSoup import BeautifulSoup

starting_url = 'http://www.jigsaw-online.com/fcp/content/all-stores/content'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)
record = {}

stores = soup.findAll("a")
print stores
for store in stores:
    print store
    link = store.get("href")
    id = store.get("id")
    class_found = store.get("class")
    print link
    if not (link is None) and (id is None) and (class_found is None):
        specific_url = 'http://www.jigsaw-online.com' + link
        try: 
            html2 = scraperwiki.scrape(specific_url)
        except:
            print "Page not found"
        else:
            soup2 = BeautifulSoup(html2)
            print html2
    
            address = soup2.find("span", { "class" : "postcode" })
            
            if not (address is None):
                print address.getText
                record['title'] = store.get("title")
                record['address'] = address.getText()
                scraperwiki.sqlite.save(['title'], record)import scraperwiki,re
from BeautifulSoup import BeautifulSoup

starting_url = 'http://www.jigsaw-online.com/fcp/content/all-stores/content'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)
record = {}

stores = soup.findAll("a")
print stores
for store in stores:
    print store
    link = store.get("href")
    id = store.get("id")
    class_found = store.get("class")
    print link
    if not (link is None) and (id is None) and (class_found is None):
        specific_url = 'http://www.jigsaw-online.com' + link
        try: 
            html2 = scraperwiki.scrape(specific_url)
        except:
            print "Page not found"
        else:
            soup2 = BeautifulSoup(html2)
            print html2
    
            address = soup2.find("span", { "class" : "postcode" })
            
            if not (address is None):
                print address.getText
                record['title'] = store.get("title")
                record['address'] = address.getText()
                scraperwiki.sqlite.save(['title'], record)