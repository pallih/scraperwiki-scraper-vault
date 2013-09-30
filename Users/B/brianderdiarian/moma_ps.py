import scraperwiki
import lxml.html
import urlparse

html = scraperwiki.scrape("http://www.moma.org/collection/browse_results.php?criteria=O%3ADE%3AI%3A5%7CG%3AOV%3AE%3A1&template_id=6&sort_order=1&results_per_page=160&page_number=1&UC=")
rootGallery = lxml.html.fromstring(html)

startLink = rootGallery.cssselect("div.description a")[1].attrib['href']           


def scrape_page(root):
    
    #try:
        for p in root.xpath("//div[@id='omniture_caption']/h3//text()"):
            title = p

        for p in root.xpath("//h4[text()='Works: ']/following-sibling::div/a[@href]//text()"):
            artist = p

        for p in root.xpath("//h4[text()='Classification: ']/following-sibling::div/a[@href]//text()"):
            material = p

        for p in root.xpath("//h4[text()='Permalink: ']/following-sibling::div/a[@href]/@href"):
            id = p

        for p in root.xpath("//p[@id='mainImage']//@src"):
            image = p

                  
                                 
            
            data = {
            'id' : "http://www.moma.org/collection/"+id,
            'title' : title,
            'artist' : artist,
            #'location' : displayLoc,
            'image' : image,
            'material' : material,
            'venue' : "The Museum of Modern Art"
            }

        print data
        scraperwiki.sqlite.save(unique_keys=["title"], data=data)
        
    #except:
        #print ("error")

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_page(root)
        
    next_link = root.cssselect("a.next")
    
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

    gallery_url = root.cssselect("img.over")[0].attrib['src']

    print gallery_url
    
base_url = 'http://www.moma.org/collection/'
starting_url = urlparse.urljoin(base_url, startLink)
scrape_and_look_for_next_link(starting_url)import scraperwiki
import lxml.html
import urlparse

html = scraperwiki.scrape("http://www.moma.org/collection/browse_results.php?criteria=O%3ADE%3AI%3A5%7CG%3AOV%3AE%3A1&template_id=6&sort_order=1&results_per_page=160&page_number=1&UC=")
rootGallery = lxml.html.fromstring(html)

startLink = rootGallery.cssselect("div.description a")[1].attrib['href']           


def scrape_page(root):
    
    #try:
        for p in root.xpath("//div[@id='omniture_caption']/h3//text()"):
            title = p

        for p in root.xpath("//h4[text()='Works: ']/following-sibling::div/a[@href]//text()"):
            artist = p

        for p in root.xpath("//h4[text()='Classification: ']/following-sibling::div/a[@href]//text()"):
            material = p

        for p in root.xpath("//h4[text()='Permalink: ']/following-sibling::div/a[@href]/@href"):
            id = p

        for p in root.xpath("//p[@id='mainImage']//@src"):
            image = p

                  
                                 
            
            data = {
            'id' : "http://www.moma.org/collection/"+id,
            'title' : title,
            'artist' : artist,
            #'location' : displayLoc,
            'image' : image,
            'material' : material,
            'venue' : "The Museum of Modern Art"
            }

        print data
        scraperwiki.sqlite.save(unique_keys=["title"], data=data)
        
    #except:
        #print ("error")

def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_page(root)
        
    next_link = root.cssselect("a.next")
    
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

    gallery_url = root.cssselect("img.over")[0].attrib['src']

    print gallery_url
    
base_url = 'http://www.moma.org/collection/'
starting_url = urlparse.urljoin(base_url, startLink)
scrape_and_look_for_next_link(starting_url)