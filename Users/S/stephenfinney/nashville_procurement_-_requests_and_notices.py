import scraperwiki
import dateutil.parser
import datetime
from BeautifulSoup import BeautifulSoup

class BrokenElementException(Exception):
       def __init__(self, value):
           self.parameter = value
       def __str__(self):
           return repr(self.parameter)

def create_table():                # This method creates the data table with a proper schema.
    print "Creating table for data..."
    scraperwiki.sqlite.execute("drop table swdata")
    scraperwiki.sqlite.execute("drop table swvariables")
    scraperwiki.sqlite.execute("create table swdata('ID' str, 'Service Description' str, 'Submit Date' date, 'Updated' str, 'Download Link' str)")
    scraperwiki.sqlite.execute("create table swvariables('name' str, 'value_blob' date)")
    scraperwiki.sqlite.commit()

create_table()
print "Scraping HTML from website..."

html = scraperwiki.scrape('http://www.tn.gov/generalserv/purchasing/ocr/rfp.shtml')
root = BeautifulSoup(html)
table = root.find('table',{"bordercolor" : "#719179"})
rows = table.findAll('tr')
broken = False
broken_elements = ""

print "Getting data..."

if root.find('span',{"class" : "style17"}):
    last_updated = root.find('span',{"class" : "style17"}).text
    last_updated = last_updated.strip('\t\n\r').replace('&nbsp;', '')
    last_updated = last_updated[46:-8]
    scraperwiki.sqlite.save_var( 'Website Last Modified',dateutil.parser.parse(last_updated).date().strftime('%m/%d/%y') )

for row in rows:
    record = {}
    cells = row.findAll('td')

    if cells:

        if cells[0].find('a',href=True):
            record['ID'] = cells[0].find('a').text
            try:
                if not "http://" in cells[0].find('a',href=True)['href']:
                    record['Download Link'] = "http://www.tn.gov/generalserv/purchasing/ocr/" + cells[0].find('a',href=True)['href']
                else: record['Download Link'] = cells[0].find('a',href=True)['href']
            except:
                broken = True
                broken_elements += "Download Link: " + cells[0].find('a',href=True) + "\n"
                

        else:
            record['ID'] = cells[0].text
            record['Download Link'] = "N/A"

        
        try:
            record['Submit Date'] = dateutil.parser.parse(cells[1].text).date().strftime('%m/%d/%y')
        except:
            broken = True
            broken_elements += "Submit Date: " + cells[1].text + "\n"
        
        if cells[1].find('img',src=True):
            record['Updated'] = "Yes"
        else: record['Updated'] = "No"

        record['Service Description'] = cells[2].text
        scraperwiki.sqlite.save(unique_keys=['ID'], data=record)

if broken == True:
    print "Broken elements: \n" + broken_elements
    raise BrokenElementException("Broken elements were detected.")

print "Mission Accomplished"
