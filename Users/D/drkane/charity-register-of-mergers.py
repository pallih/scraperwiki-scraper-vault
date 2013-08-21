###############################################################################
# Scraper for the charity register of mergers
# http://www.charity-commission.gov.uk/Charity_requirements_guidance/Your_charitys_activities/Working_with_others/rom.aspx
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import time
import re

# retrieve the Register of Mergers page
starting_url = 'http://www.charity-commission.gov.uk/Charity_requirements_guidance/Your_charitys_activities/Working_with_others/rom.aspx'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)
def group(s, n): return [s[i:i+n] for i in xrange(0, len(s), n)]


# regex for capturing Charity Commission numbers
#original version
#ccnum = re.compile(r"\([0-9]{6}\)|\([0-9]{7}\)|\([0-9]{6}-[0-9]{2}\)|\([0-9]{7}-[0-9]{2}\)|\([0-9]{6}-[0-9]{1}\)|\([0-9]{7}-[0-9]{1}\)|\([0-9]{6}/[0-9]{2}\)|\([0-9]{7}/[0-9]{2}\)|\([0-9]{6}/[0-9]{1}\)|\([0-9]{7}/[0-9]{1}\)")
#new version
ccnum = re.compile(r"\(\d?[\d]{6}\)|\(\d?[\d]{6}[\-/ ]\d?\d\)")


def find_ccnum(s):
# finds Charity Commission numbers within text string
    t = ccnum.search(s)
    if t:
        u = t.group()
        u = u.strip("(").strip(")")
    else:
        u = None
    return u

def remove_ccnum(t):
# remove Charity Commission numbers from text string
    u = ccnum.sub("",t)
    u = u.strip()
    return u

def checkDate(d):
# turn date into properly formatted one
    d = d.replace("\n","")
    d = d.replace("\r","")
    d = d.split("/")
    d[0] = int(d[0]) * 1
    d[1] = int(d[1]) * 1
    d[2] = int(d[2]) * 1
    t = (d[2], d[1], d[0], 0, 0, 0, 0, 1, 0)
    secs = time.mktime(t)
    secs = time.gmtime(secs)
    d = time.strftime("%Y-%m-%d", secs)
    return d

# use BeautifulSoup to get all <tr> tags
# bgcolor of data cells is either efefef or not specified
trs = soup.findAll('tr',bgcolor=["#efefef",None]) 
for tr in trs:
    tds = tr.findAll('td')
    # if there isn't the right number of <td>s then don't capture
    if len(tds)<3:
        continue
    else:
        # find transferor and transferee name and replace ccnum and ampersands
        if isinstance(tds[0].contents[0], basestring):
            transferor = tds[0].contents[0]
        else:
            try:
                transferor = tds[0].contents[0].contents[0]
            except:
                transferor = ''
        transferor = transferor.replace('&amp;','&')
        transferor_no = find_ccnum(transferor)
        transferor = remove_ccnum(transferor)
        if isinstance(tds[1].contents[0], basestring):
            transferee = tds[1].contents[0]
        else:
            try:
                transferee = tds[1].contents[0].contents[0]
            except:
                transferee = ''
        transferee = transferee.replace('&amp;','&')
        transferee_no = find_ccnum(transferee)
        transferee = remove_ccnum(transferee)
        # find and change dates. Dates can be null
        try:
            vesting_date = tds[2].find('div').contents[0]
            vesting_date = checkDate(vesting_date)
        except:
            vesting_date = None
        try:
            transfer_date = tds[3].find('div').contents[0]
            transfer_date = checkDate(transfer_date)
        except:
            transfer_date = None
        try:
            merger_date = tds[4].find('div').contents[0]
            merger_date = checkDate(merger_date)
        except:
            merger_date = None
    # can't work out how to create a decent unique id
    print transferor, transferor_no, transferee, transferee_no, vesting_date, transfer_date, merger_date
    record = { "transferor" : transferor , "transferor_no" : transferor_no, "transferee" : transferee, "transferee_no" : transferee_no, "vesting_date" : vesting_date, "transfer_date" : transfer_date, "merger_date" : merger_date }
    # save records to the datastore
    scraperwiki.datastore.save(["transferor"], record) 
    print "Record saved"
    