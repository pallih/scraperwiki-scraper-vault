import scraperwiki
import lxml.html

# global settings

base_url = 'http://www.w4mpjobs.org/SearchJobs.aspx?search=alljobs'

#scrape page into new object: 'html'
html = scraperwiki.scrape(base_url)
print html


root = lxml.html.fromstring(html) # turn our HTML into an lxml object
lis = root.cssselect('ul.searchresults li') # get all the <li> tags within <ul class="searchresults">
for li in lis:
    record = {} 
    if len(li):
        record["allhtml"] = li.text_content()
        divs = li.cssselect('div div') # get all the <div><div> tags within <ul class="searchresults"><li>
        record["link"] = divs[0].text_content()
        record["location"] = divs[1].text_content()
        record["salary"] = divs[2].text_content()
        record["posted"] = divs[3].text_content()
        hrefs = li.cssselect('div div strong a') # get all the <a> tags 
        record["href"] = hrefs[0].attrib.get('href')
        scraperwiki.sqlite.save(["allhtml"],record)

import scraperwiki
import lxml.html

# global settings

base_url = 'http://www.w4mpjobs.org/SearchJobs.aspx?search=alljobs'

#scrape page into new object: 'html'
html = scraperwiki.scrape(base_url)
print html


root = lxml.html.fromstring(html) # turn our HTML into an lxml object
lis = root.cssselect('ul.searchresults li') # get all the <li> tags within <ul class="searchresults">
for li in lis:
    record = {} 
    if len(li):
        record["allhtml"] = li.text_content()
        divs = li.cssselect('div div') # get all the <div><div> tags within <ul class="searchresults"><li>
        record["link"] = divs[0].text_content()
        record["location"] = divs[1].text_content()
        record["salary"] = divs[2].text_content()
        record["posted"] = divs[3].text_content()
        hrefs = li.cssselect('div div strong a') # get all the <a> tags 
        record["href"] = hrefs[0].attrib.get('href')
        scraperwiki.sqlite.save(["allhtml"],record)

