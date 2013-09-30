# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/

import scraperwiki
import lxml.html
from dateutil.parser import parse as dateparse

gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("6a95690d3cd44fc2b7fd1d37a63e605d", "I000056")

pr_page = scraperwiki.scrape('http://issa.house.gov/index.php?option=com_content&view=category&layout=blog&id=22&Itemid=28&flt_m=&flt_y=2012')
root = lxml.html.fromstring(pr_page)

container = root.get_element_by_id('idGtReportDisplay')
container.make_links_absolute('http://issa.house.gov/')

links = container.iterlinks()

#needs pagination back through older press releases?

for l in links:
    url = l[2]
    pr = scraperwiki.scrape(url)
    pr_root = lxml.html.fromstring(pr)
    
    title = pr_root.find_class('section')[0].text_content()
    date = dateparse(pr_root.find_class('createdate')[0].text_content())
    content = pr_root.find_class('article_content')[0].text_content()

    gasp.add_press_release(title, date, content)

gasp.finish()
# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/

import scraperwiki
import lxml.html
from dateutil.parser import parse as dateparse

gasp_helper = scraperwiki.utils.swimport("gasp_helper")
gasp = gasp_helper.GaspHelper("6a95690d3cd44fc2b7fd1d37a63e605d", "I000056")

pr_page = scraperwiki.scrape('http://issa.house.gov/index.php?option=com_content&view=category&layout=blog&id=22&Itemid=28&flt_m=&flt_y=2012')
root = lxml.html.fromstring(pr_page)

container = root.get_element_by_id('idGtReportDisplay')
container.make_links_absolute('http://issa.house.gov/')

links = container.iterlinks()

#needs pagination back through older press releases?

for l in links:
    url = l[2]
    pr = scraperwiki.scrape(url)
    pr_root = lxml.html.fromstring(pr)
    
    title = pr_root.find_class('section')[0].text_content()
    date = dateparse(pr_root.find_class('createdate')[0].text_content())
    content = pr_root.find_class('article_content')[0].text_content()

    gasp.add_press_release(title, date, content)

gasp.finish()
