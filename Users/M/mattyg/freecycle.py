import scraperwiki
import datetime
import lxml.html
import pprint

search_terms = 'bike bicycle cat kitten monitor'

all_locations = {
                    "BillericaMA": "Billerica", 
                    "freecycleboston": "Boston",
                    "LexingtonMA": "Lexington", 
                    "FreecycleMedfordMA": "Medford",
                    "FreeCycle-Somerville-MA":"Somerville", 
                    "FreecycleWatertown": "Watertown",
                    "FreecycleWellesleyMA":"Wellesley",
                    "Chelmsford": "Chelmsford"
                }
basegroupurl = "http://groups.freecycle.org/"


# Get all MA Groups
basegroupurl = "http://www.freecycle.org/group/US/Massachusetts"
html = scraperwiki.scrape(basegroupurl )
root = lxml.html.fromstring(html)
grps = root.cssselect("article#active_groups a")
group_urls = []
for grp in grps:
    if grp.attrib.get("href")[:4] == "http":
        group_urls.append(grp.attrib.get("href"))


params = {
    'search_words' : search_terms,
    'include_offers' : 'on',
    'date_start' : '',
    'date_end' : '',
    'resultsperpage' : '100'
}
    
for group_url in group_urls:
    url = group_url+ "/posts/search"
    searchresults = scraperwiki.scrape(url, params)
    searchroot = lxml.html.fromstring(searchresults)
    #print searchresults
    for row in searchroot.cssselect("table tr"):
        lxml.html.tostring(row)
        table_cells = row.cssselect("td")
        if table_cells: 
            try:
                record = {}
                post_url = table_cells[0].cssselect("a")[0].attrib.get("href")
                record['save_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                record['group'] = all_locations[group_url[group_url.rfind("/")+1:]]
                
                record['group_url'] = basegroupurl+group_url
                record['post_id'] = post_url [post_url.rfind("/")+1:]
                record['url'] = post_url
                record['title'] = table_cells[1].cssselect("strong a")[0].text
                scraperwiki.sqlite.save(["post_id"], record)
            except Exception as e:
                print "Error parsing row: " + lxml.html.tostring(row)
                print pprint.pprint(e)
        


import scraperwiki
import datetime
import lxml.html
import pprint

search_terms = 'bike bicycle cat kitten monitor'

all_locations = {
                    "BillericaMA": "Billerica", 
                    "freecycleboston": "Boston",
                    "LexingtonMA": "Lexington", 
                    "FreecycleMedfordMA": "Medford",
                    "FreeCycle-Somerville-MA":"Somerville", 
                    "FreecycleWatertown": "Watertown",
                    "FreecycleWellesleyMA":"Wellesley",
                    "Chelmsford": "Chelmsford"
                }
basegroupurl = "http://groups.freecycle.org/"


# Get all MA Groups
basegroupurl = "http://www.freecycle.org/group/US/Massachusetts"
html = scraperwiki.scrape(basegroupurl )
root = lxml.html.fromstring(html)
grps = root.cssselect("article#active_groups a")
group_urls = []
for grp in grps:
    if grp.attrib.get("href")[:4] == "http":
        group_urls.append(grp.attrib.get("href"))


params = {
    'search_words' : search_terms,
    'include_offers' : 'on',
    'date_start' : '',
    'date_end' : '',
    'resultsperpage' : '100'
}
    
for group_url in group_urls:
    url = group_url+ "/posts/search"
    searchresults = scraperwiki.scrape(url, params)
    searchroot = lxml.html.fromstring(searchresults)
    #print searchresults
    for row in searchroot.cssselect("table tr"):
        lxml.html.tostring(row)
        table_cells = row.cssselect("td")
        if table_cells: 
            try:
                record = {}
                post_url = table_cells[0].cssselect("a")[0].attrib.get("href")
                record['save_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                record['group'] = all_locations[group_url[group_url.rfind("/")+1:]]
                
                record['group_url'] = basegroupurl+group_url
                record['post_id'] = post_url [post_url.rfind("/")+1:]
                record['url'] = post_url
                record['title'] = table_cells[1].cssselect("strong a")[0].text
                scraperwiki.sqlite.save(["post_id"], record)
            except Exception as e:
                print "Error parsing row: " + lxml.html.tostring(row)
                print pprint.pprint(e)
        


