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
    scraperwiki.sqlite.execute("create table swdata('Posting Number' str, 'Project Name' str, 'Project Type' str, 'Due Date' datetime, 'Status' str, 'Planholders List' str, 'Description Link' str, 'Download Link' str, 'Contact' str)")
    scraperwiki.sqlite.commit()


create_table()

print "Scraping HTML from website..."
html = scraperwiki.scrape('http://www.springsgov.com/RFP.aspx')
root = BeautifulSoup(html)
tables = root.findAll('table',{"bgcolor" : "#ECECEC"})
broken = False
broken_elements = ""

print "Getting data..."
for table in tables:
    record = {}
    data = table.findAll('td')

    record['Posting Number'] = data[1].text
    record['Project Name'] = data[3].text[0] + (data[3].text)[1:].lower()
    record['Project Type'] = data[5].text

    try:
        record['Due Date'] = dateutil.parser.parse(data[7].text + " " + data[9].text).strftime('%m/%d/%y %I:%M%p')
    except:
        broken = True
        broken_elements += "Due Date: " + data[7].text + " " + data[9].text + "\n"

    record['Status'] = data[11].text

    if data[13].find('a',href=True):
        record['Planholders List'] = "http://www.springsgov.com/" + (data[13].find('a',href=True)['href']).replace(' ', '%20')
    else: record['Planholders List'] = "N/A"

    if data[15].find('a',href=True):
        record['Description Link'] = (data[15].find('a',href=True)['href']).replace(' ', '%20')
    else: record['Description Link'] = "N/A"

    try:
        if data[19].find('a',href=True):
            record['Download Link'] = "http://www.springsgov.com/" + (data[17].find('a',href=True)['href']).replace(' ', '%20')
        else: record['Download Link'] = "N/A"
    except:
        record['Download Link'] = "N/A"

    if data[len(data)-1].find('a',href=True):
        record['Contact'] = (data[len(data)-1].find('a',href=True)['href'])[7:].lower()
    else:
        name = data[len(data)-1].text
        if not name:
            record['Contact'] = "N/A"
            break
        name.capitalize()
        if "." in name:
            name[name.find(".")-1].upper()
            name[name.find(".")+2].upper()
        else: name[name.find(" ")+1].upper()
        record['Contact'] = name
    scraperwiki.sqlite.save(unique_keys=['Posting Number'], data=record)

if broken == True:
    print "Broken elements:\n" + broken_elements
    raise BrokenElementException("Broken elements were detected.")

print "Mission Accomplished"
