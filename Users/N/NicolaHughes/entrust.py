import scraperwiki
import requests
from bs4 import BeautifulSoup

# a", "b", "c", "cc", "d", "da", "e", "f"
objs = ["e"]

search_url = "http://www.entrust.org.uk/home/facts-and-figures/project-search"

params = {
    "perpage": 100,
    "offset": "",
    "ebname": "",
    "object": "",
    "projectname": "",
    "submit": "Submit" # The button has a value too
}

# For each letter
for obj in objs:
    # Assume we have a lot of pages and we'll exit when we get to the end
    for offset in range(53, 100000):
        print "Fetching page %d for '%s'" % (offset+1, obj)

        # Set the parameters we send to use that letter
        params["object"] = obj
        params["offset"] = offset
    
        # Make the web request using requests, will build a proper request
        # using params for the x=y&z=a bit of the query string.
        r = requests.get(search_url, params=params)
    
        # Build soup from the returned content
        soup = BeautifulSoup(r.content)
    
        # Find the table
        table_info = soup.find("table")
    
        # Get all of the entries, this currently includes the header though
        # so remember to skip the first.
        entries = table_info.find_all("tr")
        print "----Found %s entries for %s on page %d" % (len(entries), obj, offset+1)
        
    
        # See if we have a next page link, and increment offset before going around again
        # it has a class of page_next. If we can't find it (last page) then break
        np = soup.findAll(True, {'class': 'page_next'})
        if len(np) == 0:
            break

        for tr in entries[1:]:
            tds = tr.find_all("td")
            #print tds
            href = tds[0].find("a")
            entry_url = "http://www.entrust.org.uk" + href["href"]
            #print entry_url
            EB_name = tds[0].get_text()
            EB_county = tds[1].get_text()
            project_name = tds[2].get_text()
            obj = tds[3].get_text()
            #print EB_name, EB_county, project_name, obj
            data = { "URL": entry_url, "EB_Name": EB_name, "EB_County": EB_county, "Project_Name": project_name, "Object": obj }
            scraperwiki.sqlite.save(["URL"], data)
