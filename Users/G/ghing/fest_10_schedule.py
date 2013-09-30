import scraperwiki
import lxml.html
import re
import unicodedata
from datetime import datetime, timedelta

def is_schedule(table):
    """ Does the table represent the schedule for one of the days? """
    if table.cssselect("span.date"):
        return True
    return False

def is_set_time(s):
    set_time_expr = re.compile('\d{1,2}:\d{2,2} - \d{1,2}:\d{2,2}')
    return set_time_expr.match(s) is not None

def parse_date(date_raw):
    date_clean = date_raw.strip().replace('th', '')
    date = datetime.strptime(date_clean, '%A %B %d')
    date = date.replace(year=datetime.today().year)
    return date
    
def parse_set_time(date_raw, time_raw):
    """ Extract the set start and end times in RFC822 / IETF date syntax """
    date = parse_date(date_raw)
    time_expr = re.compile('(?P<start_hour>\d{1,2}):(?P<start_minute>\d{2,2}) - (?P<end_hour>\d{1,2}):(?P<end_minute>\d{2,2})')
    match = time_expr.search(time_raw)
    start_hour_num = (int) (match.group('start_hour'))
    start_minute_num = (int) (match.group('start_minute'))
    end_hour_num = (int) (match.group('end_hour'))
    end_minute_num = (int) (match.group('end_minute'))

    if start_hour_num < 12 and end_hour_num < 12:
        if (not (end_hour_num < start_hour_num)):
            start_time_change = timedelta(hours=start_hour_num + 12, minutes=start_minute_num)
            end_time_change = timedelta(hours=end_hour_num + 12, minutes=end_minute_num)
        else:
            start_time_change = timedelta(hours=start_hour_num + 12, minutes=start_minute_num)
            end_time_change = timedelta(days=1, hours=end_hour_num, minutes=end_minute_num)
    else:                
        start_time_change = timedelta(days=1, hours=start_hour_num-12, minutes=start_minute_num)
        if (end_hour_num < 12):
            end_time_change = timedelta(days=1, hours=end_hour_num, minutes=end_minute_num)
        else:
            end_time_change = timedelta(days=1, hours=end_hour_num-12, minutes=end_minute_num)

    return (date + start_time_change, date + end_time_change)  

def strftime_iso8601(dt):
    time_format = "%Y-%m-%dT%H:%M"
    return dt.strftime(time_format)

def strftime_rfc822(dt):
    """ 
    Convert time formatted in ISO 8601 format to RFC 822 format

    This is neccessary because SQLite's date functions use ISO 8601
    while JavaScript can only do RFC 822.
    """
    time_format = "%a, %b %d, %Y %H:%M:00 GMT-0400"
    return dt.strftime(time_format)

def slugify_venue_name(venue_name):
    """ 
    Create a slug for the venue based on its name.

    Based on http://stackoverflow.com/questions/5574042/string-slugification-in-python

    """
    # venue_name doesn't seem to be unicode, so these don't work/
    # aren't neccessary
    #slug = unicodedata.normalize('NFKD', venue_name)    
    #slug = slug.encode('ascii', 'ignore')
    slug = venue_name
    # Strip Razorcake showcase information
    slug = re.sub(r'RAZORCAKE 10 YEAR ANNIVERSARY SHOWCASEAT ', '', slug)
    slug = slug.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    slug = re.sub(r'[-]+', '-', slug)
    return slug
 
def save_set(date, venue, band, time):
    (start_time, end_time) = parse_set_time(date, time)
    scraperwiki.sqlite.save(unique_keys=[], data={
        "venue":venue.strip(), 
        "venue_slug": slugify_venue_name(venue),
        "band":band.strip(), 
        "start_time_iso8601":strftime_iso8601(start_time), 
        "end_time_iso8601":strftime_iso8601(end_time),
        "start_time_rfc822":strftime_rfc822(start_time),
        "end_time_rfc822":strftime_rfc822(end_time)}, table_name="sets")   

def parse_venue_schedule(table, date):
    venue = table.cssselect("td.style1")[0].text_content()
    for row in table.xpath("tr/td[@class='text']/.."):
        (band, time) = [td.text_content() for td in row.xpath("td")]
        if is_set_time(time):
            save_set(date, venue, band, time)

def get_schedules(root, count=None):
    schedules = [table for table in root.cssselect("table")
                 if is_schedule(table)]
    if count is None:
         return schedules
    else:
         return schedules[:count]

def parse_schedule(table):
    date = table.cssselect("span.date")[0].text_content()
    for venue_table in table.xpath("tr/td/table/tr/td/table[@bordercolor='#6b6759']"):
        parse_venue_schedule(venue_table, date)

def parse_schedules(root):
    for table in get_schedules(root):
        parse_schedule(table)

def save_venue(name, street, city, state):
    scraperwiki.sqlite.save(unique_keys=[], data={
        "name":name,
        "slug": slugify_venue_name(name),
        "street":street,
        "city":city,
        "state":state}, table_name="venues")    

def clean_street(street):
    clean_street = street.strip()
    clean_street = clean_street.replace('Street', 'St')
    clean_street = clean_street.replace('Stree', 'St')
    clean_street = clean_street.replace('St.', 'St')
    clean_street = clean_street.replace('Avenue', 'Ave')
    clean_street = clean_street.replace('Southeast', 'SE')
    clean_street = clean_street.replace('South', 'S')
    clean_street = clean_street.replace('S.', 'S')
    clean_street = clean_street.replace('West', 'W')
    clean_street = clean_street.replace('W.', 'W')
    clean_street = clean_street.replace('North', 'N')
    return clean_street
    
def parse_venues(root):
    for venue_cell in root.cssselect('td.style4'):
        venue_name = None
        venue_street = None

        for child in venue_cell:
            if child.text is not None and child.text.strip() != "":
                venue_name = child.text
            
            if child.tail is not None and child.tail.strip() != "":
                venue_street = child.tail
            
            # Special case for "The Atlantic".  The venue address is 
            # wrapped in the <strong> tag along with the name
            if venue_street is None and len(child) > 0 and child[0].tail is not None:
                venue_street = child[0].tail
            
        save_venue(venue_name, clean_street(venue_street), "Gainesville", "FL")        

html = scraperwiki.scrape("http://thefestfl.com/fest10schedule.html")
root = lxml.html.fromstring(html)
scraperwiki.sqlite.execute("drop table if exists swdata")
scraperwiki.sqlite.execute("drop table if exists venues")
scraperwiki.sqlite.execute("drop table if exists sets")
parse_venues(root)
parse_schedules(root)import scraperwiki
import lxml.html
import re
import unicodedata
from datetime import datetime, timedelta

def is_schedule(table):
    """ Does the table represent the schedule for one of the days? """
    if table.cssselect("span.date"):
        return True
    return False

def is_set_time(s):
    set_time_expr = re.compile('\d{1,2}:\d{2,2} - \d{1,2}:\d{2,2}')
    return set_time_expr.match(s) is not None

def parse_date(date_raw):
    date_clean = date_raw.strip().replace('th', '')
    date = datetime.strptime(date_clean, '%A %B %d')
    date = date.replace(year=datetime.today().year)
    return date
    
def parse_set_time(date_raw, time_raw):
    """ Extract the set start and end times in RFC822 / IETF date syntax """
    date = parse_date(date_raw)
    time_expr = re.compile('(?P<start_hour>\d{1,2}):(?P<start_minute>\d{2,2}) - (?P<end_hour>\d{1,2}):(?P<end_minute>\d{2,2})')
    match = time_expr.search(time_raw)
    start_hour_num = (int) (match.group('start_hour'))
    start_minute_num = (int) (match.group('start_minute'))
    end_hour_num = (int) (match.group('end_hour'))
    end_minute_num = (int) (match.group('end_minute'))

    if start_hour_num < 12 and end_hour_num < 12:
        if (not (end_hour_num < start_hour_num)):
            start_time_change = timedelta(hours=start_hour_num + 12, minutes=start_minute_num)
            end_time_change = timedelta(hours=end_hour_num + 12, minutes=end_minute_num)
        else:
            start_time_change = timedelta(hours=start_hour_num + 12, minutes=start_minute_num)
            end_time_change = timedelta(days=1, hours=end_hour_num, minutes=end_minute_num)
    else:                
        start_time_change = timedelta(days=1, hours=start_hour_num-12, minutes=start_minute_num)
        if (end_hour_num < 12):
            end_time_change = timedelta(days=1, hours=end_hour_num, minutes=end_minute_num)
        else:
            end_time_change = timedelta(days=1, hours=end_hour_num-12, minutes=end_minute_num)

    return (date + start_time_change, date + end_time_change)  

def strftime_iso8601(dt):
    time_format = "%Y-%m-%dT%H:%M"
    return dt.strftime(time_format)

def strftime_rfc822(dt):
    """ 
    Convert time formatted in ISO 8601 format to RFC 822 format

    This is neccessary because SQLite's date functions use ISO 8601
    while JavaScript can only do RFC 822.
    """
    time_format = "%a, %b %d, %Y %H:%M:00 GMT-0400"
    return dt.strftime(time_format)

def slugify_venue_name(venue_name):
    """ 
    Create a slug for the venue based on its name.

    Based on http://stackoverflow.com/questions/5574042/string-slugification-in-python

    """
    # venue_name doesn't seem to be unicode, so these don't work/
    # aren't neccessary
    #slug = unicodedata.normalize('NFKD', venue_name)    
    #slug = slug.encode('ascii', 'ignore')
    slug = venue_name
    # Strip Razorcake showcase information
    slug = re.sub(r'RAZORCAKE 10 YEAR ANNIVERSARY SHOWCASEAT ', '', slug)
    slug = slug.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    slug = re.sub(r'[-]+', '-', slug)
    return slug
 
def save_set(date, venue, band, time):
    (start_time, end_time) = parse_set_time(date, time)
    scraperwiki.sqlite.save(unique_keys=[], data={
        "venue":venue.strip(), 
        "venue_slug": slugify_venue_name(venue),
        "band":band.strip(), 
        "start_time_iso8601":strftime_iso8601(start_time), 
        "end_time_iso8601":strftime_iso8601(end_time),
        "start_time_rfc822":strftime_rfc822(start_time),
        "end_time_rfc822":strftime_rfc822(end_time)}, table_name="sets")   

def parse_venue_schedule(table, date):
    venue = table.cssselect("td.style1")[0].text_content()
    for row in table.xpath("tr/td[@class='text']/.."):
        (band, time) = [td.text_content() for td in row.xpath("td")]
        if is_set_time(time):
            save_set(date, venue, band, time)

def get_schedules(root, count=None):
    schedules = [table for table in root.cssselect("table")
                 if is_schedule(table)]
    if count is None:
         return schedules
    else:
         return schedules[:count]

def parse_schedule(table):
    date = table.cssselect("span.date")[0].text_content()
    for venue_table in table.xpath("tr/td/table/tr/td/table[@bordercolor='#6b6759']"):
        parse_venue_schedule(venue_table, date)

def parse_schedules(root):
    for table in get_schedules(root):
        parse_schedule(table)

def save_venue(name, street, city, state):
    scraperwiki.sqlite.save(unique_keys=[], data={
        "name":name,
        "slug": slugify_venue_name(name),
        "street":street,
        "city":city,
        "state":state}, table_name="venues")    

def clean_street(street):
    clean_street = street.strip()
    clean_street = clean_street.replace('Street', 'St')
    clean_street = clean_street.replace('Stree', 'St')
    clean_street = clean_street.replace('St.', 'St')
    clean_street = clean_street.replace('Avenue', 'Ave')
    clean_street = clean_street.replace('Southeast', 'SE')
    clean_street = clean_street.replace('South', 'S')
    clean_street = clean_street.replace('S.', 'S')
    clean_street = clean_street.replace('West', 'W')
    clean_street = clean_street.replace('W.', 'W')
    clean_street = clean_street.replace('North', 'N')
    return clean_street
    
def parse_venues(root):
    for venue_cell in root.cssselect('td.style4'):
        venue_name = None
        venue_street = None

        for child in venue_cell:
            if child.text is not None and child.text.strip() != "":
                venue_name = child.text
            
            if child.tail is not None and child.tail.strip() != "":
                venue_street = child.tail
            
            # Special case for "The Atlantic".  The venue address is 
            # wrapped in the <strong> tag along with the name
            if venue_street is None and len(child) > 0 and child[0].tail is not None:
                venue_street = child[0].tail
            
        save_venue(venue_name, clean_street(venue_street), "Gainesville", "FL")        

html = scraperwiki.scrape("http://thefestfl.com/fest10schedule.html")
root = lxml.html.fromstring(html)
scraperwiki.sqlite.execute("drop table if exists swdata")
scraperwiki.sqlite.execute("drop table if exists venues")
scraperwiki.sqlite.execute("drop table if exists sets")
parse_venues(root)
parse_schedules(root)