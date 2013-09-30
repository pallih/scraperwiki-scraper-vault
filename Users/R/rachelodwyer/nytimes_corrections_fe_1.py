from datetime import datetime, timedelta
import dateutil.parser
import string, re, time
import requests
from lxml import html 
import scraperwiki

# http://www.nytimes.com/2012/05/02/pageoneplus/corrections-may-2.html
# %Y - 4 digit year
# %m - 2 digit month
# %d - 2 digit day
# %b - abbreviated form of day, i.e. May
URL = 'http://www.nytimes.com/%Y/%m/%d/pageoneplus/corrections-%b'
# Matches: 
# http://www.nytimes.com/2012/04/18/business/media/sony-plans-major-layoffs-of-emi-work-force.html
PATTERN = 'nytimes.com/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'

current_date = datetime.now()

while True:
    # Form URL from current date
    url = string.lower( current_date.strftime(URL) )
    url = url + '-%d.html' % current_date.day # -2.html
    
    # Get the response from the web request
    response = requests.get(url)

    # Parse HTML into searchable object
    doc = html.fromstring(response.text)
    
    # Selects all 'a' elements (links) in the article div
    for link in doc.cssselect('div#article a'):
        href = link.get('href')
        m = re.search(PATTERN, href) # Match the pattern to the link we've found
        # If there's a match, we've found a link to a corrected article
        if m:
            # Form a date object from what we extracted from the link
            date_str = "%s %s %s" % (m.group('year'), m.group('month'), m.group('day'))
            article_date = dateutil.parser.parse(date_str)
            # Save to the datastore
            scraperwiki.sqlite.save(unique_keys=[], data={"date" : article_date,
                                                          "url"  : href}) 
    # Set the date to the previous day
    current_date = current_date - timedelta(days=1)

    # Stop when we get to 2011
    if current_date.year <= 2011:
        break
    
    time.sleep(1)from datetime import datetime, timedelta
import dateutil.parser
import string, re, time
import requests
from lxml import html 
import scraperwiki

# http://www.nytimes.com/2012/05/02/pageoneplus/corrections-may-2.html
# %Y - 4 digit year
# %m - 2 digit month
# %d - 2 digit day
# %b - abbreviated form of day, i.e. May
URL = 'http://www.nytimes.com/%Y/%m/%d/pageoneplus/corrections-%b'
# Matches: 
# http://www.nytimes.com/2012/04/18/business/media/sony-plans-major-layoffs-of-emi-work-force.html
PATTERN = 'nytimes.com/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'

current_date = datetime.now()

while True:
    # Form URL from current date
    url = string.lower( current_date.strftime(URL) )
    url = url + '-%d.html' % current_date.day # -2.html
    
    # Get the response from the web request
    response = requests.get(url)

    # Parse HTML into searchable object
    doc = html.fromstring(response.text)
    
    # Selects all 'a' elements (links) in the article div
    for link in doc.cssselect('div#article a'):
        href = link.get('href')
        m = re.search(PATTERN, href) # Match the pattern to the link we've found
        # If there's a match, we've found a link to a corrected article
        if m:
            # Form a date object from what we extracted from the link
            date_str = "%s %s %s" % (m.group('year'), m.group('month'), m.group('day'))
            article_date = dateutil.parser.parse(date_str)
            # Save to the datastore
            scraperwiki.sqlite.save(unique_keys=[], data={"date" : article_date,
                                                          "url"  : href}) 
    # Set the date to the previous day
    current_date = current_date - timedelta(days=1)

    # Stop when we get to 2011
    if current_date.year <= 2011:
        break
    
    time.sleep(1)