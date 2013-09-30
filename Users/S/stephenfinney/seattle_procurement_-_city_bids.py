import scraperwiki
import dateutil.parser
import datetime
import feedparser
import requests
import re, htmlentitydefs
import sys
from BeautifulSoup import BeautifulSoup

class BrokenElementException(Exception):
       def __init__(self, value):
           self.parameter = value
       def __str__(self):
           return repr(self.parameter)

def create_table():
    print "Creating table for data..."
    scraperwiki.sqlite.execute("drop table swdata")
    scraperwiki.sqlite.execute("create table swdata('Bid ID' str, 'Bid Title' str, 'Status' str, 'Posted Date' datetime, 'Due Date' datetime, 'Contact' str, 'Download Link' str, 'Details Link' str)")
    scraperwiki.sqlite.commit()


def read_feed():
    print "Reading RSS feed..."
    rss_feed = feedparser.parse('http://thebuyline.seattle.gov/category/bids-and-proposals/feed/')

    print "Getting links to data..."
    tags = rss_feed.entries  
    urls = []
    for tag in tags:
        urls.append(tag.links[0].href)
    return urls


def record_data():
    broken = False
    broken_elements = ""
    urls = read_feed()
    headers_dict = {'user-agent': 'Mozilla/5.0'}
    
    print "Scraping HTML and getting data..."
    print "Scraping " + str(len(urls)) + " pages..."
    for url in urls:
        
        # Attempts to connect to the website
        try:
            html = requests.get(url, headers=headers_dict)
        except:
            print "***ERROR: Connection to website failed. Exiting program.***"
            sys.exit(1) 

        root = BeautifulSoup(html.text)
        content = root.find('div',{"id" : "content"})
        title = content.find('h2').text
        record = {}

        if title:
            # Test for invalid bid
            if "ALERT!" in title[:6]:
                continue          


            # Record Link
            record['Details Link'] = url


            # Find and record contact email, if possible
            if content.find('a',href=True):
                links = content.findAll('a',href=True)
                for link in links:
                    if "mailto:" in link['href']:
                        record['Contact'] = (link['href'])[7:].lower()
            

            # If no email found, print error
            if record['Contact'] == "":
                record['Contact'] = "N/A"


            # Record status of bid
            statuses = {"CLOSED", "ARCHIVED", "CANCELED", "CANCELLED"}
            for status in statuses:
                if status in title:
                    record['Status'] = status.capitalize()

                    if (status + "-") in title:
                        title = title.replace( (status + "-"), "" )
                    else: 
                        title = title.replace( status, "" )
                elif status == "CANCELLED":
                    record['Status'] = "Open"


            # Record bid ID
            record['Bid ID'] = content.findAll('a')[1].text


            # Record bid title
            title  = title.replace(record['Bid ID'], "")
            record['Bid Title'] = unescape(title)
        else: 
            broken = True
            broken_elements += "Title at url: " + url + "\n"


        # This code block finds and parses the content
        # for the posted date of the bid
        content = unescape(content.text)
        colons = [m.start() for m in re.finditer(':', content)]
        date_start = content.find("Posted:") + 7
        date_end = 0

        for colon in colons:
            if colon > date_start:
                date_end = colon + 6
                break

        # Record the posted date of the bid
        date = content[date_start:date_end]

        try:
            record['Posted Date'] = dateutil.parser.parse(date).strftime('%m/%d/%y %I:%M%p')
        except:
            broken = True
            broken_elements += "Posted Date on record: " + record['Bid ID'] + ". Date: " + date
            
        

        # Find and record the download link for the bid
        content = root.find('div',{"class" : "contenttext"})
        if content.find('a',href=True):
            record['Download Link'] = content.find('a',href=True)['href']
        else: record['Download Link'] = "N/A"


        # This code block finds and parses the content
        # for the due date of the bid
        date_header_text = ""

        if record['Bid ID'] == "RFP-12132":
            try:
                p_tags = content.findAll('p')
                date_header_text = p_tags[3].text
                date = date_header_text[date_header_text.find(':'):]
                date = cleanDate(date)
                record['Due Date'] = dateutil.parser.parse(date).strftime('%m/%d/%y %I:%M%p')

                if record['Status'] == "Open" and dateutil.parser.parse(date) < datetime.datetime.now():
                    record['Status'] = "Overdue"

                scraperwiki.sqlite.save(unique_keys=['Bid ID'], data=record)
                continue
            except:
                broken = True
                broken_elements += "Due Date on record: " + record['Bid ID'] + ". Date: " + date + "\n"

        elif record['Bid ID'] == "RFI":
            record['Due Date'] = dateutil.parser.parse("November 15, 2012 11:59PM").strftime('%m/%d/%y %I:%M%p')
            if record['Status'] == "Open" and dateutil.parser.parse(record['Due Date']) < datetime.datetime.now():
                    record['Status'] = "Overdue"
            scraperwiki.sqlite.save(unique_keys=['Bid ID'], data=record)
            continue
        else:
            try:
                p_tags = content.findAll('p')
                date_header_text = p_tags[3].text
                date = date_header_text[date_header_text.find(':'):]
                date = cleanDate(date)
                record['Due Date'] = dateutil.parser.parse(date).strftime('%m/%d/%y %I:%M%p')

                if record['Status'] == "Open" and dateutil.parser.parse(date) < datetime.datetime.now():
                    record['Status'] = "Overdue"

                scraperwiki.sqlite.save(unique_keys=['Bid ID'], data=record)
                continue
            except:
                broken = True
                broken_elements += "Due Date on record: " + record['Bid ID'] + ". Date: " + date + "\n"

        strongs = content.findAll('strong')
        for strong in strongs:
            if "Date" in strong.text or "Date/Time" in strong.text:
                date_header_text = unescape(strong.text)
                break

        content = unescape(content.text)
        date_start = content.find(date_header_text) + (len(date_header_text))
        colons = [m.start() for m in re.finditer(':', content)]

        for colon in colons:
            if colon > date_start:
                date_end = colon + 5
                break

        # Record the due date of the bid, if possible
        date = cleanDate(content[date_start:date_end])
        #print "Date for " + record['Bid ID'] + ": " + date
        try:
            record['Due Date'] = dateutil.parser.parse(date).strftime('%m/%d/%y %I:%M%p')
            print "Date for " + record['Bid ID'] + ": " + record['Due Date']

            if record['Status'] == "Open" and dateutil.parser.parse(date) < datetime.datetime.now():
                record['Status'] = "Overdue"
        except:
            broken = True
            broken_elements += "Due Date on record: " + record['Bid ID'] + ". Date: " + date + "\n"

        # Save all information
        scraperwiki.sqlite.save(unique_keys=['Bid ID'], data=record)

    if broken == True:
        print "Broken elements:\n" + broken_elements
        raise BrokenElementException("Broken elements were detected.")


##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)


def cleanDate(date):
    if "Proposal-12-22.pdf" in date:     #HOTFIX HERE
        date = "08/21/12 2:01 pm"
        return date

    if "Addendum Q &A" in date:          #HOTFIX HERE
        date = "07/20/12 4:00 pm"
        return date

    date = unescape(date)

    if date[0] == ":":
        date = date.replace(":", "", 1)

    date = date.replace(" at", "")
    date = date.replace(",", "")
    date = date.replace(u'\xa0', u' ')
    date = date.strip('\t\n\r')

    if date.find("/") - 2 == -1:
        date = "0" + date

    if date[date.find(":") + 3] == " ":
        date += "m"
    else: date = date[:date.find(":") + 3] + " " + date[date.find(":") + 3:]

    date = date.lower()
    return str(date)    


create_table()
record_data()
print "Mission Accomplished"
import scraperwiki
import dateutil.parser
import datetime
import feedparser
import requests
import re, htmlentitydefs
import sys
from BeautifulSoup import BeautifulSoup

class BrokenElementException(Exception):
       def __init__(self, value):
           self.parameter = value
       def __str__(self):
           return repr(self.parameter)

def create_table():
    print "Creating table for data..."
    scraperwiki.sqlite.execute("drop table swdata")
    scraperwiki.sqlite.execute("create table swdata('Bid ID' str, 'Bid Title' str, 'Status' str, 'Posted Date' datetime, 'Due Date' datetime, 'Contact' str, 'Download Link' str, 'Details Link' str)")
    scraperwiki.sqlite.commit()


def read_feed():
    print "Reading RSS feed..."
    rss_feed = feedparser.parse('http://thebuyline.seattle.gov/category/bids-and-proposals/feed/')

    print "Getting links to data..."
    tags = rss_feed.entries  
    urls = []
    for tag in tags:
        urls.append(tag.links[0].href)
    return urls


def record_data():
    broken = False
    broken_elements = ""
    urls = read_feed()
    headers_dict = {'user-agent': 'Mozilla/5.0'}
    
    print "Scraping HTML and getting data..."
    print "Scraping " + str(len(urls)) + " pages..."
    for url in urls:
        
        # Attempts to connect to the website
        try:
            html = requests.get(url, headers=headers_dict)
        except:
            print "***ERROR: Connection to website failed. Exiting program.***"
            sys.exit(1) 

        root = BeautifulSoup(html.text)
        content = root.find('div',{"id" : "content"})
        title = content.find('h2').text
        record = {}

        if title:
            # Test for invalid bid
            if "ALERT!" in title[:6]:
                continue          


            # Record Link
            record['Details Link'] = url


            # Find and record contact email, if possible
            if content.find('a',href=True):
                links = content.findAll('a',href=True)
                for link in links:
                    if "mailto:" in link['href']:
                        record['Contact'] = (link['href'])[7:].lower()
            

            # If no email found, print error
            if record['Contact'] == "":
                record['Contact'] = "N/A"


            # Record status of bid
            statuses = {"CLOSED", "ARCHIVED", "CANCELED", "CANCELLED"}
            for status in statuses:
                if status in title:
                    record['Status'] = status.capitalize()

                    if (status + "-") in title:
                        title = title.replace( (status + "-"), "" )
                    else: 
                        title = title.replace( status, "" )
                elif status == "CANCELLED":
                    record['Status'] = "Open"


            # Record bid ID
            record['Bid ID'] = content.findAll('a')[1].text


            # Record bid title
            title  = title.replace(record['Bid ID'], "")
            record['Bid Title'] = unescape(title)
        else: 
            broken = True
            broken_elements += "Title at url: " + url + "\n"


        # This code block finds and parses the content
        # for the posted date of the bid
        content = unescape(content.text)
        colons = [m.start() for m in re.finditer(':', content)]
        date_start = content.find("Posted:") + 7
        date_end = 0

        for colon in colons:
            if colon > date_start:
                date_end = colon + 6
                break

        # Record the posted date of the bid
        date = content[date_start:date_end]

        try:
            record['Posted Date'] = dateutil.parser.parse(date).strftime('%m/%d/%y %I:%M%p')
        except:
            broken = True
            broken_elements += "Posted Date on record: " + record['Bid ID'] + ". Date: " + date
            
        

        # Find and record the download link for the bid
        content = root.find('div',{"class" : "contenttext"})
        if content.find('a',href=True):
            record['Download Link'] = content.find('a',href=True)['href']
        else: record['Download Link'] = "N/A"


        # This code block finds and parses the content
        # for the due date of the bid
        date_header_text = ""

        if record['Bid ID'] == "RFP-12132":
            try:
                p_tags = content.findAll('p')
                date_header_text = p_tags[3].text
                date = date_header_text[date_header_text.find(':'):]
                date = cleanDate(date)
                record['Due Date'] = dateutil.parser.parse(date).strftime('%m/%d/%y %I:%M%p')

                if record['Status'] == "Open" and dateutil.parser.parse(date) < datetime.datetime.now():
                    record['Status'] = "Overdue"

                scraperwiki.sqlite.save(unique_keys=['Bid ID'], data=record)
                continue
            except:
                broken = True
                broken_elements += "Due Date on record: " + record['Bid ID'] + ". Date: " + date + "\n"

        elif record['Bid ID'] == "RFI":
            record['Due Date'] = dateutil.parser.parse("November 15, 2012 11:59PM").strftime('%m/%d/%y %I:%M%p')
            if record['Status'] == "Open" and dateutil.parser.parse(record['Due Date']) < datetime.datetime.now():
                    record['Status'] = "Overdue"
            scraperwiki.sqlite.save(unique_keys=['Bid ID'], data=record)
            continue
        else:
            try:
                p_tags = content.findAll('p')
                date_header_text = p_tags[3].text
                date = date_header_text[date_header_text.find(':'):]
                date = cleanDate(date)
                record['Due Date'] = dateutil.parser.parse(date).strftime('%m/%d/%y %I:%M%p')

                if record['Status'] == "Open" and dateutil.parser.parse(date) < datetime.datetime.now():
                    record['Status'] = "Overdue"

                scraperwiki.sqlite.save(unique_keys=['Bid ID'], data=record)
                continue
            except:
                broken = True
                broken_elements += "Due Date on record: " + record['Bid ID'] + ". Date: " + date + "\n"

        strongs = content.findAll('strong')
        for strong in strongs:
            if "Date" in strong.text or "Date/Time" in strong.text:
                date_header_text = unescape(strong.text)
                break

        content = unescape(content.text)
        date_start = content.find(date_header_text) + (len(date_header_text))
        colons = [m.start() for m in re.finditer(':', content)]

        for colon in colons:
            if colon > date_start:
                date_end = colon + 5
                break

        # Record the due date of the bid, if possible
        date = cleanDate(content[date_start:date_end])
        #print "Date for " + record['Bid ID'] + ": " + date
        try:
            record['Due Date'] = dateutil.parser.parse(date).strftime('%m/%d/%y %I:%M%p')
            print "Date for " + record['Bid ID'] + ": " + record['Due Date']

            if record['Status'] == "Open" and dateutil.parser.parse(date) < datetime.datetime.now():
                record['Status'] = "Overdue"
        except:
            broken = True
            broken_elements += "Due Date on record: " + record['Bid ID'] + ". Date: " + date + "\n"

        # Save all information
        scraperwiki.sqlite.save(unique_keys=['Bid ID'], data=record)

    if broken == True:
        print "Broken elements:\n" + broken_elements
        raise BrokenElementException("Broken elements were detected.")


##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)


def cleanDate(date):
    if "Proposal-12-22.pdf" in date:     #HOTFIX HERE
        date = "08/21/12 2:01 pm"
        return date

    if "Addendum Q &A" in date:          #HOTFIX HERE
        date = "07/20/12 4:00 pm"
        return date

    date = unescape(date)

    if date[0] == ":":
        date = date.replace(":", "", 1)

    date = date.replace(" at", "")
    date = date.replace(",", "")
    date = date.replace(u'\xa0', u' ')
    date = date.strip('\t\n\r')

    if date.find("/") - 2 == -1:
        date = "0" + date

    if date[date.find(":") + 3] == " ":
        date += "m"
    else: date = date[:date.find(":") + 3] + " " + date[date.find(":") + 3:]

    date = date.lower()
    return str(date)    


create_table()
record_data()
print "Mission Accomplished"
