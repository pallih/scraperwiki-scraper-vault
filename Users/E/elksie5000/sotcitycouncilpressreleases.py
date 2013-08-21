import scraperwiki
import lxml.html
# First step

#//*[@id="main-content"]/div[1]/div[1]/ul


base_url = "http://www.stoke.gov.uk/ccm/navigation/news/latest-news-2011/2011-01-january/"

test_article = "http://www.stoke.gov.uk/ccm/content/council-and-democracy/communications/2011-press-releases/01-2011/001-11.en"


def scrape_page (url):
    print "Page scraping: "+url
    if scraperwiki.scrape(url) !="": 
  
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        stories = root.cssselect('div.frame-inner-content.icon-list a.event')
        for story in stories:
            uri = story.attrib['href']
            url_scrape = base+uri
            scrape_article(url_scrape)


def scrape_article(url):
    print "Scraping: "+ url
    record = {}
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    record['url'] = url
    headline = root.xpath('//*[@id="main-content"]/div[2]/h2')
    record['headline'] = headline[0].text_content()
    body =  root.xpath('//*[@id="page-content"]/div[2]')
    body_string = lxml.html.tostring(body[0])
    #Get rid of the div tag
    body_string = body_string.replace('<div class="body-text">', "")
    body_string = body_string.replace('</div>', "")
    body_string = body_string.replace('class="bold"', "")
    print body_string
    record['body'] = body_string
    scraperwiki.sqlite.save(['url'], record) 


html = scraperwiki.scrape(base_url)
root = lxml.html.fromstring(html)
link_box = root.xpath('//*[@id="main-content"]/div[1]/div[1]/ul')
links = link_box[0].cssselect("a")
print len(links)
print lxml.html.tostring(links[0])

base = "http://www.stoke.gov.uk"
second_bit = "/ccm/navigation/news/latest-news-2011/"
len_uri = len(second_bit)



for link in links:
    link_url =  link.attrib['href']
    if link_url[len_uri:] != "":
        url = base+link_url
        print url
        scrape_page(url)


