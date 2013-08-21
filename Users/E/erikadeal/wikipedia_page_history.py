#This scraper queries the Wikipedia API, retrieves the full revision history of an article, and saves the results in a CSV file. We did not use the Scraperwiki database because of an outage while writing the script, so this script would actually be run from a program rather than the browser. We used this history for three different articles about the Savar building collapse by switching out the URL. Because Wikipedia articles are formatted in a standard way, we only needed to change the parameters of the API query to retrieve different information.

import urllib
import xml.etree.ElementTree as ET
import csv

#Print out the content returned by the API; helps with debuggung
#url = urllib.urlopen("http://en.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=2013_Savar_building_collapse&rvprop=timestamp|user|comment&rvlimit=500").read()

#print url

#Fetch the URL to be read by an XML parser with the appropriate parameters set and separated by an ampersand:
#Format = XML
#Action = Query
#Prop = fetching the article property "revisions"
#Titles = The title of the article we want to query. I think you can only do multiples when you are NOT using the XML parser, though
#Rvprop = The specific revision properties that we want to fetch, separated by vertical dividers
#Rvlimit = Necessary declaration if we want to retrieve more than the latest revision

url = "http://en.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles=2013_Savar_building_collapse&rvlimit=1000"

#Parse the url as xml

article = ET.parse(urllib.urlopen(url))

#Use XPath to select the element we want to look at

revs = article.findall('.//rev')

print len(revs)

#print revs

with open('revisions3.csv', 'wb') as csvfile:
    revwriter = csv.writer(csvfile, delimiter=',')
    
#Iterate over <rev> elements, get the value of the attributes, and store them in variables
    for rev in revs:
        user = rev.get('user')
        time = rev.get('timestamp')
        content = rev.get('comment')
        
        #print the content of the variables
        #print user, " : ", time, " : ", content
        
        #store the user name in a list so that it can be counted in the next step
        #users.append(user)
        try:
            location = ET.parse(urllib.urlopen('http://api.hostip.info/get_xml.php?ip=' + user + '&position=true'))
        except UnicodeError:
            print "Unicode Error"
            continue

        root = location.getroot()

        country = root.find('.//countryName').text

        cityroot = root.find('.//Hostip')

        city = cityroot.find('.//{http://www.opengis.net/gml}name').text

        try:
            coords = root.find('.//{http://www.opengis.net/gml}coordinates').text.split(",", 1)
            lat = coords[0]
            lon = coords[1]
        except AttributeError:
            lat= "None"
            lon = "None"

        #print country, ", ", city, ", ", lat, ", ", lon

        try:
            revwriter.writerow([user, time, content, city, country, lat, lon])
        except UnicodeEncodeError:
            print "Unicode Issue"
            continue

csvfile.close()

