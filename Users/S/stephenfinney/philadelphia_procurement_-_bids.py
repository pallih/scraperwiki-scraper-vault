import scraperwiki
import dateutil.parser
import requests
import sys
from BeautifulSoup import BeautifulSoup


def create_tables():              # This method creates the tables needed with their proper schemas.
    print "Creating table for data..."
    scraperwiki.sqlite.execute("drop table swdata")
    scraperwiki.sqlite.execute("drop table swvariables")
    scraperwiki.sqlite.execute("create table swdata('Title' str, 'Bid Number' str, 'Prequalify Date' date, 'Open Date' date, 'Download Link' str, 'Addendums' str, 'Addendum Link' str)")
    scraperwiki.sqlite.execute("create table swvariables('name' str, 'value_blob' date)")
    scraperwiki.sqlite.commit()

def clean(text):                  # This method removes the space code from strings
    if text.endswith("&nbsp;"):
        text = text[:-6]
    return text.strip('\t\n\r')


create_tables()  

# Attempts to connect to the website
try:
    #headers_dict = {'user-agent': 'Mozilla/5.0'}
    headers_dict = {'user-agent': ''}
    #headers_dict = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.1) Gecko/20061204 Firefox/2.0.0.1'}
    #headers_dict = {'user-agent': 'Python-urllib/2.1'}
    print "Attempting connection..."
    html = requests.get('http://mbec.phila.gov/procurement/', headers=headers_dict)# Scrape the html from the website

except:
    print "***ERROR: Connection to website failed. Exiting program.***"
    sys.exit(1) 
#html = scraperwiki.scrape('http://mbec.phila.gov/procurement/') 
print html.text
root = BeautifulSoup(html.text)                                 # Parse the html into something BeautifulSoup can read
table = root.find('table',{"border" : "1", "width" : "99%"})    # Find the desired table. It has a border of 1 and width of 99%
rows = table.findAll('tr')                                      # Find all 'tr' tags in the table
first_row = True                                                # Set the boolean 'first_row' variable to True

print "Connection Established"
print "Getting data..."

# This saves the last date the website was modified.
scraperwiki.sqlite.save_var('Website Last Modified',dateutil.parser.parse( root.find('center').text[14:] ).date().strftime("%m/%d/%y"))


for row in rows:                                                # Loop each row in 'rows'

    if first_row:                                               # This 'if' statement ensures that the table header is not included
        first_row = False                                       # Make the value false
        continue                                                # and jump to next iteration in 'for' loop

    record = {}                                                 # Create an empty array for the record
    cells = row.findAll('td')                                   # Find all 'td' tags in the row

    # If the row contains any 'td' tags...
    # Then, if the cell has any alphanumeric characters,
    # store the cell text as the prequalify date
    # Else, store "N/A"
    if cells:                                                     
        if cells[0].text.isalnum():                                
            record['Prequalify Date'] = dateutil.parser.parse( clean(cells[0].text) ).date().strftime("%m/%d/%y")
        else: record['Prequalify Date'] = "N/A"

        # Record Open Date and ID, respectively
        record['Open Date'] = dateutil.parser.parse( clean(cells[1].text) ).date().strftime("%m/%d/%y")
        record['Bid Number'] = clean(cells[2].text)

        # The code below constructs the correct URL for the download link.
        # Records "N/A" if no link provided on site.
        if cells[2].find('a',href=True):                   
            record['Download Link'] = clean("http://mbec.phila.gov/procurement" + cells[2].find('a',href=True)['href'][6:])
        else: record['Download Link'] = "N/A"

        record['Title'] = clean(cells[3].text)                  # Record the title
        record['Addendums'] = clean(cells[4].text)              # Record number of addendums

        # The code below constructs the correct URL for the addendum download link.
        # Records "N/A" if no link provided on site.
        if cells[4].find('a',href=True):
            record['Addendum Link'] = clean("http://mbec.phila.gov/procurement" + cells[4].find('a',href=True)['href'][6:])
        else: record['Addendum Link'] = "N/A"

        scraperwiki.sqlite.save(unique_keys=['Bid Number'], data=record)# Save all data 

print "Mission Accomplished"
import scraperwiki
import dateutil.parser
import requests
import sys
from BeautifulSoup import BeautifulSoup


def create_tables():              # This method creates the tables needed with their proper schemas.
    print "Creating table for data..."
    scraperwiki.sqlite.execute("drop table swdata")
    scraperwiki.sqlite.execute("drop table swvariables")
    scraperwiki.sqlite.execute("create table swdata('Title' str, 'Bid Number' str, 'Prequalify Date' date, 'Open Date' date, 'Download Link' str, 'Addendums' str, 'Addendum Link' str)")
    scraperwiki.sqlite.execute("create table swvariables('name' str, 'value_blob' date)")
    scraperwiki.sqlite.commit()

def clean(text):                  # This method removes the space code from strings
    if text.endswith("&nbsp;"):
        text = text[:-6]
    return text.strip('\t\n\r')


create_tables()  

# Attempts to connect to the website
try:
    #headers_dict = {'user-agent': 'Mozilla/5.0'}
    headers_dict = {'user-agent': ''}
    #headers_dict = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.1) Gecko/20061204 Firefox/2.0.0.1'}
    #headers_dict = {'user-agent': 'Python-urllib/2.1'}
    print "Attempting connection..."
    html = requests.get('http://mbec.phila.gov/procurement/', headers=headers_dict)# Scrape the html from the website

except:
    print "***ERROR: Connection to website failed. Exiting program.***"
    sys.exit(1) 
#html = scraperwiki.scrape('http://mbec.phila.gov/procurement/') 
print html.text
root = BeautifulSoup(html.text)                                 # Parse the html into something BeautifulSoup can read
table = root.find('table',{"border" : "1", "width" : "99%"})    # Find the desired table. It has a border of 1 and width of 99%
rows = table.findAll('tr')                                      # Find all 'tr' tags in the table
first_row = True                                                # Set the boolean 'first_row' variable to True

print "Connection Established"
print "Getting data..."

# This saves the last date the website was modified.
scraperwiki.sqlite.save_var('Website Last Modified',dateutil.parser.parse( root.find('center').text[14:] ).date().strftime("%m/%d/%y"))


for row in rows:                                                # Loop each row in 'rows'

    if first_row:                                               # This 'if' statement ensures that the table header is not included
        first_row = False                                       # Make the value false
        continue                                                # and jump to next iteration in 'for' loop

    record = {}                                                 # Create an empty array for the record
    cells = row.findAll('td')                                   # Find all 'td' tags in the row

    # If the row contains any 'td' tags...
    # Then, if the cell has any alphanumeric characters,
    # store the cell text as the prequalify date
    # Else, store "N/A"
    if cells:                                                     
        if cells[0].text.isalnum():                                
            record['Prequalify Date'] = dateutil.parser.parse( clean(cells[0].text) ).date().strftime("%m/%d/%y")
        else: record['Prequalify Date'] = "N/A"

        # Record Open Date and ID, respectively
        record['Open Date'] = dateutil.parser.parse( clean(cells[1].text) ).date().strftime("%m/%d/%y")
        record['Bid Number'] = clean(cells[2].text)

        # The code below constructs the correct URL for the download link.
        # Records "N/A" if no link provided on site.
        if cells[2].find('a',href=True):                   
            record['Download Link'] = clean("http://mbec.phila.gov/procurement" + cells[2].find('a',href=True)['href'][6:])
        else: record['Download Link'] = "N/A"

        record['Title'] = clean(cells[3].text)                  # Record the title
        record['Addendums'] = clean(cells[4].text)              # Record number of addendums

        # The code below constructs the correct URL for the addendum download link.
        # Records "N/A" if no link provided on site.
        if cells[4].find('a',href=True):
            record['Addendum Link'] = clean("http://mbec.phila.gov/procurement" + cells[4].find('a',href=True)['href'][6:])
        else: record['Addendum Link'] = "N/A"

        scraperwiki.sqlite.save(unique_keys=['Bid Number'], data=record)# Save all data 

print "Mission Accomplished"
