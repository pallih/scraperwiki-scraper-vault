import scraperwiki
import lxml.html 
import json

import sys
import random

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# first we get everything from ioby
def ioby():

    print "Getting ioby projects..."

    # starting links
    html = scraperwiki.scrape("http://ioby.org/projects?phrase=&status=All&vols=All&sort_by=title&sort_order=ASC&items_per_page=All")
    root = lxml.html.fromstring(html)

    for project in root.cssselect("div[class='main-info']"):
        project_name = project.cssselect("h3")[0].text_content()
    
        print project_name

    # get the url
        url = project.cssselect("h3 a")[0].attrib.get("href")
    
        project_url = "http://ioby.org" + url

    # go get the project page, to grab geo info 
        subpage = scraperwiki.scrape(project_url)

        start = subpage.find("jQuery.extend(Drupal.settings")
        end = subpage.find("\n", start)
        line = subpage[start:end]
        line = line.replace('jQuery.extend(Drupal.settings, ', '')[:-2]

    # see if the grabbed jQuery line has location info, if it doesn't, move on
        if line.find("gmap") == -1:
            print "Found a bad line"
            continue

    # convert the line to json and get the location info
        bigjson = json.loads(line)
        project_lat = bigjson["gmap"]["project-map"]["markers"][0]["latitude"]
        project_lon = bigjson["gmap"]["project-map"]["markers"][0]["longitude"]

        data = {
          'source' : "ioby",
          'project' : project_name,
          'url' : project_url,
          'latitude' : project_lat,
          'longitude' : project_lon,
        }

        scraperwiki.sqlite.save(unique_keys=['project'], data=data)

    # that's it for ioby.

# scrape changebyus
def changebyus():

    print "Getting Change By Us projects..."

    offset = 50 # how big a chunk each time?
    start_items = 0
    max_items = 350 # how many to fetch in total? 

    # get each chunk of json
    for index in range(start_items, max_items, offset):
        print "Fetching " + str(index)
        cbu_json_url = "http://nyc.changeby.us/search/projects?terms=&n=" + str(offset) + "&offset=" + str(index) #confusing use of offset/index, they are reversed

        cbu_json = scraperwiki.scrape(cbu_json_url)
        project_string = json.loads(cbu_json)

        for project in range(0,offset):
            store_it = 1

            # deal with variable lengths in the returned json here - if it's the final tranche there may not be {offset} items
            try:
                project_name = project_string["results"][project]["title"]
            except IndexError: 
                break

            url = project_string["results"][project]["project_id"]
            project_url = "http://nyc.changeby.us/project/" + str(url)

            if url != "/project/":

                # go to subpage for the location details
                subpage = scraperwiki.scrape(project_url) # this is a long page, we're looking for the map config info in a line containing app_page.data.project
    
                start = subpage.find("app_page.data.project")
                end = subpage.find("\n", start)
                line = subpage[start:end]

                # clean it up
                projectjson = line.replace('app_page.data.project = ', '')[:-1]

                bigjson = json.loads(projectjson)

                # don't store city-wide projects
                neighborhood =  bigjson["info"]["location"]["location_id"]
            
                if neighborhood == -1:
                    store_it = 0
                    # we don't want to put city-wide projects on the map, they're cool projects but it's confusing 
    
                # this is not very elegant, but I'm confused about dealing with this json-like string
                jitterlat = random.uniform(-0.02, 0.02)
                jitterlon = random.uniform(-0.015, 0.015)
                
                project_lat = float(bigjson["info"]["location"]["position"]["lat"][0:]) + jitterlat
                project_lon = float(bigjson["info"]["location"]["position"]["lng"][0:]) + jitterlon
            
                # store everything
                if store_it == 1:
                    data = {
                      'source' : "Change By Us",
                      'project' : project_name,
                      'url' : project_url,
                      'latitude' : project_lat,
                      'longitude' : project_lon,
                    }

                    scraperwiki.sqlite.save(unique_keys=['project'], data=data)  
                     
# --------

ioby()

changebyus()
