import scraperwiki
import lxml.html
import urlparse

html = scraperwiki.scrape("http://metmuseum.org/collections/search-the-collections?deptids=19%7c44&amp;ft=*&amp;od=on&amp;noqs=true")
rootGallery = lxml.html.fromstring(html)

startLink = rootGallery.cssselect("div.centre-y a")[0].attrib['href']           


def scrape_page(root):
    
    #try:
        import unicodedata
        def strip_accents(s):
            return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

        

            

        for p in root.xpath("//dt[text()='Who']/following-sibling::dd[1]/*/*/*/text()"):
            artist = p

        for p in root.xpath("//dt[text()='What']/following-sibling::dd[1]/*/*[1]/*/text()"):
            material = p.lstrip()

        for p in root.xpath("//div[@class='text-box first cleared ']/h2/text()"):
            title = p        

        for p in root.xpath("//form[@method='post']/@action"):
            id = p
        
        
        try:
            unicode(title)
            title = strip_accents(title)
            title = title.encode('utf-8').strip('[]')
        except:
            title = title.strip('[]')

        try:
            unicode(artist)
            artist = strip_accents(artist)
            artist = artist.encode('utf-8').strip('[]').lstrip()
        except:
            artist = artist.strip('[]').lstrip()
        





        #for p in root.xpath("//div[@class='image-container hero inline']/*//@src"):
        #    image = p

        #id = root.cssselect("div#main-container form")[2].attrib['action'].strip()



        try:
            displayLoc = root.cssselect("p.gallery-id a")[0].text[8:11]#.split()[-1].splitlines()
        except:
            displayLoc = root.cssselect("p.gallery-id")[0].text[48:51]#.split()[-1].splitlines()
            
        
        for el in root.cssselect("div.image-container img"):
            image = el.attrib['src'].replace(" ","%20").strip()
                                 
            
            data = {
            'id' : "http://www.metmuseum.org"+id,
            'title' : title,
            'artist' : artist,
            'location' : displayLoc,
            'image' : image,
            'material' : material,
            'venue' : "The Metropolitan Museum of Art"
            }

        print data
        scraperwiki.sqlite.save(unique_keys=["id"], data=data)

        

        
    #except:
    #    print ("error")

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_page(root)
        
    next_link = root.cssselect("li.next a")
    
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

def find_gallery_url(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_page(root)

    gallery_url = root.cssselect("div.centre-y a")

    print gallery_url
    
base_url = 'http://www.metmuseum.org'
starting_url = urlparse.urljoin(base_url, startLink)
scrape_and_look_for_next_link(starting_url)

scraperwiki.sqlite.attach("frick")
print scraperwiki.sqlite.select("* from frick.swdata limit 2")import scraperwiki
import lxml.html
import urlparse

html = scraperwiki.scrape("http://metmuseum.org/collections/search-the-collections?deptids=19%7c44&amp;ft=*&amp;od=on&amp;noqs=true")
rootGallery = lxml.html.fromstring(html)

startLink = rootGallery.cssselect("div.centre-y a")[0].attrib['href']           


def scrape_page(root):
    
    #try:
        import unicodedata
        def strip_accents(s):
            return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

        

            

        for p in root.xpath("//dt[text()='Who']/following-sibling::dd[1]/*/*/*/text()"):
            artist = p

        for p in root.xpath("//dt[text()='What']/following-sibling::dd[1]/*/*[1]/*/text()"):
            material = p.lstrip()

        for p in root.xpath("//div[@class='text-box first cleared ']/h2/text()"):
            title = p        

        for p in root.xpath("//form[@method='post']/@action"):
            id = p
        
        
        try:
            unicode(title)
            title = strip_accents(title)
            title = title.encode('utf-8').strip('[]')
        except:
            title = title.strip('[]')

        try:
            unicode(artist)
            artist = strip_accents(artist)
            artist = artist.encode('utf-8').strip('[]').lstrip()
        except:
            artist = artist.strip('[]').lstrip()
        





        #for p in root.xpath("//div[@class='image-container hero inline']/*//@src"):
        #    image = p

        #id = root.cssselect("div#main-container form")[2].attrib['action'].strip()



        try:
            displayLoc = root.cssselect("p.gallery-id a")[0].text[8:11]#.split()[-1].splitlines()
        except:
            displayLoc = root.cssselect("p.gallery-id")[0].text[48:51]#.split()[-1].splitlines()
            
        
        for el in root.cssselect("div.image-container img"):
            image = el.attrib['src'].replace(" ","%20").strip()
                                 
            
            data = {
            'id' : "http://www.metmuseum.org"+id,
            'title' : title,
            'artist' : artist,
            'location' : displayLoc,
            'image' : image,
            'material' : material,
            'venue' : "The Metropolitan Museum of Art"
            }

        print data
        scraperwiki.sqlite.save(unique_keys=["id"], data=data)

        

        
    #except:
    #    print ("error")

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_page(root)
        
    next_link = root.cssselect("li.next a")
    
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

def find_gallery_url(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_page(root)

    gallery_url = root.cssselect("div.centre-y a")

    print gallery_url
    
base_url = 'http://www.metmuseum.org'
starting_url = urlparse.urljoin(base_url, startLink)
scrape_and_look_for_next_link(starting_url)

scraperwiki.sqlite.attach("frick")
print scraperwiki.sqlite.select("* from frick.swdata limit 2")