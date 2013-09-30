import itertools
import scraperwiki
import lxml.html           

def get_details(href):
    detail_html = scraperwiki.scrape(href)
    details = lxml.html.fromstring(detail_html)
    title = details.cssselect("h1")[0].text_content().strip()
    brief = details.cssselect(".content-text")[0].text_content().strip()
    return { 'title': title, 'brief': brief, 'href': href }

def scrape_projects(href):
    html = scraperwiki.scrape(webdev_href)
    root = lxml.html.fromstring(html)
    for entry in root.cssselect(".job-list .item"):    
        href = entry.cssselect(".title a[href]")[0].attrib['href']
        yield get_details(href)

webdev_href = "http://www.peopleperhour.com/freelance-jobs?minPrice=0&maxPrice=0&remote=GB&onsite=GB&sort=latest&category=35"         
software_href = "http://www.peopleperhour.com/freelance-jobs?minPrice=0&maxPrice=0&remote=GB&onsite=GB&sort=latest&category=36"         

for data in itertools.chain(scrape_projects(webdev_href), scrape_projects(software_href)):
    scraperwiki.sqlite.save(unique_keys=['href'], data=data)
import itertools
import scraperwiki
import lxml.html           

def get_details(href):
    detail_html = scraperwiki.scrape(href)
    details = lxml.html.fromstring(detail_html)
    title = details.cssselect("h1")[0].text_content().strip()
    brief = details.cssselect(".content-text")[0].text_content().strip()
    return { 'title': title, 'brief': brief, 'href': href }

def scrape_projects(href):
    html = scraperwiki.scrape(webdev_href)
    root = lxml.html.fromstring(html)
    for entry in root.cssselect(".job-list .item"):    
        href = entry.cssselect(".title a[href]")[0].attrib['href']
        yield get_details(href)

webdev_href = "http://www.peopleperhour.com/freelance-jobs?minPrice=0&maxPrice=0&remote=GB&onsite=GB&sort=latest&category=35"         
software_href = "http://www.peopleperhour.com/freelance-jobs?minPrice=0&maxPrice=0&remote=GB&onsite=GB&sort=latest&category=36"         

for data in itertools.chain(scrape_projects(webdev_href), scrape_projects(software_href)):
    scraperwiki.sqlite.save(unique_keys=['href'], data=data)
