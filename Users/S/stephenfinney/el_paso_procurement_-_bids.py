import scraperwiki
import dateutil.parser
from BeautifulSoup import BeautifulSoup

class BrokenElementException(Exception):
       def __init__(self, value):
           self.parameter = value
       def __str__(self):
           return repr(self.parameter)

def create_table():                                  # This method creates the data table with a proper schema.
    print "Creating table for data..."
    scraperwiki.sqlite.execute("drop table swdata")
    scraperwiki.sqlite.execute("create table swdata('Solicitation ID' str, 'Title' str, 'Type' str, 'Deposit' str, 'Issue Date' date, 'Due Date' date, 'Status' str, 'Department' str, 'Contact' str, 'Details Link' str, 'Amendments' str)")
    scraperwiki.sqlite.commit()

def record_data(cells, amendments, amendment_count): # This method stores the data
    for cell in cells:
        if cell.find('a',href=True):
            link = 'http://www.elpasotexas.gov/purchasing/' + cell.find('a',href=True)['href']
            details_html  = scraperwiki.scrape(link)
            details_root  = BeautifulSoup(details_html)
            details_table = details_root.find('table',{"border" : "0", "cellpadding" : "5", "style" : "border-collapse: collapse", "width" : "100%"})
            details_data  = details_table.findAll('td', {"valign" : "top", "colspan" : "2"})
    
            record = {}
            try:
                record['Solicitation ID'] =  details_data[0].text
                record['Title']           =  details_data[1].text[0] + (details_data[1].text)[1:].lower()
                record['Status']          =  details_data[2].text
                record['Department']      =  details_data[3].text
                record['Type']            =  details_data[4].text
                record['Deposit']         =  details_data[5].text
                record['Issue Date']      =  dateutil.parser.parse(details_data[6].text).date().strftime('%m/%d/%y')
                record['Due Date']        =  dateutil.parser.parse(details_data[7].text).date().strftime('%m/%d/%y')  
                record['Contact']         =  details_data[8].text
                record['Details Link']    =  link
                record['Amendments']      =  amendments[amendment_count].text
                amendment_count += 1
                scraperwiki.sqlite.save(unique_keys=['Solicitation ID'], data=record)
            except:
                broken = True
                broken_elements += "In record: " + record['Solicitation ID'] + ": " + record['Title'] + "\n"

        elif not "TITLE" in cell.text:
            broken = True
            broken_elements += "Details link: " + cell.text + "\n"


create_table()

print "Scraping HTML from website..."
html = scraperwiki.scrape('http://www.elpasotexas.gov/purchasing/ep-invitations.asp')
root = BeautifulSoup(html)
list_table = root.find('table',{"border" : "0", "cellpadding" : "0", "style" : "border-collapse: collapse", "width" : "100%"})

amendments = list_table.findAll('td',{"width" : "23%", "align" : "center", "valign" : "top"})
amendment_count = 0
broken = False
broken_elements = ""

print "Scraping solicitation details and getting data..."
cells = list_table.findAll('td',{"width" : "32%"})
record_data(cells, amendments, amendment_count)

cells = list_table.findAll('td',{"width" : "31%"})
record_data(cells, amendments, amendment_count)

if broken == True:
    print "Broken elements:\n" + broken_elements
    raise BrokenElementException("Broken elements were detected.")

print "Mission Accomplished"
import scraperwiki
import dateutil.parser
from BeautifulSoup import BeautifulSoup

class BrokenElementException(Exception):
       def __init__(self, value):
           self.parameter = value
       def __str__(self):
           return repr(self.parameter)

def create_table():                                  # This method creates the data table with a proper schema.
    print "Creating table for data..."
    scraperwiki.sqlite.execute("drop table swdata")
    scraperwiki.sqlite.execute("create table swdata('Solicitation ID' str, 'Title' str, 'Type' str, 'Deposit' str, 'Issue Date' date, 'Due Date' date, 'Status' str, 'Department' str, 'Contact' str, 'Details Link' str, 'Amendments' str)")
    scraperwiki.sqlite.commit()

def record_data(cells, amendments, amendment_count): # This method stores the data
    for cell in cells:
        if cell.find('a',href=True):
            link = 'http://www.elpasotexas.gov/purchasing/' + cell.find('a',href=True)['href']
            details_html  = scraperwiki.scrape(link)
            details_root  = BeautifulSoup(details_html)
            details_table = details_root.find('table',{"border" : "0", "cellpadding" : "5", "style" : "border-collapse: collapse", "width" : "100%"})
            details_data  = details_table.findAll('td', {"valign" : "top", "colspan" : "2"})
    
            record = {}
            try:
                record['Solicitation ID'] =  details_data[0].text
                record['Title']           =  details_data[1].text[0] + (details_data[1].text)[1:].lower()
                record['Status']          =  details_data[2].text
                record['Department']      =  details_data[3].text
                record['Type']            =  details_data[4].text
                record['Deposit']         =  details_data[5].text
                record['Issue Date']      =  dateutil.parser.parse(details_data[6].text).date().strftime('%m/%d/%y')
                record['Due Date']        =  dateutil.parser.parse(details_data[7].text).date().strftime('%m/%d/%y')  
                record['Contact']         =  details_data[8].text
                record['Details Link']    =  link
                record['Amendments']      =  amendments[amendment_count].text
                amendment_count += 1
                scraperwiki.sqlite.save(unique_keys=['Solicitation ID'], data=record)
            except:
                broken = True
                broken_elements += "In record: " + record['Solicitation ID'] + ": " + record['Title'] + "\n"

        elif not "TITLE" in cell.text:
            broken = True
            broken_elements += "Details link: " + cell.text + "\n"


create_table()

print "Scraping HTML from website..."
html = scraperwiki.scrape('http://www.elpasotexas.gov/purchasing/ep-invitations.asp')
root = BeautifulSoup(html)
list_table = root.find('table',{"border" : "0", "cellpadding" : "0", "style" : "border-collapse: collapse", "width" : "100%"})

amendments = list_table.findAll('td',{"width" : "23%", "align" : "center", "valign" : "top"})
amendment_count = 0
broken = False
broken_elements = ""

print "Scraping solicitation details and getting data..."
cells = list_table.findAll('td',{"width" : "32%"})
record_data(cells, amendments, amendment_count)

cells = list_table.findAll('td',{"width" : "31%"})
record_data(cells, amendments, amendment_count)

if broken == True:
    print "Broken elements:\n" + broken_elements
    raise BrokenElementException("Broken elements were detected.")

print "Mission Accomplished"
