import scraperwiki
import lxml.html

starturl = 'http://www.nhs.uk/Service-Search/GP/Bradford/Results/4/-1.759/53.796/4/2541?distance=5000&ResultsOnPageValue=100&isNational=0'

def scrapestaff(fullstafflink,starturl):
    html = scraperwiki.scrape(fullstafflink)
    root = lxml.html.fromstring(html)
    id = 0
    record = {}
    record['resultspage'] = starturl
    #div class="pad clear"
    record['name'] = root.cssselect('div."pad clear" h1')[0].text
#    record['tel'] = root.cssselect('div."pad clear" p')[0].text
 #   record['address'] = root.cssselect('div."pad clear" p')[0].text_content()
  #  record['website'] = root.cssselect('div."pad clear" a')[0].text
    #grab any contents of <div class="panel staff-details gp-staff">
    panels = root.cssselect('div."panel staff-details gp-staff"')
    for panel in panels:
        print "h4 text", panel.cssselect('h4')[0].text
        record['name'] = panel.cssselect('h4')[0].text
        record['URL'] = fullstafflink
        id = id+1
        record['ID within practice'] = id
        if panel.cssselect('div."info-item" p'):
            print "GMC No.", panel.cssselect('div."info-item" p')[0].text
            record['GMC No'] = panel.cssselect('div."info-item" p')[0].text
        else:
            record['GMC No'] = "NO GMC NUMBER"
        if panel.cssselect('div."staff-title pad" p em'):
            record['Job title'] = panel.cssselect('div."staff-title pad" p em')[0].text
        else:
            record['Job title'] = "NO JOB TITLE"
        print "RECORD", record
        scraperwiki.sqlite.save(['URL', 'ID within practice'],record)
    

def scrapelinks(starturl):
    html = scraperwiki.scrape(starturl)
    root = lxml.html.fromstring(html)
    #grab any contents of <th class="fctitle" ...>...<a href="
    links = root.cssselect("th.fctitle a")
    #loop through the resulting list
    for link in links:
        #grab the href= attribute, then replace 'Overview' in that URL with 'Staff'
        stafflink = link.attrib.get('href').replace("Overview","Staff")
        #add the nhs.uk base url so it's absolute not relative
        fullstafflink = "http://www.nhs.uk"+stafflink
        print "fullstafflink", fullstafflink
        scrapestaff(fullstafflink,starturl)
    #we could have repeated the process by following the next page link, e.g. <li class="next"><a href="
    #but the next URL simply adds '&currentPage=2' to the end
    #so instead we create a loop within which this scrapelinks function runs, on each page

for num in range(1,102):
    print num
    print "scraping", starturl+"&currentPage="+str(num)
    currentpage = starturl+"&currentPage="+str(num)
    scrapelinks(currentpage)

import scraperwiki
import lxml.html

starturl = 'http://www.nhs.uk/Service-Search/GP/Bradford/Results/4/-1.759/53.796/4/2541?distance=5000&ResultsOnPageValue=100&isNational=0'

def scrapestaff(fullstafflink,starturl):
    html = scraperwiki.scrape(fullstafflink)
    root = lxml.html.fromstring(html)
    id = 0
    record = {}
    record['resultspage'] = starturl
    #div class="pad clear"
    record['name'] = root.cssselect('div."pad clear" h1')[0].text
#    record['tel'] = root.cssselect('div."pad clear" p')[0].text
 #   record['address'] = root.cssselect('div."pad clear" p')[0].text_content()
  #  record['website'] = root.cssselect('div."pad clear" a')[0].text
    #grab any contents of <div class="panel staff-details gp-staff">
    panels = root.cssselect('div."panel staff-details gp-staff"')
    for panel in panels:
        print "h4 text", panel.cssselect('h4')[0].text
        record['name'] = panel.cssselect('h4')[0].text
        record['URL'] = fullstafflink
        id = id+1
        record['ID within practice'] = id
        if panel.cssselect('div."info-item" p'):
            print "GMC No.", panel.cssselect('div."info-item" p')[0].text
            record['GMC No'] = panel.cssselect('div."info-item" p')[0].text
        else:
            record['GMC No'] = "NO GMC NUMBER"
        if panel.cssselect('div."staff-title pad" p em'):
            record['Job title'] = panel.cssselect('div."staff-title pad" p em')[0].text
        else:
            record['Job title'] = "NO JOB TITLE"
        print "RECORD", record
        scraperwiki.sqlite.save(['URL', 'ID within practice'],record)
    

def scrapelinks(starturl):
    html = scraperwiki.scrape(starturl)
    root = lxml.html.fromstring(html)
    #grab any contents of <th class="fctitle" ...>...<a href="
    links = root.cssselect("th.fctitle a")
    #loop through the resulting list
    for link in links:
        #grab the href= attribute, then replace 'Overview' in that URL with 'Staff'
        stafflink = link.attrib.get('href').replace("Overview","Staff")
        #add the nhs.uk base url so it's absolute not relative
        fullstafflink = "http://www.nhs.uk"+stafflink
        print "fullstafflink", fullstafflink
        scrapestaff(fullstafflink,starturl)
    #we could have repeated the process by following the next page link, e.g. <li class="next"><a href="
    #but the next URL simply adds '&currentPage=2' to the end
    #so instead we create a loop within which this scrapelinks function runs, on each page

for num in range(1,102):
    print num
    print "scraping", starturl+"&currentPage="+str(num)
    currentpage = starturl+"&currentPage="+str(num)
    scrapelinks(currentpage)

import scraperwiki
import lxml.html

starturl = 'http://www.nhs.uk/Service-Search/GP/Bradford/Results/4/-1.759/53.796/4/2541?distance=5000&ResultsOnPageValue=100&isNational=0'

def scrapestaff(fullstafflink,starturl):
    html = scraperwiki.scrape(fullstafflink)
    root = lxml.html.fromstring(html)
    id = 0
    record = {}
    record['resultspage'] = starturl
    #div class="pad clear"
    record['name'] = root.cssselect('div."pad clear" h1')[0].text
#    record['tel'] = root.cssselect('div."pad clear" p')[0].text
 #   record['address'] = root.cssselect('div."pad clear" p')[0].text_content()
  #  record['website'] = root.cssselect('div."pad clear" a')[0].text
    #grab any contents of <div class="panel staff-details gp-staff">
    panels = root.cssselect('div."panel staff-details gp-staff"')
    for panel in panels:
        print "h4 text", panel.cssselect('h4')[0].text
        record['name'] = panel.cssselect('h4')[0].text
        record['URL'] = fullstafflink
        id = id+1
        record['ID within practice'] = id
        if panel.cssselect('div."info-item" p'):
            print "GMC No.", panel.cssselect('div."info-item" p')[0].text
            record['GMC No'] = panel.cssselect('div."info-item" p')[0].text
        else:
            record['GMC No'] = "NO GMC NUMBER"
        if panel.cssselect('div."staff-title pad" p em'):
            record['Job title'] = panel.cssselect('div."staff-title pad" p em')[0].text
        else:
            record['Job title'] = "NO JOB TITLE"
        print "RECORD", record
        scraperwiki.sqlite.save(['URL', 'ID within practice'],record)
    

def scrapelinks(starturl):
    html = scraperwiki.scrape(starturl)
    root = lxml.html.fromstring(html)
    #grab any contents of <th class="fctitle" ...>...<a href="
    links = root.cssselect("th.fctitle a")
    #loop through the resulting list
    for link in links:
        #grab the href= attribute, then replace 'Overview' in that URL with 'Staff'
        stafflink = link.attrib.get('href').replace("Overview","Staff")
        #add the nhs.uk base url so it's absolute not relative
        fullstafflink = "http://www.nhs.uk"+stafflink
        print "fullstafflink", fullstafflink
        scrapestaff(fullstafflink,starturl)
    #we could have repeated the process by following the next page link, e.g. <li class="next"><a href="
    #but the next URL simply adds '&currentPage=2' to the end
    #so instead we create a loop within which this scrapelinks function runs, on each page

for num in range(1,102):
    print num
    print "scraping", starturl+"&currentPage="+str(num)
    currentpage = starturl+"&currentPage="+str(num)
    scrapelinks(currentpage)

import scraperwiki
import lxml.html

starturl = 'http://www.nhs.uk/Service-Search/GP/Bradford/Results/4/-1.759/53.796/4/2541?distance=5000&ResultsOnPageValue=100&isNational=0'

def scrapestaff(fullstafflink,starturl):
    html = scraperwiki.scrape(fullstafflink)
    root = lxml.html.fromstring(html)
    id = 0
    record = {}
    record['resultspage'] = starturl
    #div class="pad clear"
    record['name'] = root.cssselect('div."pad clear" h1')[0].text
#    record['tel'] = root.cssselect('div."pad clear" p')[0].text
 #   record['address'] = root.cssselect('div."pad clear" p')[0].text_content()
  #  record['website'] = root.cssselect('div."pad clear" a')[0].text
    #grab any contents of <div class="panel staff-details gp-staff">
    panels = root.cssselect('div."panel staff-details gp-staff"')
    for panel in panels:
        print "h4 text", panel.cssselect('h4')[0].text
        record['name'] = panel.cssselect('h4')[0].text
        record['URL'] = fullstafflink
        id = id+1
        record['ID within practice'] = id
        if panel.cssselect('div."info-item" p'):
            print "GMC No.", panel.cssselect('div."info-item" p')[0].text
            record['GMC No'] = panel.cssselect('div."info-item" p')[0].text
        else:
            record['GMC No'] = "NO GMC NUMBER"
        if panel.cssselect('div."staff-title pad" p em'):
            record['Job title'] = panel.cssselect('div."staff-title pad" p em')[0].text
        else:
            record['Job title'] = "NO JOB TITLE"
        print "RECORD", record
        scraperwiki.sqlite.save(['URL', 'ID within practice'],record)
    

def scrapelinks(starturl):
    html = scraperwiki.scrape(starturl)
    root = lxml.html.fromstring(html)
    #grab any contents of <th class="fctitle" ...>...<a href="
    links = root.cssselect("th.fctitle a")
    #loop through the resulting list
    for link in links:
        #grab the href= attribute, then replace 'Overview' in that URL with 'Staff'
        stafflink = link.attrib.get('href').replace("Overview","Staff")
        #add the nhs.uk base url so it's absolute not relative
        fullstafflink = "http://www.nhs.uk"+stafflink
        print "fullstafflink", fullstafflink
        scrapestaff(fullstafflink,starturl)
    #we could have repeated the process by following the next page link, e.g. <li class="next"><a href="
    #but the next URL simply adds '&currentPage=2' to the end
    #so instead we create a loop within which this scrapelinks function runs, on each page

for num in range(1,102):
    print num
    print "scraping", starturl+"&currentPage="+str(num)
    currentpage = starturl+"&currentPage="+str(num)
    scrapelinks(currentpage)

