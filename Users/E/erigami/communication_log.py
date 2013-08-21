import BeautifulSoup as bs
import scraperwiki as sw
import time
import re
import sqlite3 as sqlite
import traceback as tb

ROOT = "https://ocl-cal.gc.ca/app/secure/orl/lrrs/do/"

# When the following is set to true, we'll skip over existing communication logs (saves one page load per entry)
SKIP_SEEN = True

class Status:

    def __init__(self):
        self.sinceLastRead = 0
        self.search_pages = 0
        self.errors = 0 # Number of errors encountered
        self.processed = 0 # Number of comms read
        self.skipped = 0 # Number comms skipped
        self.lastDate = '<unset>'


    def show(self):
        print "Search pages: %s;   Processed: %s;   Skipped: %s;   Errors: %s;   LastDate: %s;    Cpu: %ss" % (self.search_pages, self.processed, self.skipped, self.errors, self.lastDate, time.clock())


def parse_page(parsed, stat, stopOnFirstSeen):
    """Parse the table rows from the Communication log search results."""
    
    # Find the table
    table = parsed.find(name='th', attrs={'class' : 'formHeaderSub'}).findParent(name='table')

    for row in table.contents:
        if isinstance(row, bs.NavigableString):
            continue

        cells = row.findAll('td')
        if len(cells) != 3:
            continue

        # Get the date, for output-y purposes
        date = cells[0].a.string

        # Get the page and correspondence id
        path = ROOT + cells[0].a['href']

        stat.lastDate = date
        corr_id = n(_parse_correspondence(cells[1]))
        if SKIP_SEEN:
            try:
                t = sw.sqlite.select("contact_id from contact where contact_id=? and error=0", [corr_id])
                if len(t) > 0:
                    #print "Skipping %s" % corr_id
                    stat.skipped += 1
                    stat.sinceLastRead += 1
                    if stopOnFirstSeen and stat.sinceLastRead > 100:
                        print 'Terminal skip on: %s (%s)' % (corr_id, date)
                        return False
                    continue
            except sw.sqlite.NoSuchTableSqliteError:
                print "Missing table - first run?"

        print "Loading %s (%s)" % (corr_id, date)

        #print "o:%s c:%s f:%s i:%s" % (org, consultant, firm, corr_id)

        # Get the peeps who were lobbied
        detail = sw.scrape(path)

        try:        
            _parse_communication_detail(detail, path)
            stat.processed += 1
            stat.sinceLastRead = 0
        except Exception as e:
            stat.errors += 1
            try:
                sw.sqlite.save(unique_keys=['uri'], table_name='contact',
                        data={
                                'contact_id' : n(corr_id),
                                'iserror' : 1,
                                'uri' : path
                        },
                        verbose=2
                )
            finally:
                pass
            #except sw.sqlite.SqliteError:
            #    print "Could not save error record for %s" % path
            print "Error processing %s" % path
            print e            

    stat.search_pages += 1

    return True


def _parse_communication_detail(page, path):
    """Parse a communication detail page."""
    parsed = bs.BeautifulSoup(page, fromEncoding='iso-8859-1')

    # Find the table
    found = None
    for h1 in parsed.findAll('h1'):
        if h1.string.find("Communication Report Summary"):
            found = h1
            break

    if found == None:
        raise Exception("Could not find h1 in " + path)

    tab = found.findNext('table')

    # Parse the communication goodies
    org = None # Lobbying on behalf of
    lobbyist_indiv = None # Name of the individual lobbyist
    lobbyist_reg = None # Reg-id of the lobbyist
    comm_id = None # Communication id
    comm_date = None # Date of the communication
    comm_subm = None # Date the submission occured

    data = tab.findAll('tr')
    offset = 0
    if len(data) == 6:
        # lobbyist
        offset = 1
        lobbyist_indiv = data[0].find('td', {'class' : 'data'}).string
    elif len(data) == 5:
        # in-house communication
        offset = 0
    else:
        raise Exception("Bad rowcount: " + `len(data)` + " " + `data` + " from " + path)
    
    org = data[offset + 0].findAll('td')[1].strong.string
    lobbyist_reg = data[offset + 1].find('td', {'class' : 'data'}).a.string
    comm_id = data[offset + 2].find('td', {'class' : 'data'}).string
    comm_date = data[offset + 3].findAll('td')[1].string
    comm_subm = data[offset + 4].findAll('td')[1].string
    
    #print "l:%s o:%s r:%s i:%s d:%s s:%s" % (lobbyist_indiv, org, lobbyist_reg, comm_id, comm_date, comm_subm)

    # Save the lobbied names/positions
    tab = tab.findNextSibling('table')
    cur = tab.findAll('td')[1].strong
    while True:
        person = cur.string.strip()
        cur = cur.nextSibling
        title = cur.string[1:].strip()
        cur = cur.nextSibling.nextSibling
        victim_org = cur.string.strip()
        
        #print "--p:%s t:%s v:%s" % (person, title, victim_org)

        sw.sqlite.save(unique_keys=['contact_id', 'person'], table_name='victim',
                data={
                        'contact_id' : n(comm_id),
                        'person' : n(person),
                        'title' : n(title),
                        'organization' : n(victim_org)
                }
        )

        cur = cur.findNextSibling('strong')
        if None == cur:
            break

    # Get the subjects
    for td in parsed.findAll('td', {'class' : 'labelForm'}):
        if td.string.find("Subject Matter of the communication:") >= 0:
            txt = ''
            for ctt in td.findNextSibling("td", {'class' : 'tableTop'}).contents:
                if isinstance(ctt, bs.NavigableString):
                    txt += ctt.string
                else:
                    if ctt.name != 'sup':
                        raise Exception("Unexpected tag: %s" % ctt.name)

            for subj in txt.split(',&nbsp;'):
                sw.sqlite.save(unique_keys=['contact_id', 'subject'], table_name='contact_subject',
                        data={
                                'contact_id' : n(comm_id),
                                'subject' : n(subj)
                        }
                )
            

    # Save the interaction record - note that we do this AFTER the victims have been saved,
    # in case the scraper is terminated part way through. 
    sw.sqlite.save(unique_keys=['contact_id'], table_name='contact',
            data={
                    'contact_id' : n(comm_id),
                    'behalf' : n(org), 
                    'lobbyist_id' : n(lobbyist_reg),
                    'date_contact_h' : n(comm_date),
                    'date_contact_c' : _time_to_unix(comm_date),
                    'date_submitted_h' : n(comm_subm),
                    'date_submitted_c' : _time_to_unix(comm_date),
                    'uri' : path,
                    'iserror' : 0
            }
    )


def n(s):
    """Normalize the given string - strip text, replace &nbsp; with space."""
    s = s.strip()
    s = s.replace('&nbsp;', ' ')
    return re.sub(r"\s+", ' ', s)
    

def _time_to_unix(t):
     return time.mktime(time.strptime(n(t), "%Y-%m-%d"))


def _parse_correspondence(c):
    s = c.contents[-1].string.strip()
    return s[s.find(':') + 1:]


def walk_search(page, stat, stopOnFirstSeen):
    while True:
        parsed = bs.BeautifulSoup(page, fromEncoding='iso-8859-1')

        r = parse_page(parsed, stat, stopOnFirstSeen)
        stat.show()
        if not r:
            return

        page = None
        td = parsed.find(name='td', attrs={'colspan' : '4'})
        for a in td.findAll('a'):
            if "Next" == a.string:
                page = sw.scrape(ROOT + a['href'])

        if page == None:
            print "No next link"
            break
    

sw.sqlite.execute("CREATE TABLE IF NOT EXISTS contact_errors (contact_id TEXT, uri TEXT, error INTEGER);")
path = "http://false"
corr_id = "corid"
try:
    sw.sqlite.save(unique_keys=['uri'], table_name='contact_errors',
                        data={
                                'contact_id' : n(corr_id),
                                'my_error' : 1,
                                'uri' : path, 
                                'TRACE' : 'xxx'
                        },
                        verbose=2
    )
except sw.sqlite.SqliteError, e:
    tb.print_exc()
    print e
    print dir(e)
    print e.args
    print e.message
    raise e


stat = Status()


# Get the new items
print "Walking new..."
page = sw.scrape(ROOT + "_ls63_ls6f_ls6d_ls6d_ls4c_ls6f_ls67_ls50_ls75_ls62_ls6c_ls69_ls63_ls53_ls65_ls61_ls72_ls63_ls68?_STRTG3=tr", {'searchType' : 'Search'})
walk_search(page, stat, True)

# Get the old items
data = sw.sqlite.select('MIN(date_contact_c) AS c FROM contact')
oldest = time.strftime('%Y-%m-%d', time.gmtime(data[0]['c'] + 172800))
print "Walking ancients. Starting at %s." % oldest
page = sw.scrape(ROOT + "_ls63_ls6f_ls6d_ls6d_ls4c_ls6f_ls67_ls50_ls75_ls62_ls6c_ls69_ls63_ls53_ls65_ls61_ls72_ls63_ls68?_STRTG3=tr", {
        'searchType' : 'Search', 
        'registrationStatus' : 'DATE_RANGE_SEARCH_TYPE',
        'activityDateFrom' : '1900-1-1',
        'activityDateTo' : oldest
})
walk_search(page, stat, False)