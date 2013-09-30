###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
import re
import lxml.html                    # To parse HTML
from lxml.html.clean import Cleaner # To get rid of unneeded HTML tags
import time
html = scraperwiki.scrape('http://www.raptureready.com/rap2.html')
print "Click on the ...more link to see the whole page"

# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <td> tags.
# -- UNCOMMENT THE 6 LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Console' tab again, and you'll see how we're extracting 
# the HTML that was inside <td></td> tags.
# We use lxml, which is a Python library especially for parsing html.
# -----------------------------------------------------------------------------

html = html.replace('<br>', ' ')
html = re.sub(r'(\&.*?;)|(\n|\t|\r)',' ',html)
print html
issues = []
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
cleaner = Cleaner(remove_tags=['font','span'], links=False, remove_unknown_tags=False)
root = cleaner.clean_html(root)
newhtml = lxml.html.tostring(root)

record = {}
datestring = re.findall("Updated (.*?)</p>",newhtml)[0]
date = time.strptime(datestring, '%b %d, %Y')                 # encode the date as a date using format Month dd, YYYY
date = time.strftime('%Y-%m-%d', date)                        # decode that date back into a string of format YYYY-mm-dd

if scraperwiki.sqlite.get_var('last_update') == None or scraperwiki.sqlite.get_var('last_update') != date:
    record["Date"] = date

    lis = root.cssselect('li') # get all the <li> tags
    for li in lis:
        li.text = re.sub(r'(\w+) \((\w+)\)',r'\1 - \2',li.text)
        li.text = li.text.replace('/',' and ')
        issues.append(li.text.strip())                # just the text inside the HTML tag
    
    scorestring = ''
    tds = root.cssselect('td')
    for td in tds:
        if td.text and re.match('\d[^\d]', td.text.strip()):
            scorestring = scorestring + ' ' + td.text.strip()
    scores = re.sub('(\+|-)\d','',scorestring).split()
    scores = [int(x) for x in scores]
    print scores
    
    record = dict(zip(issues,scores))
    print record
    total = 0
    for issue,score in record.items():
        total = total + score
    #print len(scores)
    #print len(issues)
    record["Total"] = total
    print record
    datestring = re.findall("Updated (.*?)</p>",newhtml)[0]
    date = time.strptime(datestring, '%b %d, %Y')                 # encode the date as a date using format Month dd, YYYY
    date = time.strftime('%Y-%m-%d', date)                        # decode that date back into a string of format YYYY-mm-dd
    print date
    record["Date"] = date
    
    scraperwiki.sqlite.save(["Date"], record) # save the records one by one
    scraperwiki.sqlite.save_var('last_update', date)
###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
import re
import lxml.html                    # To parse HTML
from lxml.html.clean import Cleaner # To get rid of unneeded HTML tags
import time
html = scraperwiki.scrape('http://www.raptureready.com/rap2.html')
print "Click on the ...more link to see the whole page"

# -----------------------------------------------------------------------------
# 1. Parse the raw HTML to get the interesting bits - the part inside <td> tags.
# -- UNCOMMENT THE 6 LINES BELOW (i.e. delete the # at the start of the lines)
# -- CLICK THE 'RUN' BUTTON BELOW
# Check the 'Console' tab again, and you'll see how we're extracting 
# the HTML that was inside <td></td> tags.
# We use lxml, which is a Python library especially for parsing html.
# -----------------------------------------------------------------------------

html = html.replace('<br>', ' ')
html = re.sub(r'(\&.*?;)|(\n|\t|\r)',' ',html)
print html
issues = []
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
cleaner = Cleaner(remove_tags=['font','span'], links=False, remove_unknown_tags=False)
root = cleaner.clean_html(root)
newhtml = lxml.html.tostring(root)

record = {}
datestring = re.findall("Updated (.*?)</p>",newhtml)[0]
date = time.strptime(datestring, '%b %d, %Y')                 # encode the date as a date using format Month dd, YYYY
date = time.strftime('%Y-%m-%d', date)                        # decode that date back into a string of format YYYY-mm-dd

if scraperwiki.sqlite.get_var('last_update') == None or scraperwiki.sqlite.get_var('last_update') != date:
    record["Date"] = date

    lis = root.cssselect('li') # get all the <li> tags
    for li in lis:
        li.text = re.sub(r'(\w+) \((\w+)\)',r'\1 - \2',li.text)
        li.text = li.text.replace('/',' and ')
        issues.append(li.text.strip())                # just the text inside the HTML tag
    
    scorestring = ''
    tds = root.cssselect('td')
    for td in tds:
        if td.text and re.match('\d[^\d]', td.text.strip()):
            scorestring = scorestring + ' ' + td.text.strip()
    scores = re.sub('(\+|-)\d','',scorestring).split()
    scores = [int(x) for x in scores]
    print scores
    
    record = dict(zip(issues,scores))
    print record
    total = 0
    for issue,score in record.items():
        total = total + score
    #print len(scores)
    #print len(issues)
    record["Total"] = total
    print record
    datestring = re.findall("Updated (.*?)</p>",newhtml)[0]
    date = time.strptime(datestring, '%b %d, %Y')                 # encode the date as a date using format Month dd, YYYY
    date = time.strftime('%Y-%m-%d', date)                        # decode that date back into a string of format YYYY-mm-dd
    print date
    record["Date"] = date
    
    scraperwiki.sqlite.save(["Date"], record) # save the records one by one
    scraperwiki.sqlite.save_var('last_update', date)
