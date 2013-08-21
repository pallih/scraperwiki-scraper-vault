# underlying webpage has changed.  This scraper is broken


import scraperwiki
import BeautifulSoup
import re
import sys
import traceback
from datetime import datetime
from scraperwiki import datastore, log
import mechanize
import urlparse
import urllib2
import csv

print "hi there"
# BBSRC Grant Scraper [currently doesn't work because the search engine thinks there is a security problem.  try later]

# get abbreviated references first.  Then can later look up full data
# (the webpage has time-outs which will block slow sequential accessing)

def MainGetAbbreviatedReferences():
    br = mechanize.Browser()
    br.open("http://www.bbsrc.ac.uk/pa/grants/QuickSearch.aspx")
    print list(br.forms())[0]
    br.form = list(br.forms())[1]  # the forms don't have names
    # br["p_s_INAM,WINS"] = "Edinburgh"  # limit by institution to avoid whole database for now
    r = br.submit()

    recordsfound = -1
    nrecordsgot = 0
    allrecords = [ ]  # batch them up for later saving
    while True:
        try:
            nextlink = br.find_link(text_regex=re.compile("next TOC list"))
        except:
            nextlink = None
        text = br.response().read()
        
        mrecordsfound = re.search('<B><font face="arial">\s*(\d+)</B> Records found', text)
        nrecordsfound = int(mrecordsfound.group(1))
        if recordsfound == -1:
            log("Records found: %d" % nrecordsfound)
        elif recordsfound != nrecordsfound:
            log("mismatch in records found %d %d" % (recordsfound, nrecordsfound))
        recordsfound = nrecordsfound
        
        for desc, link in re.findall("(?s)<HTML>(.*?)</HTML>(.*?)<BR>", text):
            try:
                data = ExtractAbbreviatedBlock(desc, link, br.geturl())
                #scraperwiki.datastore.save(unique_keys=['grant_reference',], data=data)
                allrecords.append(data)
                print [nrecordsgot , data["grant_title"]]
                nrecordsgot += 1
            except Exception, e:
                print e
                log(e)
                
        if not nextlink:
            break
        br.follow_link(nextlink)

    if nrecordsgot != recordsfound:
        log("mismatch in records got %d %d" % (recordsfound, nrecordsgot))

    # save the records after we have collected them because the save function is too slow
    for data in allrecords:
        scraperwiki.datastore.save(unique_keys=['grant_reference',], data=data)

def formatExceptionInfo(maxTBlevel=5):
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.args
    except AttributeError:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)

        
def ExtractAbbreviatedBlock(desc, link, baseurl):
    mgrantref = re.search("<strong>(?:Grant\s*Reference|Studentship\s*number|Project\s*Reference):\s*</strong>\s*([^<]*)<", desc)
    mgrantinstitution = re.search("<strong>(?:Institution\s*of\s*Grant|Registered\s*Institution|Institute):\s*</strong>\s*([^<]*)<", desc)
    if not mgrantref or not mgrantinstitution:
        log(desc)
    grantref = mgrantref.group(1)
    grantinstitution = re.sub("\s+", " ", mgrantinstitution.group(1)).strip()
    mlink = re.search('(?s)<a href="(.*?)">(.*?)</a>', link)
    if not mlink:
        log(link)
    lurl, name = mlink.groups()
    # url = urlparse.urljoin(baseurl, re.sub("&amp;", "&", lurl)) # URL is useless as it's stateful
    name = re.sub("\s+", " ", name)
    return {"grant_reference":grantref, "grant_institution":grantinstitution, "grant_title":name}

                                   
def MainScrapeDetailedData():
    alldata = RetrieveAllData()
    br = mechanize.Browser()
    salldata = [ data  for data in alldata  if "total_grant" not in data ]
    log("Total records: %d, To scrape: %d" % (len(alldata), len(salldata)))
    for data in salldata:
        print "Scraping ref:", data["grant_reference"]
        try:
            grant = ScrapeDetailedData(br, data)
        except:
            print formatExceptionInfo()
            # log(e)
            grant=None
        if grant:
            print grant
            assert grant["grant_reference"] == data["grant_reference"]
            scraperwiki.datastore.save(["grant_reference"], grant)

        
def RetrieveAllData():
    url = "http://scraperwiki.com/scrapers/export/bbsrc-grants/"
    s = urllib2.urlopen(url)
    c = csv.reader(s.readlines()[1:10])
    headers = c.next()
    print headers
    alldata = [ ]
    for row in c:
        r = dict((k, v)  for k, v in zip(headers, row)  if v)
        alldata.append(r)
    return alldata

                                  
                                  
PLANNING_AREAS = {
    'AF':'Agri-Food',
    'AS':'Animal Sciences',
    'BCB':'Biochemistry & Cell Biology',
    'BMS':'Biomolecular Sciences',
    'EBS':'Engineering & Biological Sciences',
    'EQP':'Equipment & Facilities',
    'G&A':'Grants and Awards',
    
    'GDB':'Genes & Developmental Biology',
    'PMS':'Plant & Microbial Sciences',
    'A':'Animal Systems, Health & Wellbeing',
    'B':'Plants, Microbes, Food & Sustainability',
    'C':'Technological & Methodological Development',
    'D':'Molecules, Cells & Industrial Biotechnology',
}

GRANT_TYPES = {
    'Responsive':'Research grant',
    'IPA':'Industrial Partner Awards',
    'NI':'New Investigator Awards',
    'Fellow':'Fellowships',
    'LINK':'Research grant',
}


def clean_date(ddate):
    clean_date = datetime.date(datetime.strptime(ddate.strip(),'%d/%m/%y')).isoformat()
    return clean_date

def ScrapeDetailedData(br, data=None, ref=None):
    
    # this creates a new session for each search and the system soon calls security. gah.
    br.open("http://www.bbsrc.ac.uk/science/grants/search-grants-index.aspx")
    br.form = list(br.forms())[1]  # the forms don't have names
    if ref:
        reference = ref
    else:
        reference = data["grant_reference"]
        
    br["p_s_RONO"] = '"%s"' % reference
    
    r=br.submit()
    detail_html = r.read()
    detail = BeautifulSoup.BeautifulSoup(detail_html)
    
    state = detail.find('input')['value']

    # be polite - log out of session - or else the system will call security on you sooner or later
    logout_link = 'http://oasis.bbsrc.ac.uk/netans-bin/gate.exe?state=%s&f=logout&a_logout=Logout' % state
    
    br.open(logout_link)
    grant = {}
    
    tables = detail.findAll('table')
    print len(tables)

    grant['award_type'] = tables[0].find('td').find('font').findAll(text=True)[0]

    grant['grant_type'] = tables[0].find('a').findAll(text=True)[0]
    grant['grant_reference'] = tables[1].find('td').findAll(text=True)[1]

    td_data = tables[2].findAll('td')
    grant['grant_title'] = td_data[0].find('em').findAll(text=True)[0]
    grant['grant_institution'] = td_data[1].findAll(text=True)[1]
    grant['principal_investigator'] = td_data[2].findAll(text=True)[2]
    grant['investigator_at'] = td_data[2].findAll(text=True)[4]
    
    if len(td_data) == 4:
        grant['co_applicant'] = td_data[3].findAll(text=True)[2]
        grant['co_applicant_at'] = td_data[3].findAll(text=True)[4]
    
    grant['abstract'] = tables[3].findAll('td')[1].findAll(text=True)[2]
    grant['start_date'] = tables[4].findAll('td')[0].findAll(text=True)[2]
    grant['estimated_end_date'] = tables[4].findAll('td')[1].findAll(text=True)[2]
    grant['duration'] = tables[4].findAll('td')[2].findAll(text=True)[2]
    grant['planning_area'] = tables[5].find('a').findAll(text=True)[0].replace(';','')
    grant['total_grant'] = tables[5].findAll('td')[3].findAll(text=True)[1].replace(',','')
    grant['total_grant']  = grant['total_grant'][2:]
    for k,v in grant.items():
        grant[k] = v.strip().replace('\n',' ')
    # Clean up
    grant['total_grant'] = int(grant['total_grant']) # cgi script doesn't like ints ?
    # dereference the abbreviations
    grant['s_planning_area'] = PLANNING_AREAS[grant['planning_area']]
    grant['s_grant_type'] = GRANT_TYPES[grant['grant_type']]

    grant['start_date'] = clean_date(grant['start_date'])
    grant['estimated_end_date'] = clean_date(grant['estimated_end_date'])
    
    return grant


# main call to get the references
#MainGetAbbreviatedReferences()


# rescrape of those that are incomplete
#MainScrapeDetailedData()

# br = mechanize.Browser()

# ScrapeDetailedData(br, ref='D10262')
