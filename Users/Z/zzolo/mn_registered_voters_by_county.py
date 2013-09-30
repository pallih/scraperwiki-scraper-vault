import scraperwiki           
import lxml.html
import dateutil.parser

# Reads number of registered voters in MN by County from this page:
# http://www.sos.state.mn.us/index.aspx?page=531 

data = scraperwiki.scrape('http://www.sos.state.mn.us/index.aspx?page=531')
html = lxml.html.fromstring(data)
count = 0

# Get date first
date_text = html.cssselect('#Title1_subTitle')[0].text
date_text = date_text.replace('As of ', '')
try:
  date = dateutil.parser.parse(date_text).date()
except ValueError:
  print 'Could not parse date.'
  
# In theory we should only update if new date

# Read table and insert rows
rows = html.cssselect('table.bodytext tr')
for row in rows:
  cells = row.cssselect('td')
  if cells[0].text != None:
    item = {
      'id': str(date) + '-' + cells[0].text,
      'date': date,
      'county': cells[0].text,
      'voters': int(cells[1].text.replace(',', ''))
    }
    
    scraperwiki.sqlite.save(unique_keys=['id'], data=item)import scraperwiki           
import lxml.html
import dateutil.parser

# Reads number of registered voters in MN by County from this page:
# http://www.sos.state.mn.us/index.aspx?page=531 

data = scraperwiki.scrape('http://www.sos.state.mn.us/index.aspx?page=531')
html = lxml.html.fromstring(data)
count = 0

# Get date first
date_text = html.cssselect('#Title1_subTitle')[0].text
date_text = date_text.replace('As of ', '')
try:
  date = dateutil.parser.parse(date_text).date()
except ValueError:
  print 'Could not parse date.'
  
# In theory we should only update if new date

# Read table and insert rows
rows = html.cssselect('table.bodytext tr')
for row in rows:
  cells = row.cssselect('td')
  if cells[0].text != None:
    item = {
      'id': str(date) + '-' + cells[0].text,
      'date': date,
      'county': cells[0].text,
      'voters': int(cells[1].text.replace(',', ''))
    }
    
    scraperwiki.sqlite.save(unique_keys=['id'], data=item)