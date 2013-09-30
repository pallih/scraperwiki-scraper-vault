###############################################################################
# Basic scraper
###############################################################################

import sys, logging, mechanize, unicodedata
import scraperwiki
from BeautifulSoup import BeautifulSoup


# This function strips any unicode or other such stuff from text being dumped to the console.
def unicode_strip(str):
    return "".join([c for c in str if ord(c) < 128])

# Function for extracting the data from the table
def extractTableData(year_value, fund_value):
    header_rows = soup.findAll(attrs={"class":"datahdr"})
    
    # Grab the text, strip out whitespace and newline characters
    row_titles = [row.contents[0].strip('\r\n\t ') for row in header_rows]
    
    print "Row Titles: %s" % row_titles
    
    # Grab data rows from all tables, because there may be more than one
    data_rows = []
    data_table = ''

    for header_row in header_rows:
        
        if (data_table != header_row.parent.parent):
            data_table = header_row.parent.parent
    
            # Grab every row bar the first one (the headers) and assume it's data
            data_rows.extend(data_table.findAll("tr")[1:])
    
    print "Found %d rows" % len(data_rows)
    
    # The main body. row_index and cell_index calculations are just for presentation.
    for row in data_rows:
        row_index = data_rows.index(row)
        print "Row %d: %d total cells" % (row_index + 1, len(row.findAll("td")))
        try:
            # Get all table cells (<td>'s)
            cells = [cell for cell in row.findAll("td")]
        except IndexError:
            print console_strip(row.renderContents())
            # This gets triggered if the row is empty.
            continue
        
        print "Found %d cells in row" % len(cells)
        # Iterate through the cells and assign them to an array.

        for counter, cell in enumerate(cells):
            # This strips out whitespace, and leading and trailing carriage control
            # characters
            cells[counter] = cell.p.renderContents().strip('\r\n\t ')

        print cells

        # Generate the dictionary to save to scraperwiki
        record = {
                    "Index" : row_index, \
                    "Year" : year_value, \
                    "Fund" : fund_value, \
                    "Recipient" : unicode_strip(cells[0]), \
                    "Description" : unicode_strip(cells[1]), \
                    "Work Area" : unicode_strip(cells[2]), \
                    "Location" : unicode_strip(cells[3]), \
                    "Amount Awarded" : unicode_strip(cells[4])
                 }

        print record

        scraperwiki.datastore.save(["Index", "Year", "Fund"], record) 
    
    return


# Retrieve page
url = 'http://www.artscouncil.ie/en/we_funded.aspx'
br = mechanize.Browser()
response = br.open(url)
soup = BeautifulSoup(response.read())

# Get fund values
select = soup.find('select', { 'name' : 'ComponentPlaceHolder1:_ctl0:ddlFunds' })
options = select.findAll('option')

funds = {}
for option in options:
    if (len(option['value'])):
        funds[option['value']] = option.contents;

print funds;

# Get year values
select = soup.find('select', { 'name' : 'ComponentPlaceHolder1:_ctl0:ddlYear' })
options = select.findAll('option')

years = {}
for (counter, option) in enumerate(options):
    if (len(option['value'])):
        years[counter] = option.contents;

# Iterate over the two
for fund_key, fund_value in funds.iteritems() :
    fund_value = fund_value[0].encode('ascii', 'ignore') # ASCII conversion

    for year_key, year_value in years.iteritems() :
        year_value = year_value[0].encode('ascii', 'ignore') # ASCII conversion
        
        # Submit the form with relevant fund and year value
        br.select_form(name='Form1')
        br["ComponentPlaceHolder1:_ctl0:ddlFunds"] = [fund_key]
        br["ComponentPlaceHolder1:_ctl0:ddlYear"] = [year_value]

        # Uncomment these for HTTP request/response logging
        #logger = logging.getLogger("mechanize")
        #logger.addHandler(logging.StreamHandler(sys.stdout))
        #logger.setLevel(logging.DEBUG)        
        #br.set_debug_http(False)
        #br.set_debug_responses(False)

        # There are two submit buttons, so we will use the second one
        req = br.click(type="submit", nr=1)
        br.open(req)

        # Read the response from the submitted form
        response = br.response().read()
        print response
        soup = BeautifulSoup(response)

        print year_value + ", " + fund_value + ", ",

        print len(funds)

        if "Amount Awarded" in response:
            print "Got it!";

            extractTableData(year_value, fund_value)

            # Go back to the original URL for the next iteration
            response = br.open(url)
            soup = BeautifulSoup(response.read())
        elif "There were no decisions" in response:
            print "No results..."
        else:
            print "Unknown error"
###############################################################################
# Basic scraper
###############################################################################

import sys, logging, mechanize, unicodedata
import scraperwiki
from BeautifulSoup import BeautifulSoup


# This function strips any unicode or other such stuff from text being dumped to the console.
def unicode_strip(str):
    return "".join([c for c in str if ord(c) < 128])

# Function for extracting the data from the table
def extractTableData(year_value, fund_value):
    header_rows = soup.findAll(attrs={"class":"datahdr"})
    
    # Grab the text, strip out whitespace and newline characters
    row_titles = [row.contents[0].strip('\r\n\t ') for row in header_rows]
    
    print "Row Titles: %s" % row_titles
    
    # Grab data rows from all tables, because there may be more than one
    data_rows = []
    data_table = ''

    for header_row in header_rows:
        
        if (data_table != header_row.parent.parent):
            data_table = header_row.parent.parent
    
            # Grab every row bar the first one (the headers) and assume it's data
            data_rows.extend(data_table.findAll("tr")[1:])
    
    print "Found %d rows" % len(data_rows)
    
    # The main body. row_index and cell_index calculations are just for presentation.
    for row in data_rows:
        row_index = data_rows.index(row)
        print "Row %d: %d total cells" % (row_index + 1, len(row.findAll("td")))
        try:
            # Get all table cells (<td>'s)
            cells = [cell for cell in row.findAll("td")]
        except IndexError:
            print console_strip(row.renderContents())
            # This gets triggered if the row is empty.
            continue
        
        print "Found %d cells in row" % len(cells)
        # Iterate through the cells and assign them to an array.

        for counter, cell in enumerate(cells):
            # This strips out whitespace, and leading and trailing carriage control
            # characters
            cells[counter] = cell.p.renderContents().strip('\r\n\t ')

        print cells

        # Generate the dictionary to save to scraperwiki
        record = {
                    "Index" : row_index, \
                    "Year" : year_value, \
                    "Fund" : fund_value, \
                    "Recipient" : unicode_strip(cells[0]), \
                    "Description" : unicode_strip(cells[1]), \
                    "Work Area" : unicode_strip(cells[2]), \
                    "Location" : unicode_strip(cells[3]), \
                    "Amount Awarded" : unicode_strip(cells[4])
                 }

        print record

        scraperwiki.datastore.save(["Index", "Year", "Fund"], record) 
    
    return


# Retrieve page
url = 'http://www.artscouncil.ie/en/we_funded.aspx'
br = mechanize.Browser()
response = br.open(url)
soup = BeautifulSoup(response.read())

# Get fund values
select = soup.find('select', { 'name' : 'ComponentPlaceHolder1:_ctl0:ddlFunds' })
options = select.findAll('option')

funds = {}
for option in options:
    if (len(option['value'])):
        funds[option['value']] = option.contents;

print funds;

# Get year values
select = soup.find('select', { 'name' : 'ComponentPlaceHolder1:_ctl0:ddlYear' })
options = select.findAll('option')

years = {}
for (counter, option) in enumerate(options):
    if (len(option['value'])):
        years[counter] = option.contents;

# Iterate over the two
for fund_key, fund_value in funds.iteritems() :
    fund_value = fund_value[0].encode('ascii', 'ignore') # ASCII conversion

    for year_key, year_value in years.iteritems() :
        year_value = year_value[0].encode('ascii', 'ignore') # ASCII conversion
        
        # Submit the form with relevant fund and year value
        br.select_form(name='Form1')
        br["ComponentPlaceHolder1:_ctl0:ddlFunds"] = [fund_key]
        br["ComponentPlaceHolder1:_ctl0:ddlYear"] = [year_value]

        # Uncomment these for HTTP request/response logging
        #logger = logging.getLogger("mechanize")
        #logger.addHandler(logging.StreamHandler(sys.stdout))
        #logger.setLevel(logging.DEBUG)        
        #br.set_debug_http(False)
        #br.set_debug_responses(False)

        # There are two submit buttons, so we will use the second one
        req = br.click(type="submit", nr=1)
        br.open(req)

        # Read the response from the submitted form
        response = br.response().read()
        print response
        soup = BeautifulSoup(response)

        print year_value + ", " + fund_value + ", ",

        print len(funds)

        if "Amount Awarded" in response:
            print "Got it!";

            extractTableData(year_value, fund_value)

            # Go back to the original URL for the next iteration
            response = br.open(url)
            soup = BeautifulSoup(response.read())
        elif "There were no decisions" in response:
            print "No results..."
        else:
            print "Unknown error"
