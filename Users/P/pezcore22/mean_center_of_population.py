# This scraper collects data about the Mean Center of Population of the 
# United States from 1790-2010. The site being scraped is originally from 
# http://www.census.gov/geo/reference/centersofpop/natcentersofpop.html. 
# However, due to some errors in the html from the original site, I created 
# a copy with the errors fixed and uploaded it on to University of Washington 
# student webspace. The storage of this page on UW space is temporary and is 
# used for academic research only.


import scraperwiki
import lxml.html


# The following website is on temporary space and will be used for 
# academic purposes only. 
html = scraperwiki.scrape("http://students.washington.edu/jareds22")
root = lxml.html.fromstring(html)

# Print statements for debugging purposes

# print html
# tmptrs = root.cssselect("div.inside tr")
# print len(tmptrs)

for tr in root.cssselect("div.inside tr"):
    
    # Print statement for debugging purposes
    # print lxml.html.tostring(tr)
    
    tds = tr.cssselect("td")

    # Print statement for debugging purposes
    # print "Length = "+str(len(tds))

    if len(tds) == 4:

        censusyear = tds[0].text
        lat = float(tds[1].text)
        longi = float(tds[2].text)
        approxloc = tds[3].text

        data = {
            'Census Year' : censusyear,
            'Latitude' : lat,
            'Longitude' : -longi,
            'Approximate Location' : approxloc
        }

        scraperwiki.sqlite.save(unique_keys=['Latitude'],data=data)



# This scraper collects data about the Mean Center of Population of the 
# United States from 1790-2010. The site being scraped is originally from 
# http://www.census.gov/geo/reference/centersofpop/natcentersofpop.html. 
# However, due to some errors in the html from the original site, I created 
# a copy with the errors fixed and uploaded it on to University of Washington 
# student webspace. The storage of this page on UW space is temporary and is 
# used for academic research only.


import scraperwiki
import lxml.html


# The following website is on temporary space and will be used for 
# academic purposes only. 
html = scraperwiki.scrape("http://students.washington.edu/jareds22")
root = lxml.html.fromstring(html)

# Print statements for debugging purposes

# print html
# tmptrs = root.cssselect("div.inside tr")
# print len(tmptrs)

for tr in root.cssselect("div.inside tr"):
    
    # Print statement for debugging purposes
    # print lxml.html.tostring(tr)
    
    tds = tr.cssselect("td")

    # Print statement for debugging purposes
    # print "Length = "+str(len(tds))

    if len(tds) == 4:

        censusyear = tds[0].text
        lat = float(tds[1].text)
        longi = float(tds[2].text)
        approxloc = tds[3].text

        data = {
            'Census Year' : censusyear,
            'Latitude' : lat,
            'Longitude' : -longi,
            'Approximate Location' : approxloc
        }

        scraperwiki.sqlite.save(unique_keys=['Latitude'],data=data)



