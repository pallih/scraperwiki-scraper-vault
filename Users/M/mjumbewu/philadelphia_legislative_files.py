###############################################################################
# This will collect the latest legislative filings released in the city of
# Philadelphia.
###############################################################################

import scraperwiki
import httplib
import urllib2
import new
import re
import datetime
from BeautifulSoup import BeautifulSoup, Tag, NavigableString
from scraperwiki import utils

##
# HACK: Monkey patch BeatufulSoup.Tag until my change gets
#       pulled in.
#
def patchGetText(self, separator=u""):
    if not len(self.contents):
        return u""
    stopNode = self._lastRecursiveChild().next
    strings = []
    current = self.contents[0]
    while current is not stopNode:
        if isinstance(current, NavigableString):
            strings.append(current)
        current = current.next
    result = separator.join(strings)
    return re.sub(r'\s+', ' ', result)

Tag.getText = new.instancemethod(patchGetText, None, Tag)
Tag.text = property(Tag.getText)
#
##

STARTING_KEY = 72 # The highest key was 11001 as of 5 Apr 2011

class PhillyLegistarSiteWrapper (object):
    """
    A facade over the Philadelphia city council legistar site data.  It is
    responsible for scraping data out of the site.  The main external point
    of interaction is scrape_legis_file.
    """

    STARTING_URL = 'http://legislation.phila.gov/detailreport/?key='

    def urlopen(self, *args, **kwargs):
        return urllib2.urlopen(*args, **kwargs)

    def scrape_legis_file(self, key, soup):
        '''Extract a record from the given document (soup). The key is for the
           sake of record-keeping.  It is the key passed to the site URL.'''

        span = soup.find('span', {'id':'lblFileNumberValue'})
        lid = span.text

        span = soup.find('span', {'id':'lblFileTypeValue'})
        ltype = span.text

        span = soup.find('span', {'id':'lblFileStatusValue'})
        lstatus = span.text

        span = soup.find('span', {'id':'lblTitleValue'})
        ltitle = span.text

        span = soup.find('span', {'id':'lblControllingBodyValue'})
        lbody = span.text

        span = soup.find('span', {'id':'lblIntroDateValue'})
        lintro = span.text

        span = soup.find('span', {'id':'lblFinalActionValue'})
        lfinal = span.text

        span = soup.find('span', {'id':'lblVersionValue'})
        lversion = span.text

        span = soup.find('span', {'id':'lblContactValue'})
        lcontact = span.text

        span = soup.find('span', {'id':'lblSponsorsValue'})
        lsponsors = span.text

        record = {
            'key' : key,
            'id' : lid,
            'url' : self.STARTING_URL + str(key),
            'type' : ltype.strip(),
            'status' : lstatus.strip(),
            'title' : ltitle.strip(),
            'controlling_body' : lbody,
            'intro_date' : self.convert_date(lintro),
            'final_date' : self.convert_date(lfinal),
            'version' : lversion,
            'contact' : lcontact.strip(),
            'sponsors' : lsponsors
        }

        attachments = self.scrape_legis_attachments(key, soup)
        actions = self.scrape_legis_actions(key, soup)
        minutes = self.collect_minutes(actions)

        print record, attachments, actions, minutes
        return record, attachments, actions, minutes

    def get_minutes_date(self, minutes_url):
        date_match = re.search('_(\d{2})-(\d{2})-(\d{2})_', minutes_url)
        if date_match:
            date_taken = datetime.date(
                year=int('20' + date_match.group(1)),
                month=int(date_match.group(2)),
                day=int(date_match.group(3)),
            )
        else:
            date_taken = ''

        return date_taken

    def get_minutes_doc(self, minutes_url):
        fulltext = self.extract_pdf_text(minutes_url)
        date_taken = self.get_minutes_date(minutes_url)

        minutes_doc = {
            'url' : minutes_url,
            'fulltext' : fulltext,
            'date_taken' : date_taken,
        }

        return minutes_doc

    def collect_minutes(self, actions):
        """
        Given a list of legislative actions, collect the minutes data attached
        to those actions.
        """

        minutes = {}
        for action in actions:
            minutes_url = action['minutes_url']
            if minutes_url.endswith('.pdf'):
                minutes_doc = self.get_minutes_doc(minutes_url)
                minutes[minutes_url] = minutes_doc

        return minutes.values()

    def scrape_legis_attachments(self, key, soup):
        """
        Given a beautiful soup representation of legislative file, return the
        list of attachments.
        """

        attachments = []

        attach_div = soup.find('div', {'id' : 'divAttachmentsValue'})
        for cell in attach_div.findAll('a'):
            url = cell['href']

            if url.endswith('.pdf'):
                fulltext = self.extract_pdf_text(url)
            else:
                fulltext = ''

            attachment = {
                'key' : key,
                'description' : cell.text,
                'url' : url,
                'fulltext' : fulltext,
            }
            attachments.append(attachment)

        return attachments

    def scrape_legis_actions(self, key, soup):
        """
        Given a beautiful soup representation of a legislative file,
        return the actions taken on the file.
        """

        def get_action_cell_text(cell):
            cell_a = cell.find('a')
            if cell_a:
                return cell_a.text
            else:
                return cell.text

        def get_action_cell_resource(cell):
            cell_a = cell.find('a')
            if cell_a:
                return cell_a['href']
            else:
                return ''

        notes = []
        actions = []

        action_div = soup.find('div', {'id': 'divScroll'})
        action_rows = action_div.findAll('tr')

        for action_row in action_rows:
            cells = action_row.findAll('td')

            if len(cells) == 2:
                # Sometimes, there are notes interspersed in the history table.
                # Luckily (?) their rows have only two cells instead of four, so
                # we can easily tell that they're there.
                action = actions[-1]
                action['notes'] = cells[1].text.strip()
                continue

            action = {
                'key' : key,
                'date_taken' : self.convert_date(get_action_cell_text(cells[0])),
                'acting_body' : get_action_cell_text(cells[1]).strip(),
                'description' : get_action_cell_text(cells[2]).strip(),
                'motion' : get_action_cell_text(cells[3]).strip(),
                'minutes_url' : get_action_cell_resource(cells[0]).strip(),
                'notes' : '',
            }
            actions.append(action)

        return actions

    __pdf_cache = None
    def init_pdf_cache(self, seed=None):
        if seed is None:
            seed = {}
        self.__pdf_cache = self.__pdf_cache or seed

    def extract_pdf_text(self, pdf_data, tries_left=5):
        """
        Given an http[s] URL, a file URL, or a file-like object containing
        PDF data, return the text from the PDF.  Cache URLs or data that have
        already been seen.
        """

        self.init_pdf_cache()

        pdf_key = pdf_data
        if pdf_key in self.__pdf_cache:
            pdf_content = unicode(self.__pdf_cache[pdf_key])
            if pdf_content not in [None, 'None']:
                return pdf_content

        if pdf_key.startswith('file://'):
            path = pdf_key[7:]
            pdf_data = open(path).read()
        elif pdf_key.startswith('http://') or pdf_key.startswith('https://'):
            url = pdf_key
            try:
                pdf_data = self.urlopen(url).read()

            # Protect against removed PDFs (ones that result in 404 HTTP
            # response code).  I don't know why they've removed some PDFs
            # but they have.
            except urllib2.HTTPError, err:
                if err.code == 404:
                    self.__pdf_cache[pdf_key] = ''
                    return ''
                else:
                    raise

            # Been getting timeout exceptions every so often, so try again
            # if timed out.
            except urllib2.URLError, err:
                if tries_left:
                    return self.extract_pdf_text(pdf_key, tries_left-1)

        xml_data = utils.pdftoxml(pdf_data)

        self.__pdf_cache[pdf_key] = self.extract_xml_text(xml_data, 'pdf2xml')
        return self.__pdf_cache[pdf_key]

    def extract_xml_text(self, xml_data, root_node_name):
        soup = BeautifulSoup(xml_data)
        root_node = soup.find(root_node_name)

        if root_node:
            xml_text = root_node.text
            return xml_text
        # Some PDFs are images
        else:
            return ''

    def convert_date(self, orig_date):
        if orig_date:
            return datetime.datetime.strptime(orig_date, '%m/%d/%Y').date()
        else:
            return ''


    def is_error_page(self, soup):
        '''Check the given soup to see if it represents an error page.'''
        error_p = soup.find('p', 'errorText')

        if error_p is None: return False
        else: return True

    def check_for_new_content(self, last_key):
        '''Look through the next 10 keys to see if there are any more files.
           10 is arbitrary, but I feel like it's large enough to be safe.'''

        curr_key = last_key
        for _ in xrange(10):
            curr_key = curr_key + 1

            url = self.STARTING_URL + str(curr_key)
            more_tries = 10
            while True:
                try:
                    html = self.urlopen(url)
                    break

                # Sometimes the server will respond with a status line that httplib
                # does not understand (an empty status line, in particular).  When
                # this happens, keep trying to access the page.  Give up after 10
                # tries.
                except httplib.BadStatusLine, ex:
                    more_tries -= 1;
                    print 'Received BadStatusLine exception %r for url %r' % (ex, url)
                    if not more_tries:
                        raise

                # Sometimes the server will do things like just take too long to
                # respond.  When it does, try again 10 times.
                except urllib2.URLError, ex:
                    more_tries -= 1;
                    print 'Received URLError exception %r for url %r' % (ex, url)
                    if not more_tries:
                        raise
            soup = BeautifulSoup(html)

            if not self.is_error_page(soup):
                return curr_key, soup

        return curr_key, None


class CacheMachine (object):
    """
    A CacheMachine allows lazy-loading of a string value.  Give it a callable
    and it will run that callable the first time the string value of the object
    is requested.  It will store the value for future retrievals.
    
    CacheMachine exists to circumvent the inability for this scraper to load the
    entire minutes or attachments tables at once from within a ScraperWiki 
    process.
    """
    def __init__(self, callable):
        self.__callable = callable
    
    def __unicode__(self):
        if not hasattr(self, 'cache'):
            self.cache = self.__callable()
        return unicode(self.cache)


class ScraperWikiDataStoreWrapper (object):
    """
    This is the interface over an arbitrary database where the information is
    being stored.  I'm using it primarily because I want the scraper code to be
    used on both ScraperWiki and in my Django app on my Django models.  For my
    app, I want local access to the data.  But I love ScraperWiki as a central
    place where you can find data about anything you want, so it's important to
    have the data available here as well.
    """
    def get_latest_key(self):
        '''Check the datastore for the key of the most recent filing.'''

        max_key = STARTING_KEY

        try:
            records = scraperwiki.sqlite.select('* from swdata order by key desc limit 1')
            if records:
                record = records[0]
                max_key = record['key']
        except scraperwiki.sqlite.NoSuchTableSqliteError:
            pass

        return int(max_key)

    def get_continuation_key(self):
        return scraperwiki.sqlite.get_var('continuation_key', 72)

    def save_continuation_key(self, key):
        scraperwiki.sqlite.save_var('continuation_key', key)

    def save_legis_file(self, record, attachments, actions, minuteses):
        """
        Take a legislative file record and do whatever needs to be
        done to get it into the database.
        """
        # Convert m/d/y dates into date objects.
        scraperwiki.sqlite.save(['key'], record)
        for attachment in attachments:
            scraperwiki.sqlite.save(['key','url'], attachment, table_name='attachments')
        for minutes in minuteses:
            scraperwiki.sqlite.save(['url'], minutes, table_name='minutes')
        for action in actions:
            scraperwiki.sqlite.save(['key','date_taken','description','notes'], action, table_name='actions')

    @property
    def pdf_mapping(self):
        """
        Build a mapping of the URLs and PDF test that already exist in the
        database.
        """
        mapping = {}

        def get_stored_fulltext(table, url):
            print 'Searching the cache for fulltext for url %r...' % (url,),
            row = scraperwiki.sqlite.select('fulltext from %s where url=?' % table, [url])
            if row:
                print 'found it!'
                return row[0]['fulltext']
            else:
                print "couldn't find it."
                return None

        attachments = scraperwiki.sqlite.select('url from attachments')
        for attachment in attachments:
            url = attachment['url']
            mapping[url] = CacheMachine(lambda: get_stored_fulltext('attachments', url))

        minuteses = scraperwiki.sqlite.select('url from minutes')
        for minutes in minuteses:
            url = minutes['url']
            mapping[url] = CacheMachine(lambda: get_stored_fulltext('minutes', url))

        return mapping

        
def import_leg_files(start_key, source, ds, save_key=False):
    """
    Imports the legislative filings starting at the given key, and going either
    until there it reaches the end of the available records, or the script times
    out.
    """
    curr_key = start_key
    while True:
        curr_key, soup = source.check_for_new_content(curr_key)
        
        if soup is None:
            return
        
        record, attachments, actions, minutes = source.scrape_legis_file(curr_key, soup)
        ds.save_legis_file(record, attachments, actions, minutes)
        if save_key:
            ds.save_continuation_key(curr_key)



# Create a datastore wrapper object
ds = ScraperWikiDataStoreWrapper()
source = PhillyLegistarSiteWrapper()
print 'set up the objects'

# Seed the PDF cache with already-downloaded content.
#
# Downloading and parsing PDF content really slows down the scraping
# process.  If we had to redownload all of them every time we scraped,
# it would take a really long time to refresh all of the old stuff.  So
# that PDFs that have already been downloaded won't be again, seed the
# source cache with that data.
#
# This might be too much of a burden on memory.
source.init_pdf_cache(ds.pdf_mapping)
print 'initialized the cache'

# Get the latest filings
latest_key = ds.get_latest_key()
import_leg_files(latest_key, source, ds)
print 'imported new stuff'

# Continue updating the entire datastore
cont_key = ds.get_continuation_key()
import_leg_files(cont_key, source, ds, save_key=True)
print 'updated old stuff'

# If we've made it here, then we have all the latest filings, and we have gone 
# through and updated the entire datastore.  Now, reset the continuation key to 
# get ready for the next go-around.
ds.save_continuation_key(72)
###############################################################################
# This will collect the latest legislative filings released in the city of
# Philadelphia.
###############################################################################

import scraperwiki
import httplib
import urllib2
import new
import re
import datetime
from BeautifulSoup import BeautifulSoup, Tag, NavigableString
from scraperwiki import utils

##
# HACK: Monkey patch BeatufulSoup.Tag until my change gets
#       pulled in.
#
def patchGetText(self, separator=u""):
    if not len(self.contents):
        return u""
    stopNode = self._lastRecursiveChild().next
    strings = []
    current = self.contents[0]
    while current is not stopNode:
        if isinstance(current, NavigableString):
            strings.append(current)
        current = current.next
    result = separator.join(strings)
    return re.sub(r'\s+', ' ', result)

Tag.getText = new.instancemethod(patchGetText, None, Tag)
Tag.text = property(Tag.getText)
#
##

STARTING_KEY = 72 # The highest key was 11001 as of 5 Apr 2011

class PhillyLegistarSiteWrapper (object):
    """
    A facade over the Philadelphia city council legistar site data.  It is
    responsible for scraping data out of the site.  The main external point
    of interaction is scrape_legis_file.
    """

    STARTING_URL = 'http://legislation.phila.gov/detailreport/?key='

    def urlopen(self, *args, **kwargs):
        return urllib2.urlopen(*args, **kwargs)

    def scrape_legis_file(self, key, soup):
        '''Extract a record from the given document (soup). The key is for the
           sake of record-keeping.  It is the key passed to the site URL.'''

        span = soup.find('span', {'id':'lblFileNumberValue'})
        lid = span.text

        span = soup.find('span', {'id':'lblFileTypeValue'})
        ltype = span.text

        span = soup.find('span', {'id':'lblFileStatusValue'})
        lstatus = span.text

        span = soup.find('span', {'id':'lblTitleValue'})
        ltitle = span.text

        span = soup.find('span', {'id':'lblControllingBodyValue'})
        lbody = span.text

        span = soup.find('span', {'id':'lblIntroDateValue'})
        lintro = span.text

        span = soup.find('span', {'id':'lblFinalActionValue'})
        lfinal = span.text

        span = soup.find('span', {'id':'lblVersionValue'})
        lversion = span.text

        span = soup.find('span', {'id':'lblContactValue'})
        lcontact = span.text

        span = soup.find('span', {'id':'lblSponsorsValue'})
        lsponsors = span.text

        record = {
            'key' : key,
            'id' : lid,
            'url' : self.STARTING_URL + str(key),
            'type' : ltype.strip(),
            'status' : lstatus.strip(),
            'title' : ltitle.strip(),
            'controlling_body' : lbody,
            'intro_date' : self.convert_date(lintro),
            'final_date' : self.convert_date(lfinal),
            'version' : lversion,
            'contact' : lcontact.strip(),
            'sponsors' : lsponsors
        }

        attachments = self.scrape_legis_attachments(key, soup)
        actions = self.scrape_legis_actions(key, soup)
        minutes = self.collect_minutes(actions)

        print record, attachments, actions, minutes
        return record, attachments, actions, minutes

    def get_minutes_date(self, minutes_url):
        date_match = re.search('_(\d{2})-(\d{2})-(\d{2})_', minutes_url)
        if date_match:
            date_taken = datetime.date(
                year=int('20' + date_match.group(1)),
                month=int(date_match.group(2)),
                day=int(date_match.group(3)),
            )
        else:
            date_taken = ''

        return date_taken

    def get_minutes_doc(self, minutes_url):
        fulltext = self.extract_pdf_text(minutes_url)
        date_taken = self.get_minutes_date(minutes_url)

        minutes_doc = {
            'url' : minutes_url,
            'fulltext' : fulltext,
            'date_taken' : date_taken,
        }

        return minutes_doc

    def collect_minutes(self, actions):
        """
        Given a list of legislative actions, collect the minutes data attached
        to those actions.
        """

        minutes = {}
        for action in actions:
            minutes_url = action['minutes_url']
            if minutes_url.endswith('.pdf'):
                minutes_doc = self.get_minutes_doc(minutes_url)
                minutes[minutes_url] = minutes_doc

        return minutes.values()

    def scrape_legis_attachments(self, key, soup):
        """
        Given a beautiful soup representation of legislative file, return the
        list of attachments.
        """

        attachments = []

        attach_div = soup.find('div', {'id' : 'divAttachmentsValue'})
        for cell in attach_div.findAll('a'):
            url = cell['href']

            if url.endswith('.pdf'):
                fulltext = self.extract_pdf_text(url)
            else:
                fulltext = ''

            attachment = {
                'key' : key,
                'description' : cell.text,
                'url' : url,
                'fulltext' : fulltext,
            }
            attachments.append(attachment)

        return attachments

    def scrape_legis_actions(self, key, soup):
        """
        Given a beautiful soup representation of a legislative file,
        return the actions taken on the file.
        """

        def get_action_cell_text(cell):
            cell_a = cell.find('a')
            if cell_a:
                return cell_a.text
            else:
                return cell.text

        def get_action_cell_resource(cell):
            cell_a = cell.find('a')
            if cell_a:
                return cell_a['href']
            else:
                return ''

        notes = []
        actions = []

        action_div = soup.find('div', {'id': 'divScroll'})
        action_rows = action_div.findAll('tr')

        for action_row in action_rows:
            cells = action_row.findAll('td')

            if len(cells) == 2:
                # Sometimes, there are notes interspersed in the history table.
                # Luckily (?) their rows have only two cells instead of four, so
                # we can easily tell that they're there.
                action = actions[-1]
                action['notes'] = cells[1].text.strip()
                continue

            action = {
                'key' : key,
                'date_taken' : self.convert_date(get_action_cell_text(cells[0])),
                'acting_body' : get_action_cell_text(cells[1]).strip(),
                'description' : get_action_cell_text(cells[2]).strip(),
                'motion' : get_action_cell_text(cells[3]).strip(),
                'minutes_url' : get_action_cell_resource(cells[0]).strip(),
                'notes' : '',
            }
            actions.append(action)

        return actions

    __pdf_cache = None
    def init_pdf_cache(self, seed=None):
        if seed is None:
            seed = {}
        self.__pdf_cache = self.__pdf_cache or seed

    def extract_pdf_text(self, pdf_data, tries_left=5):
        """
        Given an http[s] URL, a file URL, or a file-like object containing
        PDF data, return the text from the PDF.  Cache URLs or data that have
        already been seen.
        """

        self.init_pdf_cache()

        pdf_key = pdf_data
        if pdf_key in self.__pdf_cache:
            pdf_content = unicode(self.__pdf_cache[pdf_key])
            if pdf_content not in [None, 'None']:
                return pdf_content

        if pdf_key.startswith('file://'):
            path = pdf_key[7:]
            pdf_data = open(path).read()
        elif pdf_key.startswith('http://') or pdf_key.startswith('https://'):
            url = pdf_key
            try:
                pdf_data = self.urlopen(url).read()

            # Protect against removed PDFs (ones that result in 404 HTTP
            # response code).  I don't know why they've removed some PDFs
            # but they have.
            except urllib2.HTTPError, err:
                if err.code == 404:
                    self.__pdf_cache[pdf_key] = ''
                    return ''
                else:
                    raise

            # Been getting timeout exceptions every so often, so try again
            # if timed out.
            except urllib2.URLError, err:
                if tries_left:
                    return self.extract_pdf_text(pdf_key, tries_left-1)

        xml_data = utils.pdftoxml(pdf_data)

        self.__pdf_cache[pdf_key] = self.extract_xml_text(xml_data, 'pdf2xml')
        return self.__pdf_cache[pdf_key]

    def extract_xml_text(self, xml_data, root_node_name):
        soup = BeautifulSoup(xml_data)
        root_node = soup.find(root_node_name)

        if root_node:
            xml_text = root_node.text
            return xml_text
        # Some PDFs are images
        else:
            return ''

    def convert_date(self, orig_date):
        if orig_date:
            return datetime.datetime.strptime(orig_date, '%m/%d/%Y').date()
        else:
            return ''


    def is_error_page(self, soup):
        '''Check the given soup to see if it represents an error page.'''
        error_p = soup.find('p', 'errorText')

        if error_p is None: return False
        else: return True

    def check_for_new_content(self, last_key):
        '''Look through the next 10 keys to see if there are any more files.
           10 is arbitrary, but I feel like it's large enough to be safe.'''

        curr_key = last_key
        for _ in xrange(10):
            curr_key = curr_key + 1

            url = self.STARTING_URL + str(curr_key)
            more_tries = 10
            while True:
                try:
                    html = self.urlopen(url)
                    break

                # Sometimes the server will respond with a status line that httplib
                # does not understand (an empty status line, in particular).  When
                # this happens, keep trying to access the page.  Give up after 10
                # tries.
                except httplib.BadStatusLine, ex:
                    more_tries -= 1;
                    print 'Received BadStatusLine exception %r for url %r' % (ex, url)
                    if not more_tries:
                        raise

                # Sometimes the server will do things like just take too long to
                # respond.  When it does, try again 10 times.
                except urllib2.URLError, ex:
                    more_tries -= 1;
                    print 'Received URLError exception %r for url %r' % (ex, url)
                    if not more_tries:
                        raise
            soup = BeautifulSoup(html)

            if not self.is_error_page(soup):
                return curr_key, soup

        return curr_key, None


class CacheMachine (object):
    """
    A CacheMachine allows lazy-loading of a string value.  Give it a callable
    and it will run that callable the first time the string value of the object
    is requested.  It will store the value for future retrievals.
    
    CacheMachine exists to circumvent the inability for this scraper to load the
    entire minutes or attachments tables at once from within a ScraperWiki 
    process.
    """
    def __init__(self, callable):
        self.__callable = callable
    
    def __unicode__(self):
        if not hasattr(self, 'cache'):
            self.cache = self.__callable()
        return unicode(self.cache)


class ScraperWikiDataStoreWrapper (object):
    """
    This is the interface over an arbitrary database where the information is
    being stored.  I'm using it primarily because I want the scraper code to be
    used on both ScraperWiki and in my Django app on my Django models.  For my
    app, I want local access to the data.  But I love ScraperWiki as a central
    place where you can find data about anything you want, so it's important to
    have the data available here as well.
    """
    def get_latest_key(self):
        '''Check the datastore for the key of the most recent filing.'''

        max_key = STARTING_KEY

        try:
            records = scraperwiki.sqlite.select('* from swdata order by key desc limit 1')
            if records:
                record = records[0]
                max_key = record['key']
        except scraperwiki.sqlite.NoSuchTableSqliteError:
            pass

        return int(max_key)

    def get_continuation_key(self):
        return scraperwiki.sqlite.get_var('continuation_key', 72)

    def save_continuation_key(self, key):
        scraperwiki.sqlite.save_var('continuation_key', key)

    def save_legis_file(self, record, attachments, actions, minuteses):
        """
        Take a legislative file record and do whatever needs to be
        done to get it into the database.
        """
        # Convert m/d/y dates into date objects.
        scraperwiki.sqlite.save(['key'], record)
        for attachment in attachments:
            scraperwiki.sqlite.save(['key','url'], attachment, table_name='attachments')
        for minutes in minuteses:
            scraperwiki.sqlite.save(['url'], minutes, table_name='minutes')
        for action in actions:
            scraperwiki.sqlite.save(['key','date_taken','description','notes'], action, table_name='actions')

    @property
    def pdf_mapping(self):
        """
        Build a mapping of the URLs and PDF test that already exist in the
        database.
        """
        mapping = {}

        def get_stored_fulltext(table, url):
            print 'Searching the cache for fulltext for url %r...' % (url,),
            row = scraperwiki.sqlite.select('fulltext from %s where url=?' % table, [url])
            if row:
                print 'found it!'
                return row[0]['fulltext']
            else:
                print "couldn't find it."
                return None

        attachments = scraperwiki.sqlite.select('url from attachments')
        for attachment in attachments:
            url = attachment['url']
            mapping[url] = CacheMachine(lambda: get_stored_fulltext('attachments', url))

        minuteses = scraperwiki.sqlite.select('url from minutes')
        for minutes in minuteses:
            url = minutes['url']
            mapping[url] = CacheMachine(lambda: get_stored_fulltext('minutes', url))

        return mapping

        
def import_leg_files(start_key, source, ds, save_key=False):
    """
    Imports the legislative filings starting at the given key, and going either
    until there it reaches the end of the available records, or the script times
    out.
    """
    curr_key = start_key
    while True:
        curr_key, soup = source.check_for_new_content(curr_key)
        
        if soup is None:
            return
        
        record, attachments, actions, minutes = source.scrape_legis_file(curr_key, soup)
        ds.save_legis_file(record, attachments, actions, minutes)
        if save_key:
            ds.save_continuation_key(curr_key)



# Create a datastore wrapper object
ds = ScraperWikiDataStoreWrapper()
source = PhillyLegistarSiteWrapper()
print 'set up the objects'

# Seed the PDF cache with already-downloaded content.
#
# Downloading and parsing PDF content really slows down the scraping
# process.  If we had to redownload all of them every time we scraped,
# it would take a really long time to refresh all of the old stuff.  So
# that PDFs that have already been downloaded won't be again, seed the
# source cache with that data.
#
# This might be too much of a burden on memory.
source.init_pdf_cache(ds.pdf_mapping)
print 'initialized the cache'

# Get the latest filings
latest_key = ds.get_latest_key()
import_leg_files(latest_key, source, ds)
print 'imported new stuff'

# Continue updating the entire datastore
cont_key = ds.get_continuation_key()
import_leg_files(cont_key, source, ds, save_key=True)
print 'updated old stuff'

# If we've made it here, then we have all the latest filings, and we have gone 
# through and updated the entire datastore.  Now, reset the continuation key to 
# get ready for the next go-around.
ds.save_continuation_key(72)
