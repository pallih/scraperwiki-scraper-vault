import scraperwiki

import lxml.html
import json

# helper from (https://scraperwiki.com/scrapers/uk_towns_and_cities)
def get_html(title):
    raw_json = scraperwiki.scrape("http://en.wikipedia.org/w/api.php?action=parse&format=json&page=" + title)
    html = json.loads(raw_json)['parse']['text']['*']
    return html

urls = []

years = range(2003, 2021)
for year in years:
    urls.append("Oil_megaprojects_(" + str(year) + ")")


#Code is adapted from: https://scraperwiki.com/scrapers/time_zone_abbreviations/edit/
#reading tables is a bit difficult as we want to get both linked and unlinked text, which sometimes occurs in the same table cell
#In other words, when we find "<a href=...>Athabasca</a> (Muskeg River)",
#we want "Athabasca (Muskeg River)"

#Testing for single page
#page_title = "Oil_megaprojects_(2003)"

for page_title in urls:

    html = get_html(page_title)
    doc = lxml.html.fromstring(html)
    
    table = doc.cssselect('table.wikitable')[1]
    
    headers = table.xpath("//tr/th/text()")
    
    for row in table.cssselect('tr'):
        projectData = dict()
        cells = row.cssselect('td')
        index = 0
        for cell in cells:
            value = unicode(cell.text_content()).encode('utf-8')
            header = headers[index].replace(" ", "_").replace(".", "")
            index += 1
            projectData[header] = value
    
        if projectData.has_key('Project_Name'): #only use data where we have a project name
            if projectData["Project_Name"] != None: 
                scraperwiki.sqlite.save(unique_keys=['Project_Name'], data=projectData)
    
import scraperwiki

import lxml.html
import json

# helper from (https://scraperwiki.com/scrapers/uk_towns_and_cities)
def get_html(title):
    raw_json = scraperwiki.scrape("http://en.wikipedia.org/w/api.php?action=parse&format=json&page=" + title)
    html = json.loads(raw_json)['parse']['text']['*']
    return html

urls = []

years = range(2003, 2021)
for year in years:
    urls.append("Oil_megaprojects_(" + str(year) + ")")


#Code is adapted from: https://scraperwiki.com/scrapers/time_zone_abbreviations/edit/
#reading tables is a bit difficult as we want to get both linked and unlinked text, which sometimes occurs in the same table cell
#In other words, when we find "<a href=...>Athabasca</a> (Muskeg River)",
#we want "Athabasca (Muskeg River)"

#Testing for single page
#page_title = "Oil_megaprojects_(2003)"

for page_title in urls:

    html = get_html(page_title)
    doc = lxml.html.fromstring(html)
    
    table = doc.cssselect('table.wikitable')[1]
    
    headers = table.xpath("//tr/th/text()")
    
    for row in table.cssselect('tr'):
        projectData = dict()
        cells = row.cssselect('td')
        index = 0
        for cell in cells:
            value = unicode(cell.text_content()).encode('utf-8')
            header = headers[index].replace(" ", "_").replace(".", "")
            index += 1
            projectData[header] = value
    
        if projectData.has_key('Project_Name'): #only use data where we have a project name
            if projectData["Project_Name"] != None: 
                scraperwiki.sqlite.save(unique_keys=['Project_Name'], data=projectData)
    
