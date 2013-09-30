# Scraper for Curaçao Chamber of Commerce                                                  #
# http://www.curacao-chamber.an/info/

import urllib2, re, httplib, scraperwiki, socket, datetime
from BeautifulSoup import BeautifulSoup as bs
from time import sleep

#debug:
#import random, pprint


# timeout in seconds
timeout = 10
socket.setdefaulttimeout(timeout)

def formatDate(datestring):
    # e.g. July 22, 1994 -> 1994-07-22
    if datestring == None: return None
    return datetime.datetime.strptime(datestring.strip(), "%B %d, %Y" ).strftime('%Y-%m-%d')

def parse(id):
    url = 'http://www.curacao-chamber.an/info/registry/excerpt.asp?companyid=%s&establishmentnr=0' % id
    resp = urllib2.urlopen(url)
    #print resp.info()

    soup = bs(resp.read())
    datatable = soup.find(id='maintable').table
    result = {}
    
    #parse label and number from header (this info is always included)
    nr, sep, label = soup.find(text=re.compile('registered under number')).partition(':')
    p = re.compile('\d+')
    result['companynr'] =  p.search(nr).group()
    result['label'] = label.strip()

    #extract the info string, containing the status of the company
    try:
        result['info'] = soup.find(attrs={'class': re.compile('warning|status')}).text
    except:
        result['info'] = None    

    #extract all data cells, process later
    for row in datatable.findAll(id=re.compile('data_cell')):
        result[str(row['id'])] = row.text

    return result

def clean(raw_result, returnfull=False):
    #Cleans and returns selected number of fields.
    #Use returnfull=True to get also the raw records

    clean_result = {}

    clean_result[u'CompanyNumber'] = int(raw_result['companynr'])
    clean_result[u'CompanyName'] = raw_result['label']
    clean_result[u'CompanyType'] = raw_result.get('LegalInfo_LegalFormID_data_cell')
    # Seat can be different from adress, e.g. St. Maarten while address on Curaçao:
    clean_result[u'CompanyStatutorySeat'] = raw_result.get('LegalInfo_StatutorySeat_data_cell') 

    clean_result[u'EstablismentDate'] = formatDate(raw_result.get('LegalInfo_DateEstablished_data_cell'))
    clean_result[u'IncorporationDate'] = formatDate(raw_result.get('LegalInfo_DateIncorporated_data_cell'))
    clean_result[u'DiscontinuationDate'] = formatDate(raw_result.get('LegalInfo_DateDiscontinued_data_cell'))

    clean_result[u'AddressStreet'] = raw_result.get('Addresses_Street_data_cell')
    clean_result[u'AddressCountry'] = raw_result.get('Addresses_CountryID_data_cell')
    clean_result[u'AddressPOBox'] = raw_result.get('Addresses_POBoxNr_data_cell')


    # Standardize the info warnings to activity-status
    clean_result[u'GeneralHaltDate'] = None
    if raw_result['info'] != None:
        p = re.compile('In bankruptcy|In liquidation|The business is not longer registered|The legal entity does not longer exist under local laws|The business is discontinued')
        clean_result[u'Status'] = p.match(raw_result['info']).group()

        # Extract some general end-data from info string (contains liquadation, discontinuation, etc. date):
        try:
            clean_result[u'GeneralHaltDate'] = formatDate(raw_result['info'].split('as of')[1].strip())
        except IndexError:
            clean_result[u'GeneralHaltDate'] = None

    else: clean_result[u'Status'] = 'Active'

    # return also raw fields if requested
    if returnfull: clean_result = dict(clean_result, **raw_result)
    
    return clean_result


class ScraperController:
    def __init__(self, highestRegisterdNr=None, mode='scrape'):
        self.highestRegisterdNr = highestRegisterdNr
        if self.highestRegisterdNr == None:
            try: # from DB
                self.highestRegisterdNr = int(scraperwiki.sqlite.get_var('highestRegisterdNr'))
            except TypeError:
                self.highestRegisterdNr = 122845 #currently (mid april) highest, update this for fallback
        try: # get last scraped from DB:
            self.lastScrapedNr = int(scraperwiki.sqlite.get_var('lastScrapedNr')) + 1
        except TypeError: #empty db, etc.
            self.lastScrapedNr = 0 # start from 1

    def scrapeCompany(self,nr):
        try:
            result = clean(parse(nr))
            scraperwiki.sqlite.save(['CompanyNumber'], result)
            rapport = {'scrapedate': str(datetime.datetime.now()), 'result': 'succes'}
            scraperwiki.sqlite.save_var('lastScrapedNr', nr)
        except Exception, e:
            rapport = {'scrapedate': str(datetime.datetime.now()), 'result': e}
        scraperwiki.sqlite.save_var(nr, rapport)

    def scrapeRange(self, startNumber=None, stopNumber=None):
        for nr in range(startNumber, stopNumber):
            print('Scraping company nr. %s' % nr)
            self.scrapeCompany(nr)
            sleep(0.5)

    def randomUpdate(self, n=500):
        #select random number from db/possible range (revist HTTP 500 numbers?)
        oldRecords = scraperwiki.sqlite.select('* FROM swdata ORDER BY RANDOM() LIMIT %s;' % n)
        for oldRecord in oldRecords:
            nr = oldRecord['CompanyNumber']
            print 'Checking company nr. %s' % nr
            newRecord = clean(parse(nr))
            if not oldRecord == newRecord:
                diff = {}
                diff = {'CompanyNumber' : nr, 'scrapedate' : str(datetime.datetime.now()), 'oldRecord' : oldRecord, 'newRecord' : newRecord }
                scraperwiki.sqlite.save(['CompanyNumber'], diff, table_name="swversioning")
                scraperwiki.sqlite.save(['CompanyNumber'], newRecord)
                print 'Updated company nr. %s' % nr
            sleep(0.5)           

    def start(self):

        # 1. If incomplete, start scraping from last scraped number, up to max registered
        if self.lastScrapedNr < self.highestRegisterdNr:
            print 'Starting scraperun from %s' % str(self.lastScrapedNr + 1)
            self.scrapeRange(self.lastScrapedNr+1, self.highestRegisterdNr)

        # 2. try scraping new numbers until HTTP error, save max registerd number

        while True:
            nr = self.highestRegisterdNr
            nr += 1
            try:
                scrapeCompany(nr)
                scraperwiki.sqlite.save_var('highestRegisterdNr', nr)
                sleep(0.5) 
            except urllib2.HTTPError:
                break

        # 3. if all are done, skip to random revisting records that are in DB
        sc.randomUpdate()

sc = ScraperController()
sc.start()

# Scraper for Curaçao Chamber of Commerce                                                  #
# http://www.curacao-chamber.an/info/

import urllib2, re, httplib, scraperwiki, socket, datetime
from BeautifulSoup import BeautifulSoup as bs
from time import sleep

#debug:
#import random, pprint


# timeout in seconds
timeout = 10
socket.setdefaulttimeout(timeout)

def formatDate(datestring):
    # e.g. July 22, 1994 -> 1994-07-22
    if datestring == None: return None
    return datetime.datetime.strptime(datestring.strip(), "%B %d, %Y" ).strftime('%Y-%m-%d')

def parse(id):
    url = 'http://www.curacao-chamber.an/info/registry/excerpt.asp?companyid=%s&establishmentnr=0' % id
    resp = urllib2.urlopen(url)
    #print resp.info()

    soup = bs(resp.read())
    datatable = soup.find(id='maintable').table
    result = {}
    
    #parse label and number from header (this info is always included)
    nr, sep, label = soup.find(text=re.compile('registered under number')).partition(':')
    p = re.compile('\d+')
    result['companynr'] =  p.search(nr).group()
    result['label'] = label.strip()

    #extract the info string, containing the status of the company
    try:
        result['info'] = soup.find(attrs={'class': re.compile('warning|status')}).text
    except:
        result['info'] = None    

    #extract all data cells, process later
    for row in datatable.findAll(id=re.compile('data_cell')):
        result[str(row['id'])] = row.text

    return result

def clean(raw_result, returnfull=False):
    #Cleans and returns selected number of fields.
    #Use returnfull=True to get also the raw records

    clean_result = {}

    clean_result[u'CompanyNumber'] = int(raw_result['companynr'])
    clean_result[u'CompanyName'] = raw_result['label']
    clean_result[u'CompanyType'] = raw_result.get('LegalInfo_LegalFormID_data_cell')
    # Seat can be different from adress, e.g. St. Maarten while address on Curaçao:
    clean_result[u'CompanyStatutorySeat'] = raw_result.get('LegalInfo_StatutorySeat_data_cell') 

    clean_result[u'EstablismentDate'] = formatDate(raw_result.get('LegalInfo_DateEstablished_data_cell'))
    clean_result[u'IncorporationDate'] = formatDate(raw_result.get('LegalInfo_DateIncorporated_data_cell'))
    clean_result[u'DiscontinuationDate'] = formatDate(raw_result.get('LegalInfo_DateDiscontinued_data_cell'))

    clean_result[u'AddressStreet'] = raw_result.get('Addresses_Street_data_cell')
    clean_result[u'AddressCountry'] = raw_result.get('Addresses_CountryID_data_cell')
    clean_result[u'AddressPOBox'] = raw_result.get('Addresses_POBoxNr_data_cell')


    # Standardize the info warnings to activity-status
    clean_result[u'GeneralHaltDate'] = None
    if raw_result['info'] != None:
        p = re.compile('In bankruptcy|In liquidation|The business is not longer registered|The legal entity does not longer exist under local laws|The business is discontinued')
        clean_result[u'Status'] = p.match(raw_result['info']).group()

        # Extract some general end-data from info string (contains liquadation, discontinuation, etc. date):
        try:
            clean_result[u'GeneralHaltDate'] = formatDate(raw_result['info'].split('as of')[1].strip())
        except IndexError:
            clean_result[u'GeneralHaltDate'] = None

    else: clean_result[u'Status'] = 'Active'

    # return also raw fields if requested
    if returnfull: clean_result = dict(clean_result, **raw_result)
    
    return clean_result


class ScraperController:
    def __init__(self, highestRegisterdNr=None, mode='scrape'):
        self.highestRegisterdNr = highestRegisterdNr
        if self.highestRegisterdNr == None:
            try: # from DB
                self.highestRegisterdNr = int(scraperwiki.sqlite.get_var('highestRegisterdNr'))
            except TypeError:
                self.highestRegisterdNr = 122845 #currently (mid april) highest, update this for fallback
        try: # get last scraped from DB:
            self.lastScrapedNr = int(scraperwiki.sqlite.get_var('lastScrapedNr')) + 1
        except TypeError: #empty db, etc.
            self.lastScrapedNr = 0 # start from 1

    def scrapeCompany(self,nr):
        try:
            result = clean(parse(nr))
            scraperwiki.sqlite.save(['CompanyNumber'], result)
            rapport = {'scrapedate': str(datetime.datetime.now()), 'result': 'succes'}
            scraperwiki.sqlite.save_var('lastScrapedNr', nr)
        except Exception, e:
            rapport = {'scrapedate': str(datetime.datetime.now()), 'result': e}
        scraperwiki.sqlite.save_var(nr, rapport)

    def scrapeRange(self, startNumber=None, stopNumber=None):
        for nr in range(startNumber, stopNumber):
            print('Scraping company nr. %s' % nr)
            self.scrapeCompany(nr)
            sleep(0.5)

    def randomUpdate(self, n=500):
        #select random number from db/possible range (revist HTTP 500 numbers?)
        oldRecords = scraperwiki.sqlite.select('* FROM swdata ORDER BY RANDOM() LIMIT %s;' % n)
        for oldRecord in oldRecords:
            nr = oldRecord['CompanyNumber']
            print 'Checking company nr. %s' % nr
            newRecord = clean(parse(nr))
            if not oldRecord == newRecord:
                diff = {}
                diff = {'CompanyNumber' : nr, 'scrapedate' : str(datetime.datetime.now()), 'oldRecord' : oldRecord, 'newRecord' : newRecord }
                scraperwiki.sqlite.save(['CompanyNumber'], diff, table_name="swversioning")
                scraperwiki.sqlite.save(['CompanyNumber'], newRecord)
                print 'Updated company nr. %s' % nr
            sleep(0.5)           

    def start(self):

        # 1. If incomplete, start scraping from last scraped number, up to max registered
        if self.lastScrapedNr < self.highestRegisterdNr:
            print 'Starting scraperun from %s' % str(self.lastScrapedNr + 1)
            self.scrapeRange(self.lastScrapedNr+1, self.highestRegisterdNr)

        # 2. try scraping new numbers until HTTP error, save max registerd number

        while True:
            nr = self.highestRegisterdNr
            nr += 1
            try:
                scrapeCompany(nr)
                scraperwiki.sqlite.save_var('highestRegisterdNr', nr)
                sleep(0.5) 
            except urllib2.HTTPError:
                break

        # 3. if all are done, skip to random revisting records that are in DB
        sc.randomUpdate()

sc = ScraperController()
sc.start()

