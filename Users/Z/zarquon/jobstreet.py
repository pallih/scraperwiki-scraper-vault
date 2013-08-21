import scraperwiki
import lxml.html

# Blank Python

print "Hello, coding in the cloud!"

html = scraperwiki.scrape("http://job-search.jobstreet.com.sg/singapore/job-opening.php")
root = lxml.html.fromstring(html)  

for row in root.cssselect("h4.rRowTitle a"):
    classified = row.attrib['href'].find('classified-ads')
    print row.text + ' ' + str(classified)
    if classified == -1:
        # ignore if from classified ads
        pass
    else:
        # scrape the main ad itself
        html = scraperwiki.scrape(row.attrib['href'])
        root = lxml.html.fromstrong(html)

        for rowtwo in root.cssselect():
        
        tmp =         
   
