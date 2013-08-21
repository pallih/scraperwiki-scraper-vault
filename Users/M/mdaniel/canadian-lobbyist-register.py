import scraperwiki
import re
import time
import urllib
from BeautifulSoup import BeautifulSoup

owner_url = 'http://www.ocl-cal.gc.ca/eic/site/lobbyist-lobbyiste1.nsf/eng/h_nx00274.html'
base_url = 'https://ocl-cal.gc.ca/app/secure/orl/lrrs/do/'
data_url = base_url \
+'_ls70_ls75_ls62_ls6c_ls69_ls63_ls53_ls65_ls61_ls72_ls63_ls68' \
+'?_ls73_ls65_ls61_ls72_ls63_ls68_ls54_ls79_ls70_ls65=search' \
+'&_ls72_ls65_ls67_ls69_ls73_ls74_ls72_ls61_ls74_ls69_ls6f_ls6e_ls53_ls74_ls61_ls74_ls75_ls73=recentActivity' \
+'&_STRTG3=tr'

scraperwiki.metadata.save('data_columns',\
  ['org.name','org.officer','org.phone',\
   'firm.consultant','firm.name','firm.client','firm.phone',\
   'from-date','to-date' \
  ])

def process_page( soup ):
    ''' This will insert the 'org' record and 'firm' records
    which it finds in the provided BeautifulSoup instance, `soup'.
    It will then attempt to locate the 'Next' URL and return it
    for further processing.'''
    lobbyists = []
    data_tds = soup.findAll('td',{'colspan':'2'})
    for row in data_tds:
        lobbyist = {}
    
        dateRow = row.findNext('td')
        dateTxt = dateRow.find('a').text
        dateFrom = None
        dateTo = None
        ma = re.search(r'\s*(\S+)\s*to\s*(.*)', dateTxt)
        if ma:
            dateFrom = ma.group(1)
            dateTo = ma.group(2)
    
        strongs = row.findAll('strong')
        if len(strongs) < 3:
            # organization
            org = {}
            org['org.name'] = strongs[0].text.strip()
            org['org.officer'] = strongs[1].text.strip()
            # sorry, this was much nicer in xpath :-(
            org['org.phone'] = row.getText('\0').split('\0')[6]
            if dateFrom:
                org['from-date'] = dateFrom
                org['to-date'] = dateTo
    
            # there does not appear to be a unique key :-(
            scraperwiki.datastore.save(['org.name','org.officer'], org)
    
            # lobbyist['organization'] = org
            # lobbyists.append( lobbyist )
        else:
            # consulting-firm
            firm = {}
            firm['firm.consultant'] = strongs[0].text.strip()
            firm['firm.name'] = strongs[1].text.strip()
            firm['firm.client'] = strongs[2].text.strip()
            # sorry, this was much nicer in xpath :-(
            firm['firm.phone'] = row.getText('\0').split('\0')[9]
            if dateFrom:
                firm['from-date'] = dateFrom
                firm['to-date'] = dateTo
    
            scraperwiki.datastore.save(['firm.name','firm.consultant','firm.client'], firm )
    
            # lobbyist['consulting-firm'] = firm
            # lobbyists.append( lobbyist )
    # print lobbyists
    td_bottom = soup.find('td',{'class':'tableBottom tableRight'})
    next_url = None
    if td_bottom:
        a_links = td_bottom.findAll('a')
        for a in a_links:
            if a.text == 'Next':
                next_url = a['href']
                break
    return next_url

def process_pagination( base_url, data_url ):
    # we are experiencing connection reset by peer
    # so retry a few times to obtain the data
    # sleeping in between attempts
    retries = 3
    for x in xrange(0, retries):
        try:
            html = scraperwiki.scrape( data_url )
            break
        except Exception, e:
            print "KABOOM on <%s>", e
            time.sleep( 30 )
    soup = BeautifulSoup( html )
    pageTxt = soup.find('td',{'colspan':'6'}).text
    ma = re.search(r'Results: (\d+)\s*-\s*(\d+)\s*of\s*(\d+)', pageTxt)
    if ma:
        print "PAGE.Start=",ma.group(1)
        print "PAGE.Stop=",ma.group(2)
        print "PAGE.Total=",ma.group(3)
    next_href = process_page( soup )
    if next_href:
        next_url = urllib.basejoin( base_url, next_href )
        print "NEXT=",next_url
        process_pagination( base_url, next_url )

process_pagination( base_url, data_url )
