import scraperwiki
import lxml.html
import urlparse

# This scraper is programmed as part of a research project.
# For any queries, contact Dominic Soon.



# main table has 16 rows
def scrapewithnext(url, counter, max):

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    for el in root.cssselect("tr"):  
        tds = el.cssselect("td")
        if len(tds)==16:
            uniqueurl = tds[1].cssselect("a")[0].attrib.get('href')
            if uniqueurl is None or not "info.php" in uniqueurl: continue
            data = { 
                'uniqueurl': uniqueurl,
                'model': tds[1].text_content(),
                'price': tds[3].text_content(),
                'date': tds[5].text_content(),
                'gear': tds[7].text_content(),
                'engine': tds[9].text_content(),
                'mileage': tds[11].text_content(),
                'type': tds[13].text_content()
            }
            
            scraperwiki.sqlite.save(unique_keys=['uniqueurl'], data=data)
  
    # must figure out how to clean up text data

    
    if counter < max:
        for link in root.cssselect("a.pagebar"):
            tmptext = link.text
            if tmptext is None:
                continue
            if "next" in tmptext.lower():
                # use this URL
                next_url = urlparse.urljoin(base_url, link.attrib.get('href'))    
                scrapewithnext(next_url, counter + 1, max);
                break

# script starts here
base_url = "http://www.sgcarmart.com"
scrapewithnext("http://www.sgcarmart.com/used_cars/listing.php?BRSR=400&RPG=100&AVL=2&TO=Any&ASL=1", 1, 800)

# Run 1: stopped after 80 pagesimport scraperwiki
import lxml.html
import urlparse

# This scraper is programmed as part of a research project.
# For any queries, contact Dominic Soon.



# main table has 16 rows
def scrapewithnext(url, counter, max):

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    for el in root.cssselect("tr"):  
        tds = el.cssselect("td")
        if len(tds)==16:
            uniqueurl = tds[1].cssselect("a")[0].attrib.get('href')
            if uniqueurl is None or not "info.php" in uniqueurl: continue
            data = { 
                'uniqueurl': uniqueurl,
                'model': tds[1].text_content(),
                'price': tds[3].text_content(),
                'date': tds[5].text_content(),
                'gear': tds[7].text_content(),
                'engine': tds[9].text_content(),
                'mileage': tds[11].text_content(),
                'type': tds[13].text_content()
            }
            
            scraperwiki.sqlite.save(unique_keys=['uniqueurl'], data=data)
  
    # must figure out how to clean up text data

    
    if counter < max:
        for link in root.cssselect("a.pagebar"):
            tmptext = link.text
            if tmptext is None:
                continue
            if "next" in tmptext.lower():
                # use this URL
                next_url = urlparse.urljoin(base_url, link.attrib.get('href'))    
                scrapewithnext(next_url, counter + 1, max);
                break

# script starts here
base_url = "http://www.sgcarmart.com"
scrapewithnext("http://www.sgcarmart.com/used_cars/listing.php?BRSR=400&RPG=100&AVL=2&TO=Any&ASL=1", 1, 800)

# Run 1: stopped after 80 pages