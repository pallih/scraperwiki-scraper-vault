import scraperwiki
import lxml.html
import urlparse

html = scraperwiki.scrape("http://metmuseum.org/collections/search-the-collections?&noqs=true&od=on&ft=*&deptids=21&what=Paintings&pg=1")
rootGallery = lxml.html.fromstring(html)

startLink = rootGallery.cssselect("div.centre-y a")[0].attrib['href']           


def scrape_page(root):
    
    try:
        venue = "The Metropolitan Museum of Art"

        
        id = root.cssselect("div#main-container form")[2].attrib['action'].strip()


        import unicodedata
        def strip_accents(s):
            return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

        try:
            title = root.cssselect("h2")[1].text
            unicode(title)
            title = strip_accents(title)
            title = title.encode('utf-8').strip('[]')
        except:
            title = root.cssselect("h2")[1].text.strip('[]')
            
                
        for el in root.cssselect("dd.cleared")[1]:
            materialList = lxml.html.tostring(el)
        material = lxml.html.fromstring(materialList).text_content()
        from string import maketrans   
        intab = "1234567890(),\r\n\t"
        outtab = "                "
        trantab = maketrans(intab, outtab)
        str = material;
        material = str.translate(trantab);
        material = material.split()
            


        try:
            artist = root.cssselect("dd.cleared a")[0].text
            unicode(artist)
            artist = strip_accents(artist)
            artist = artist.encode('utf-8').strip()
        except:
            artist = root.cssselect("dd.cleared a")[0].text.strip()


        try:
            displayLoc = root.cssselect("p.gallery-id a")[0].text[8:11]#.split()[-1].splitlines()
        except:
            displayLoc = root.cssselect("p.gallery-id")[0].text[48:51]#.split()[-1].splitlines()
            
        
        for el in root.cssselect("div.image-container img"):
            imgSrc = el.attrib['src'].strip().replace(" ","%20")
                                 
            
            data = {
            'id' : id,
            'title' : title,
            'artist' : artist,
            'location' : displayLoc,
            'image' : imgSrc,
            'material' : material,
            'venue' : venue
            }

        print data
        scraperwiki.sqlite.save(unique_keys=["id"], data=data)
        
    except:
        print ("error")

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