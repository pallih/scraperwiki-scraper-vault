# this is a set of base classes intended to be subclassed and used by Openly Local planning application scrapers

# the actual work is done in the run() function of the BaseScraper

import scraperwiki
from datetime import timedelta
from datetime import date
from datetime import datetime
import time
import re
import dateutil.parser
from BeautifulSoup import BeautifulSoup
import unittest

util = scraperwiki.utils.swimport("utility_library")
scrapemark = scraperwiki.utils.swimport("scrapemark_09")

class BaseScraper(): # scraper template class to be subclassed by all children

    # default settings for all scrapers
    ID_ORDER = 'rowid asc' # defines order for id only records to return the most recent records first - example 'uid desc' or 'url desc'
    START_SEQUENCE = ''
    TABLE_NAME = 'swdata'
    DATA_START_MARKER = 'earliest'
    DATA_END_MARKER = 'latest'
    MAX_ID_BATCH = 600 # max application ids to fetch in one go
    MAX_UPDATE_BATCH = 350 # max application details to scrape in one go
    STABLE_INTERVAL = 60 # number of days before application detail is considered stable
    DEBUG = False
    HEADERS = None
    PROXY = ''
    JSESS_REGEX = re.compile(r';jsessionid=\w*')
    TIMEOUT = 30

    request_date_format = '%d/%m/%Y'

    # scrapemark config items to be provided in children
    scrape_data_block = "" # captures HTML block encompassing all fields to be gathered
    scrape_min_data = "" # the minimum acceptable valid dataset on an application page
    scrape_optional_data = "" # other optional parameters that can appear on an application page

    def __init__(self, table_name = None):
        self.br, self.handler, self.cj = util.get_browser(self.HEADERS, '', self.PROXY)
        if table_name:
            self.TABLE_NAME = table_name
        if self.TABLE_NAME != 'swdata':
            self.DATA_START_MARKER = 'earliest-' + self.TABLE_NAME
            self.DATA_END_MARKER = 'latest-' + self.TABLE_NAME

    # optionally try to get a batch of missing early IDs back to start of the sequence
    def gather_early_ids (self):
        current_earliest_sequence = scraperwiki.sqlite.get_var(self.DATA_START_MARKER)
        current_latest_sequence = scraperwiki.sqlite.get_var(self.DATA_END_MARKER)
        if current_earliest_sequence and current_earliest_sequence > self.START_SEQUENCE: # only takes place when some current data has been gathered
            earliest, latest, count = self.gather_ids(self.START_SEQUENCE, current_earliest_sequence)
            scraperwiki.sqlite.save_var(self.DATA_START_MARKER, earliest)
            if latest and not current_latest_sequence:
                scraperwiki.sqlite.save_var(self.DATA_END_MARKER, latest)
            print "Gathered " + str(count) + " early ids from " + str(earliest) + " to " +  str(latest)
        elif current_earliest_sequence:
            print "Gathered no early ids: earliest (" + str(current_earliest_sequence) + ") <= target (" +  str(self.START_SEQUENCE) + ")"
        
    # always make an attempt to get some current IDs from the most recent part of the sequence
    def gather_current_ids (self):
        current_earliest_sequence = scraperwiki.sqlite.get_var(self.DATA_START_MARKER)
        current_latest_sequence = scraperwiki.sqlite.get_var(self.DATA_END_MARKER)
        if not current_latest_sequence: # set up the swvariables table by saving something
            scraperwiki.sqlite.save_var(self.DATA_END_MARKER, None)
        earliest, latest, count = self.gather_ids(current_latest_sequence)
        scraperwiki.sqlite.save_var(self.DATA_END_MARKER, latest)
        if not current_earliest_sequence:
            scraperwiki.sqlite.save_var(self.DATA_START_MARKER, earliest)
        print "Gathered " + str(count) + " current ids from " + str(earliest) + " to " +  str(latest)

    # optionally try to get a batch of missing early IDs back to start of the sequence
    def gather_early_ids2 (self):
        current_earliest_sequence = scraperwiki.sqlite.get_var(self.DATA_START_MARKER)
        current_latest_sequence = scraperwiki.sqlite.get_var(self.DATA_END_MARKER)
        if current_earliest_sequence and current_earliest_sequence > self.START_SEQUENCE: # only takes place when some current data has been gathered
            earliest, latest, count = self.gather_ids2(self.START_SEQUENCE, current_earliest_sequence)
            if count:
                scraperwiki.sqlite.save_var(self.DATA_START_MARKER, earliest)
                if not current_latest_sequence:
                    scraperwiki.sqlite.save_var(self.DATA_END_MARKER, latest)
                print "Gathered %d early ids from %s to %s" % (count, earliest, latest)
            else:
                print "Warning - gathered no early ids before %s" % latest
        elif current_earliest_sequence:
            print "Gathered no early ids: earliest (%s) <= target (%s)" % (current_earliest_sequence, self.START_SEQUENCE)
        
    # always make an attempt to get some current IDs from the most recent part of the sequence
    def gather_current_ids2 (self):
        current_earliest_sequence = scraperwiki.sqlite.get_var(self.DATA_START_MARKER)
        current_latest_sequence = scraperwiki.sqlite.get_var(self.DATA_END_MARKER)
        if not current_latest_sequence: # set up the swvariables table by saving something
            scraperwiki.sqlite.save_var(self.DATA_END_MARKER, None)
        earliest, latest, count = self.gather_ids2(current_latest_sequence)
        if count:
            scraperwiki.sqlite.save_var(self.DATA_END_MARKER, latest)
            if not current_earliest_sequence:
                scraperwiki.sqlite.save_var(self.DATA_START_MARKER, earliest)
            print "Gathered %d current ids from %s to %s" % (count, earliest, latest)
        else:
            print "Warning - gathered no current ids later than %s" % earliest
            
    # gathers IDs, function to be implemented in the children
    def gather_ids (self, sequence_from, sequence_to):
        return '', '', 0

    # gathers IDs, function to be implemented in the children
    def gather_ids2 (self, sequence_from, sequence_to):
        return '', '', 0

    # try to fill the application detail in any empty records
    def populate_missing_applications(self):
        try:
            result = scraperwiki.sqlite.select("count(*) as count, max(rowid) as max, min(rowid) as min from " + self.TABLE_NAME + " where date_scraped is null")
            missing_count = int(result[0]['count'])
            maxr = int(result[0]['max'])
            minr = int(result[0]['min'])
        except:
            missing_count = 0; maxr = 0; minr = 0
        try:
            missing_applications = scraperwiki.sqlite.select("""
                * from """ + self.TABLE_NAME + " where date_scraped is null order by " + self.ID_ORDER + """
                limit """ + str(self.MAX_UPDATE_BATCH))
            scraperwiki.sqlite.execute("create index if not exists date_scraped_manual_index on " + self.TABLE_NAME + " (date_scraped)")
            scraperwiki.sqlite.execute("create index if not exists start_date_manual_index on " + self.TABLE_NAME + " (start_date)")
        except:
            missing_applications = scraperwiki.sqlite.select("""
                * from """ + self.TABLE_NAME + " order by " + self.ID_ORDER + """
                limit """ + str(self.MAX_UPDATE_BATCH))
        count = 0
        for applic in missing_applications:
            if self.update_application_detail(applic):
                count = count + 1
        print "Populated " + str(count) + " empty applications (out of " + str(len(missing_applications)) + " tried and " + str(missing_count) + " found)", maxr, minr
        if count == 0 and len(missing_applications) == self.MAX_UPDATE_BATCH:
            print "First bad empty application:", missing_applications[0]['uid']
                
    # always update the details of the most current applications not previously scraped today
    def update_current_applications(self):
        cutoff_date = date.today() - timedelta(days=self.STABLE_INTERVAL)
        current_test = """
        (date_scraped is not null and date_scraped < '""" + date.today().strftime(util.ISO8601_DATE) + """') and
        (start_date is null or start_date > '""" + cutoff_date.strftime(util.ISO8601_DATE) + "')"
        #print current_test
        try:
            result = scraperwiki.sqlite.select("count(*) as count from " + self.TABLE_NAME + " where " + current_test)
            update_count = int(result[0]['count'])
        except:
            update_count = 0; maxr = 0; minr = 0
        current_applications = scraperwiki.sqlite.select("* from " + self.TABLE_NAME + " where " + current_test + " order by date_scraped asc limit " + str(self.MAX_UPDATE_BATCH))
        count = 0
        for applic in current_applications:
            if self.update_application_detail(applic):
                count = count + 1
        print "Updated " + str(count) + " other current applications (out of " + str(len(current_applications)) + " tried and " + str(update_count) + " found)" 

    # fetches and stores the details of one application
    def update_application_detail(self, applic):
        result = None
        if applic.get('url'):
            result = self.get_detail_from_url(applic['url'])
        if not result:
            result = self.get_detail_from_uid(applic['uid'])
        if result:
            applic.update(result)
            if applic.get('date_received') and applic.get('date_validated'):
                if applic['date_received'] < applic['date_validated']:
                    applic['start_date'] = applic['date_received']
                else:
                    applic['start_date'] = applic['date_validated']
            elif applic.get('date_received'):
                applic['start_date'] = applic['date_received']
            elif applic.get('date_validated'):
                applic['start_date'] = applic['date_validated']
            applic['date_scraped'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            scraperwiki.sqlite.save(unique_keys=['uid'], data=applic, table_name=self.TABLE_NAME)
            return True
        else:
            if self.DEBUG:
                print "Cannot update details for:", applic
            if self.is_zombie(applic['uid']):
                scraperwiki.sqlite.execute("delete from %s where uid = '%s'" % (self.TABLE_NAME, applic['uid']))
                scraperwiki.sqlite.commit()
                print 'Deleted', applic['uid']
            return False

    # tests for zombie applications (that don't lead anywhere) using the uid, to be implemented in the children
    def is_zombie(self, uid):
        return False

    # get application data using the UID, to be implemented in the children
    def get_detail_from_uid(self, uid):
        return None

    # scrape detailed information on one record via its access URL
    def get_detail_from_url (self, url):
        if self.DEBUG: start = time.time()
        try:
            response = self.br.open(url, None, self.TIMEOUT) # a shortish timeout, as we then fall back via the uid if it fails
            html = response.read()
            url = response.geturl()
            if self.DEBUG:
                print "Html obtained from url:", html
        except:
            if self.DEBUG: raise
            else: return None
        result = self.get_detail(html, url)
        if self.DEBUG:
            print "Secs to fetch detail from url and process:", time.time() - start
        return result

    # scrape detailed information on one record given its HTML and URL
    def get_detail (self, html, url, scrape_data_block = None, scrape_min_data = None, scrape_optional_data = []):
        # use class defaults if none supplied
        scrape_data_block = scrape_data_block or self.scrape_data_block
        scrape_min_data = scrape_min_data or self.scrape_min_data
        scrape_optional_data = scrape_optional_data or self.scrape_optional_data
        result = scrapemark.scrape(scrape_data_block, html, url)
        if result and result.get('block'):
            data_block = result['block']
            if self.DEBUG:
                print "Scraped data block:", data_block
            result = scrapemark.scrape(scrape_min_data, data_block, url)
            if self.DEBUG:
                print "Scraped min data:", result
            if result:
                for i in scrape_optional_data:
                    next_val = scrapemark.scrape(i, data_block, url)
                    if next_val:
                        result.update(next_val)
                self.clean_record(result)
                return result
            else:
                return None
        else:
            return None

    # post process a scraped record: parses dates, converts to ISO8601 format, strips spaces, tags etc
    def clean_record (self, record):
        if self.DEBUG: print "Raw record", record
        for k, v in record.items(): 
            if v:
                if isinstance(v, list):
                    v = ' '.join(v)

                if not util.GAPS_REGEX.sub('', v): # first test for and remove any fields with space only strings - see dates below
                    v = None
                elif k == 'uid':
                    v = util.GAPS_REGEX.sub('', v) # strip any spaces in uids
                elif k == 'url' or k.endswith('_url'):
                    text = util.GAPS_REGEX.sub('', v) # strip any spaces in urls
                    v = self.JSESS_REGEX.sub('', text) # strip any jsessionid parameter
                elif k.endswith('_date') or k.startswith('date_'):
                    text = util.GAPS_REGEX.sub(' ', v) # normalise any internal space (allows date conversion to handle non-breakable spaces)
                    try: # note bug: the date parser turns an all spaces string into today's date
                        dt = dateutil.parser.parse(text, dayfirst=True).date()
                        v = dt.strftime(util.ISO8601_DATE)
                    except:
                        v = None # badly formatted dates are stripped out
                else:
                    text = util.TAGS_REGEX.sub(' ', v) # replace any html tag content with spaces
                    try:
                        text = BeautifulSoup(text, convertEntities="html").contents[0].string
                        # use beautiful soup to convert html entities to unicode strings
                    except:
                        pass
                    text = util.GAPS_REGEX.sub(' ', text) # normalise any internal space
                    v = text.strip() # strip leading and trailing space
            if not v: # delete if the cleaned record is empty
                del record[k]
            else:
                record[k] = v
        if self.DEBUG: print "Cleaned record", record

    # post process a set of uid/url records: strips spaces in the uid etc - now uses clean_record above
    def clean_ids (self, records):
        for record in records:
            record = self.clean_record(record)

    # main run function for all scrapers
    def run (self):
        self.gather_current_ids2()
        self.gather_early_ids2()
        self.populate_missing_applications()
        self.update_current_applications()

    # care = reset scraping by zeroing sequence counters
    def reset (self, earliest = None, latest = None):
        scraperwiki.sqlite.save_var(self.DATA_START_MARKER, earliest)
        scraperwiki.sqlite.save_var(self.DATA_END_MARKER, latest)
        earliest = scraperwiki.sqlite.get_var(self.DATA_START_MARKER)
        latest = scraperwiki.sqlite.get_var(self.DATA_END_MARKER)
        print "Successfuly reset the sequence counters for " + self.TABLE_NAME + ": earliest = " + str(earliest) + ", latest = " + str(latest)

    # care = completely clear the current scraped data
    def clear_all (self):
        scraperwiki.sqlite.execute("delete from swvariables where name = '" + self.DATA_START_MARKER + "' or name = '" + self.DATA_END_MARKER + "'")
        scraperwiki.sqlite.execute("drop table if exists " + self.TABLE_NAME)
        scraperwiki.sqlite.commit()
        print "Successfuly cleared out " + self.TABLE_NAME

    # replace the current planning data with all the data from another planning scraper
    def replace_all_with(self, scraper_name = None, remote_table = None):
        if not remote_table:
            remote_table = self.TABLE_NAME
        if not scraper_name and remote_table == self.TABLE_NAME:
            print "Cannot replace the scraped data with itself"
            return
        scraper = ''
        if scraper_name:
            try:
                scraper = 'scraper.'
                scraperwiki.sqlite.attach(scraper_name, 'scraper') 
                scraper_name = scraper_name + ':'
            except:
                pass
        else:
            scraper_name = ''
        if remote_table != 'swdata':
            remote_start_marker = 'earliest-' + remote_table
            remote_end_marker = 'latest-' + remote_table
        else:
            remote_start_marker = 'earliest'
            remote_end_marker = 'latest'
        result = scraperwiki.sqlite.select("* from " + scraper + "swvariables where name = '" + remote_start_marker + "'")
        earliest = result[0]
        result = scraperwiki.sqlite.select("* from " + scraper + "swvariables where name = '" + remote_end_marker + "'")
        latest = result[0]
        earliest['name'] = self.DATA_START_MARKER
        latest['name'] = self.DATA_END_MARKER
        scraperwiki.sqlite.save(unique_keys=['name'], data=earliest, table_name='swvariables') 
        scraperwiki.sqlite.save(unique_keys=['name'], data=latest, table_name='swvariables')
        try:
            scraperwiki.sqlite.execute("drop table if exists " + self.TABLE_NAME)
        except:
            pass
        scraperwiki.sqlite.execute("create table if not exists " + self.TABLE_NAME + " as select * from " + scraper + remote_table) # indices?
        scraperwiki.sqlite.commit()
        result = scraperwiki.sqlite.select("count(*) as count from " + self.TABLE_NAME)
        count = result[0]['count']
        earliest = scraperwiki.sqlite.get_var(self.DATA_START_MARKER)
        latest = scraperwiki.sqlite.get_var(self.DATA_END_MARKER)
        print "Successfuly cloned " + self.TABLE_NAME + " from " + scraper_name + remote_table + ": count = " + str(count) + ", earliest = " + earliest + ", latest = " + latest
        
# Telford, Nuneaton, Brighton, East Sussex, Braintree, Hyndburn, South Hams, Kirklees, Ceredigion, Monmouthshire
# Redcar/Cleveland, Glamorgan, North Lincs, Nottinghamshire,  ... and more ...
class DateScraper(BaseScraper): # for those sites that can return applications between two arbitrary search dates 

    START_SEQUENCE = '2000-01-01' # gathers id data by working backwards from the current date towards this one
    BATCH_DAYS = 14 # batch size for each scrape - number of days to gather to produce at least one result each time
    MIN_DAYS = 14 # min number of days to get when gathering current ids

    # process id batches working through a date sequence
    # if two parameters are supplied this is a request to gather backwards from 'to' towards 'from', returning the real date range found
    # if one parameter is supplied it's a request to gather backwards from today towards 'from', returning the real date range found
    def gather_ids (self, sequence_from = None, sequence_to = None):
        original_current_target = None
        if not sequence_to: # gathering current dates
            get_current_dates = True
            current_period_begins = date.today() - timedelta(days=self.MIN_DAYS)
            start = date.today()
            original_current_target = util.get_dt(sequence_from, util.ISO8601_DATE)
            if original_current_target:
                target = original_current_target
                if target < current_period_begins:
                    start = target + timedelta(days=self.MIN_DAYS)
                elif target > current_period_begins:
                    target = current_period_begins
            else:
                target = current_period_begins
        else: # gathering early dates
            get_current_dates = False
            full_sequence_begins = util.get_dt(self.START_SEQUENCE, util.ISO8601_DATE)
            start = util.get_dt(sequence_to, util.ISO8601_DATE)
            target = util.get_dt(sequence_from, util.ISO8601_DATE)
            if not start or start > date.today():
                start = date.today()
            if not target or target < full_sequence_begins:
                target = full_sequence_begins
        count = 0
        current = start 
        while (get_current_dates or count < self.MAX_ID_BATCH) and current > target: # only take account of max batch if gathering early dates
            next = current - timedelta(days=self.BATCH_DAYS)
            result = self.get_id_batch(next, current)
            if result:
                if self.DEBUG:
                    print "Storing " + str(len(result)) + " ids gathered from " + next.strftime(util.ISO8601_DATE) + " to " + current.strftime(util.ISO8601_DATE)
                scraperwiki.sqlite.save(unique_keys=['uid'], data=result, table_name=self.TABLE_NAME)
                if self.DEBUG: print sequence_from, sequence_to
                if get_current_dates: # latest applications are updated on the spot
                    for i in result:
                        self.update_application_detail(i)
                count = count + len(result)
                current = next - timedelta(days=1)
            else:
                break
        if original_current_target and current > original_current_target: # error if not gathered enough current data to fully fill data gap
            return original_current_target.strftime(util.ISO8601_DATE), original_current_target.strftime(util.ISO8601_DATE), 0
        else:
            return current.strftime(util.ISO8601_DATE), start.strftime(util.ISO8601_DATE), count
        # note 'current' date is exclusive, 'start' date is inclusive

    # Improved version of gather_ids()
    # process id batches working through a date sequence
    # if two parameters are supplied this is a request to gather backwards from 'to' towards 'from', returning the real date range found
    # if one parameter is supplied it's a request to gather forwards beyond 'from' towards today, returning the real date range found
    # always expects to gather some data - returned count of zero is an error
    def gather_ids2 (self, sequence_from = None, sequence_to = None):
        if not sequence_to: # gathering current dates - going forward
            move_forward = True
            target = date.today()
            start = util.get_dt(sequence_from, util.ISO8601_DATE)
            current_period_begins = target - timedelta(days=self.MIN_DAYS)
            if not start or start > current_period_begins:
                start = current_period_begins
            start = start + timedelta(days=1) # begin one day after supplied date
        else: # gathering early dates - going backward
            move_forward = False
            start = util.get_dt(sequence_to, util.ISO8601_DATE)
            target = util.get_dt(sequence_from, util.ISO8601_DATE)
            if not start or start > date.today():
                start = date.today()
            else:
                start = start - timedelta(days=1) # begin one day before supplied date
            full_sequence_begins = util.get_dt(self.START_SEQUENCE, util.ISO8601_DATE)
            if not target or target < full_sequence_begins:
                target = full_sequence_begins
        count = 0
        current = start
        ok_current = start
        while count < self.MAX_ID_BATCH and ((not move_forward and current >= target) or (move_forward and current <= target)): 
            if not move_forward:
                next = current - timedelta(days=self.BATCH_DAYS-1)
                result = self.get_id_batch(next, current)
            else:
                next = current + timedelta(days=self.BATCH_DAYS-1)
                result = self.get_id_batch(current, next)
            if result:
                if self.DEBUG:
                    if not move_forward:
                        print "Storing " + str(len(result)) + " ids gathered from " + next.strftime(util.ISO8601_DATE) + " to " + current.strftime(util.ISO8601_DATE)
                    else:
                        print "Storing " + str(len(result)) + " ids gathered from " + current.strftime(util.ISO8601_DATE) + " to " + next.strftime(util.ISO8601_DATE)
                scraperwiki.sqlite.save(unique_keys=['uid'], data=result, table_name=self.TABLE_NAME)
                count = count + len(result)
                ok_current = next
                if not move_forward:
                    current = next - timedelta(days=1)
                else:
                    current = next + timedelta(days=1)
                    for i in result:
                        self.update_application_detail(i) # latest applications are updated on the spot
            else:
                break
        if not move_forward:
            return ok_current.strftime(util.ISO8601_DATE), start.strftime(util.ISO8601_DATE), count
        else:
            if ok_current > date.today():
                ok_current = date.today()
            return start.strftime(util.ISO8601_DATE), ok_current.strftime(util.ISO8601_DATE), count

    # retrieves a batch of IDs betwen two sequence dates, to be implemented in the children
    # NB dates should be inclusive
    def get_id_batch (self, date_from, date_to):
        return [] # empty or None is an invalid result - means try again next time

# annual = Weymouth - now date scraper - see dorsetforyou
# monthly = Wokingham, Sedgemoor, Wychavon, Peak District
# 20 days = Gosport
# weekly = Kensington, Tower Hamlets, West Lothian, Colchester, Nottingham, Stevenage, Hastings, Copeland (PDFs), Swale (some PDFs), Isle of Man, Solihull, Exmoor
# weekly and monthly = Cotswold
class PeriodScraper(BaseScraper): # for those sites that return a fixed period of applications (weekly, monthly) around a search date

    START_SEQUENCE = '2000-01-01' # gathers id data by working backwards from the current date towards this one
    #PERIOD_TYPE = 'Month' # calendar month including the specified date
    #PERIOD_TYPE = 'Saturday' # 7 day week ending on the specified day and including the supplied date
    #PERIOD_TYPE = '-Saturday' # 7 day week beginning on the specified day and including the supplied date
    #PERIOD_TYPE = '14' # 2 weeks beginning on the specified date
    #PERIOD_TYPE = '-14' # 2 weeks ending on the specified date
    MIN_DAYS = 14 # min number of days to get when gathering current ids

    # process id batches working through a date sequence
    # if two parameters are supplied this is a request to gather backwards from 'to' towards 'from', returning the real date range found
    # if one parameter is supplied it's a request to gather backwards from today towards 'from', returning the real date range found
    def gather_ids (self, sequence_from = None, sequence_to = None):
        original_current_target = None
        if not sequence_to: # gathering current dates
            get_current_dates = True
            current_period_begins = date.today() - timedelta(days=self.MIN_DAYS)
            start = date.today()
            original_current_target = util.get_dt(sequence_from, util.ISO8601_DATE)
            if original_current_target:
                target = original_current_target
                if target < current_period_begins:
                    start = target + timedelta(days=self.MIN_DAYS)
                elif target > current_period_begins:
                    target = current_period_begins
            else:
                target = current_period_begins
        else: # gathering early dates
            get_current_dates = False
            full_sequence_begins = util.get_dt(self.START_SEQUENCE, util.ISO8601_DATE)
            start = util.get_dt(sequence_to, util.ISO8601_DATE)
            target = util.get_dt(sequence_from, util.ISO8601_DATE)
            if not start or start > date.today():
                start = date.today()
            if not target or target < full_sequence_begins:
                target = full_sequence_begins
        count = 0
        current = start
        while (get_current_dates or count < self.MAX_ID_BATCH) and current > target: # only take account of max batch if gathering early dates
            result, from_dt, to_dt = self.get_id_period(current) 
            if from_dt and to_dt:
                if self.DEBUG:
                    print "Storing " + str(len(result)) + " ids gathered from " + str(from_dt) + " to " + str(to_dt)
                if result:
                    scraperwiki.sqlite.save(unique_keys=['uid'], data=result, table_name=self.TABLE_NAME)
                    if self.DEBUG: print sequence_from, sequence_to
                    if get_current_dates: # latest applications are updated on the spot
                        for i in result:
                            self.update_application_detail(i)
                    count = count + len(result)
                current = from_dt - timedelta(days=1)
            else:
                break
        if original_current_target and current > original_current_target: # error if not gathered enough current data to fully fill data gap
            return original_current_target.strftime(util.ISO8601_DATE), original_current_target.strftime(util.ISO8601_DATE), 0
        else:
            return current.strftime(util.ISO8601_DATE), start.strftime(util.ISO8601_DATE), count

    # Improved version of gather_ids()
    # process id batches working through a date sequence
    # if two parameters are supplied this is a request to gather backwards from 'to' towards 'from', returning the real date range found
    # if one parameter is supplied it's a request to gather forwards beyond 'from' towards today, returning the real date range found
    # always expects to gather some data - returned count of zero is an error
    def gather_ids2 (self, sequence_from = None, sequence_to = None):
        if not sequence_to: # gathering current dates - going forward
            move_forward = True
            target = date.today()
            start = util.get_dt(sequence_from, util.ISO8601_DATE)
            current_period_begins = target - timedelta(days=self.MIN_DAYS)
            if not start or start > current_period_begins:
                start = current_period_begins
            start = start + timedelta(days=1) # begin one day after supplied date
        else: # gathering early dates - going backward
            move_forward = False
            start = util.get_dt(sequence_to, util.ISO8601_DATE)
            target = util.get_dt(sequence_from, util.ISO8601_DATE)
            if not start or start > date.today():
                start = date.today()
            else:
                start = start - timedelta(days=1) # begin one day before supplied date
            full_sequence_begins = util.get_dt(self.START_SEQUENCE, util.ISO8601_DATE)
            if not target or target < full_sequence_begins:
                target = full_sequence_begins
        count = 0
        current = start
        ok_current = start
        while count < self.MAX_ID_BATCH and ((not move_forward and current > target) or (move_forward and current < target)): 
            result, from_dt, to_dt = self.get_id_period(current)
            if from_dt and to_dt:
                if self.DEBUG:
                    print "Storing " + str(len(result)) + " ids gathered from " + str(from_dt) + " to " + str(to_dt)
                if result:
                    scraperwiki.sqlite.save(unique_keys=['uid'], data=result, table_name=self.TABLE_NAME)
                    count = count + len(result)
                if not move_forward: # if moving backward continue even with no result, as some periods might be legitimately empty?
                    ok_current = from_dt
                    current = from_dt - timedelta(days=1)
                else:
                    if not result: break # however if moving forward we expect to get some data on each scrape
                    ok_current = to_dt
                    current = to_dt + timedelta(days=1)
                    for i in result:
                        self.update_application_detail(i) # latest applications are updated on the spot
            else:
                break
        if not move_forward:
            return ok_current.strftime(util.ISO8601_DATE), start.strftime(util.ISO8601_DATE), count
        else:
            if ok_current > date.today():
                ok_current = date.today()
            return start.strftime(util.ISO8601_DATE), ok_current.strftime(util.ISO8601_DATE), count

    # retrieves a batch of IDs around one date, to be implemented in the children
    # can return zero records if no data found for the requested period, but applicable (inclusive) dates must be returned
    def get_id_period (self, date):
        return [], None, None # invalid if return dates are not set - means try again next time

# YYYYNNNN (year + 4/5 digit sequence number) = Hereford, Tewkesbury, Walsall, Waverley, Rotherham, Ashfield, Jersey, Pembrokeshire Coast
# incrementing numeric ids = Isle of Wight, Surrey, Scilly Isles, Purbeck, Hampshire, 
# fixed one page lists = Derbyshire, Northamptonshire
# old ones not working now = Merthyr Tydfil, Newport
# now weekly = Solihull
class ListScraper(BaseScraper): # for those sites that return a full paged list of all applications 

    START_SEQUENCE = 1 # gathering back to this record number 
    PAGE_SIZE = 25
    START_POINT = 1 # the default first scrape point if the scraper is empty (only required if max_sequence is not implemented)
    MIN_RECS = 50 # min number of records to get when gathering current ids

    # process id batches working through a numeric sequence
    # (where the earliest record is nominally record number 1)
    # note 'from' is smaller than 'to'
    def gather_ids (self, sequence_from = None, sequence_to = None):
        start = sequence_to
        target = sequence_from
        if target is not None and target < self.START_SEQUENCE: # target can legitimately be null (when no data has been gathered before)
            target = self.START_SEQUENCE
        count = 0
        current = start
        while count < self.MAX_ID_BATCH and (current is None or target is None or current > target):
            result, from_rec, to_rec = self.get_id_records(target, current) # both can be null (when no data has been gathered before)
            if not start: start = to_rec
            if not current: current = to_rec
            if not target: target = self.START_SEQUENCE
            if from_rec and to_rec:
                if self.DEBUG:
                    print "Storing " + str(len(result)) + " ids gathered from " + str(from_rec) + " to " + str(to_rec)
                scraperwiki.sqlite.save(unique_keys=['uid'], data=result, table_name=self.TABLE_NAME)
                if sequence_from and not sequence_to: # latest applications are updated on the spot
                    for i in result:
                        self.update_application_detail(i)
                count = count + len(result)
                current = from_rec - 1
            else:
                break
        return current, start, count

    # Improved version of gather_ids()
    # process id batches working through a numeric sequence (where the earliest record is nominally record number 1)
    # if two parameters are supplied this is a request to gather backwards from 'to' towards 'from', returning the real sequence range found
    # if one parameter is supplied it's a request to gather forwards beyond 'from', returning the real sequence range found
    # note 'from' is always smaller than 'to'
    def gather_ids2 (self, sequence_from = None, sequence_to = None):
        max = self.get_max_sequence()
        if not sequence_to: # gathering current sequence numbers - going forward
            move_forward = True
            target = max
            start = sequence_from
            if max:
                current_period_begins = max - self.MIN_RECS
                if not start or start > current_period_begins:
                    start = current_period_begins
            if start:
                start = start + 1 # begin one after supplied sequence number
            else:
                start = self.START_POINT
        else: # gathering early sequence numbers - going backward
            move_forward = False
            start = sequence_to
            target = sequence_from
            if max and (not start or start > max):
                start = max
            else:
                start = start - 1 # begin one before supplied sequence number
            if not target or target < self.START_SEQUENCE:
                target = self.START_SEQUENCE
        count = 0
        current = start
        ok_current = start
        while count < self.MAX_ID_BATCH and (not current or not target or (not move_forward and current > target) or (move_forward and current < target)): 
            result, from_rec, to_rec = self.get_id_records2(current, move_forward)
            if not start: 
                if not move_forward:
                    start = to_rec
                else:
                    start = from_rec
                ok_current = start
            if from_rec and to_rec:
                if self.DEBUG:
                    print "Storing " + str(len(result)) + " ids gathered from " + str(from_rec) + " to " + str(to_rec)
                if result:
                    scraperwiki.sqlite.save(unique_keys=['uid'], data=result, table_name=self.TABLE_NAME)
                    count = count + len(result)
                    if not move_forward:
                        ok_current = from_rec
                        current = from_rec - 1
                    else:
                        ok_current = to_rec
                        current = to_rec + 1
                        for i in result:
                            self.update_application_detail(i) # latest applications are updated on the spot
            else:
                break
        if not move_forward:
            return ok_current, start, count
        else:
            return start, ok_current, count

    # returns current max record number - can be overridden in the children
    def get_max_sequence (self):
        return scraperwiki.sqlite.get_var(self.DATA_END_MARKER)

    # retrieves records between two sequence numbers - to be defined in the children
    # can return zero records if no data found for the requested interval, but applicable (inclusive) sequences must be returned
    def get_id_records (self, from_rec, to_rec):
        return [], None, None # invalid if return sequences are not set - means try again next time


