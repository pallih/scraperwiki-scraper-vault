import scraperwiki
import lxml.html
import lxml.etree
import urlparse
from BeautifulSoup import BeautifulSoup, NavigableString




# scrape website
url = 'http://www.thisislincolnshire.co.uk/search/search.html?searchPhrase=riots&where=&searchType=&lpCreated=August++++2011'

url_list = ("http://www.thisisbristol.co.uk", "http://www.thisiscornwall.co.uk")

search_term = "/search/search.html?searchPhrase=riots&where=&searchType=&lpCreated=August++++2011"
article = ""
base_url = 'http://www.thisislincolnshire.co.uk'

#scrape_page goes through a page of results

def scrape_page(root, base_url):
    
    rows = root.cssselect('ul.results-list h2 a')
    for row in rows:
        article_url = base_url+row.xpath('@href')[0]
        print article_url
        if "story.html" in article_url:
            article = scrape_article(base_url+row.xpath('@href')[0])
            #print row.text
            #Set up data record - to be used later
            record = {}
            record['Link'] = base_url+row.xpath('@href')[0]
            record['Headline'] = row.text
            record['Article'] = article[0]
            record['Date_pub'] = article[1]
            record['Site'] = base_url
            print record, '--------'
            scraperwiki.sqlite.save(['Headline'], record)      
        else:
            print "This is a gallery"    
            
        
             


def scrape_article(url):
    print "entered scrape_article "+url
    article_data = scraperwiki.scrape(url)
    article_root = lxml.html.fromstring(article_data)
    article = article_root.cssselect("div.story-body")
    date_pub = article_root.xpath('//meta[@property="article:published_time"]')
    date_pub = lxml.html.tostring(date_pub[0])
    date_pub = date_pub[49:74]
    article = lxml.html.tostring(article[0])
    image_box = article_root.cssselect("div.story-gallery")
    if image_box:
        image_box = lxml.html.tostring(image_box[0])
        article = article.replace(image_box, "")
    invalid_tags = ['div']
    article = strip_tags(article, invalid_tags)
    return article, date_pub

def strip_tags(html, invalid_tags):
    soup = BeautifulSoup(html)

    for tag in soup.findAll(True):
        if tag.name in invalid_tags:
            s = ""

            for c in tag.contents:
                if not isinstance(c, NavigableString):
                    c = strip_tags(unicode(c), invalid_tags)
                s += unicode(c)

            tag.replaceWith(s)

    return soup

def scrape_and_look_for_next_link(url):
    #scrape html search page
    html = scraperwiki.scrape(url)  
    print "Scrape: " +url
    #parse out the base_url from this search
    o = urlparse.urlparse(url)
    base_url = "http://"+o[1]
    print "base: ", base_url
    root = lxml.html.fromstring(html) #turn the HTML into lxml object
    scrape_page(root, base_url)
    if root.cssselect('ol.pagination li.next a'):
        print "Test passed"
        next_link = root.cssselect('ol.pagination li a')[-1] #grab the last <a from the last <li in the <ol class="pagination"
        print "next link: "+ lxml.html.tostring(next_link)
        next_link = next_link.xpath('@href')[0] #splice URL with first element of type @href 
        next_url = base_url+next_link
        text_next = root.cssselect("ol.pagination li.next a")
        print "looping"
        if text_next:
            scrape_and_look_for_next_link(next_url)
    

        
           
def main(url_list, search_term):
    sites = len(url_list)
    for el in range(sites):
        url = url_list[el]+search_term
        scrape_and_look_for_next_link(url)

main(url_list, search_term)
print "We're done!" 

 


    



