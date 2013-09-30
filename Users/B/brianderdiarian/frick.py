import scraperwiki
import lxml.html
import urlparse

html = scraperwiki.scrape("http://collections.frick.org/view/objects/asimages/888?t:state:flow=cd53dfbf-075b-4413-b438-63da2a62d908")
rootGallery = lxml.html.fromstring(html)

startLink = rootGallery.cssselect("a.titleLink")[0].attrib['href']           


def scrape_page(root):
    
    #try:

        import unicodedata
        def strip_accents(s):
            return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
        
        for p in root.xpath("//div[@class='singledata']/em/text()"):
            title = p

        try:
            unicode(title)
            title = strip_accents(title)
            title = title.encode('utf-8').lower().capitalize()
        except:
            title = title

            artist = root.cssselect("span.artistName")[0].text

        #try:
        #    unicode(artist)
        #    artist = strip_accents(artist)
        #    artist = artist.encode('utf-8')
        #except:
        #    artist = artist
            

        #for p in root.xpath("//h4[text()='Classification: ']/following-sibling::div/a[@href]//text()"):
        #    material = p

            id = root.cssselect("a.permalink")[0].attrib['href']

                  
                                 
            
            data = {
            'id' : id,
            'title' : title,
            'artist' : artist,
            #'location' : displayLoc,
            #'image' : image,
            #'material' : material,
            'venue' : "The Frick Collection"
            }

            print data
            scraperwiki.sqlite.save(unique_keys=["id"], data=data)

    #except:
        #print ("error")

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_page(root)
        
    for el in root.cssselect("div.pagenavright a"):
        next_link = image_base_url+el.attrib['href'][12:]
    
        print next_link
        if next_link:
            scrape_and_look_for_next_link(next_link)

def find_gallery_url(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_page(root)

    gallery_url = root.cssselect("img.over")[0].attrib['src']

    print gallery_url

image_base_url = 'http://67.99.191.20/view/objects/'
base_url = 'http://collections.frick.org/view/objects/asimages/'
starting_url = urlparse.urljoin(base_url, startLink)
scrape_and_look_for_next_link(starting_url)import scraperwiki
import lxml.html
import urlparse

html = scraperwiki.scrape("http://collections.frick.org/view/objects/asimages/888?t:state:flow=cd53dfbf-075b-4413-b438-63da2a62d908")
rootGallery = lxml.html.fromstring(html)

startLink = rootGallery.cssselect("a.titleLink")[0].attrib['href']           


def scrape_page(root):
    
    #try:

        import unicodedata
        def strip_accents(s):
            return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
        
        for p in root.xpath("//div[@class='singledata']/em/text()"):
            title = p

        try:
            unicode(title)
            title = strip_accents(title)
            title = title.encode('utf-8').lower().capitalize()
        except:
            title = title

            artist = root.cssselect("span.artistName")[0].text

        #try:
        #    unicode(artist)
        #    artist = strip_accents(artist)
        #    artist = artist.encode('utf-8')
        #except:
        #    artist = artist
            

        #for p in root.xpath("//h4[text()='Classification: ']/following-sibling::div/a[@href]//text()"):
        #    material = p

            id = root.cssselect("a.permalink")[0].attrib['href']

                  
                                 
            
            data = {
            'id' : id,
            'title' : title,
            'artist' : artist,
            #'location' : displayLoc,
            #'image' : image,
            #'material' : material,
            'venue' : "The Frick Collection"
            }

            print data
            scraperwiki.sqlite.save(unique_keys=["id"], data=data)

    #except:
        #print ("error")

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_page(root)
        
    for el in root.cssselect("div.pagenavright a"):
        next_link = image_base_url+el.attrib['href'][12:]
    
        print next_link
        if next_link:
            scrape_and_look_for_next_link(next_link)

def find_gallery_url(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_page(root)

    gallery_url = root.cssselect("img.over")[0].attrib['src']

    print gallery_url

image_base_url = 'http://67.99.191.20/view/objects/'
base_url = 'http://collections.frick.org/view/objects/asimages/'
starting_url = urlparse.urljoin(base_url, startLink)
scrape_and_look_for_next_link(starting_url)