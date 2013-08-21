import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://jobs.guardian.co.uk/jobs/media/digital-media/")
root = lxml.html.fromstring(html)
print html

ID_number = 1
jobs = root.cssselect('li')

for job in jobs:
    record1 = job.cssselect("div.jobWrap")
    body= job.cssselect("div.adBody")
    location = job.cssselect ("ul.horiz")
    details = job.cssselect("ul.recruitmentdetails")
    other = job.cssselect("p.selJobShortDesc")
    name = job.cssselect ("h4")
    
           
    print jobs

for job in jobs:
    #Change ID_number so it's 1 higher than it was 
    ID_number = ID_number + 1    
    #Create a new variable - record - containing a dictionary of 3 things...
    record = { "tag" : job.tag, "div" : job.text, "ID" : ID_number }
    scraperwiki.sqlite.save(["ID"], record)
