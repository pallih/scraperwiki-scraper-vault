###############################################################################
# Scrape Boston restaurant inspections via
# http://www.cityofboston.gov/isd/health/mfc/search.asp
###############################################################################

import scraperwiki
from datetime import datetime
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['LicenseNo', 'Establishment', 'Address', 'Neighborhood'])

url = 'http://www.cityofboston.gov/isd/health/mfc/search.asp'

html = BeautifulSoup(scraperwiki.scrape(url))

options = html.find("select", { "name" : "cboNhood" }).findAll("option")

for option in options:
    if len(option.contents) > 0:
        neighborhood = option.contents[0]
        
        print neighborhood
    
        # get the inspections page for a specific establishment and 
        # scrape out the inspection dates and inspection status
        neighborhoodHtml = BeautifulSoup(scraperwiki.scrape(url, { "cboNhood": neighborhood, "isPostBack": "true" }))

        # scrape_table function: gets passed an individual page to scrape
        data_tables = neighborhoodHtml.find("div", { "class" : "mainLeadStory" }).findAll("table")

        if len(data_tables) > 1:
            data_table = data_tables[1]
            rows = data_table.findAll("tr")
            for row in rows:
                # Set up our data record - we'll need it later
                record = {}
                table_cells = row.findAll("td")

                if table_cells:

                    licenseNo = table_cells[0].contents[0]['href'].replace('insphistory.asp?licno=','')
                    print licenseNo
                    record['LicenseNo'] = licenseNo
                    record['Establishment'] = table_cells[0].text
                    record['Address'] = table_cells[1].text
                    record['Neighborhood'] = table_cells[2].text
                    # Print out the data we've gathered
                    print record
                    print '------------'

                    # Finally, save the record to the datastore - 'Artist' is our unique key
                    scraperwiki.datastore.save(["LicenseNo", 'Establishment', 'Address', 'Neighborhood'], record)
                    

'''
                    # this is how you get the detail for each license but its too slow and hits the scraperwiki cpu limit
                    # Get the list of inspections for this establishment

                    inspectionHtml = BeautifulSoup(scraperwiki.scrape('http://www.cityofboston.gov/isd/health/mfc/insphistory.asp?licno=' + licenseNo))
                    inspections = inspectionHtml.find("div", { "class" : "mainLeadStory" }).findAll("li")

                    for inspection in inspections:
                    record['LicenseNo'] = licenseNo
                    record['Establishment'] = table_cells[0].text
                    record['Address'] = table_cells[1].text
                    record['Neighborhood'] = table_cells[2].text
                    inspectDate = datetime.strptime(inspection.text.split('-',1)[0], "%A, %B %d, %Y")
                    record['InspectionDate'] = inspectDate.strftime("%Y-%m-%d")
                    record['InspectionStatus'] = inspection.text.split('-',1)[1]
'''

###############################################################################
# Scrape Boston restaurant inspections via
# http://www.cityofboston.gov/isd/health/mfc/search.asp
###############################################################################

import scraperwiki
from datetime import datetime
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['LicenseNo', 'Establishment', 'Address', 'Neighborhood'])

url = 'http://www.cityofboston.gov/isd/health/mfc/search.asp'

html = BeautifulSoup(scraperwiki.scrape(url))

options = html.find("select", { "name" : "cboNhood" }).findAll("option")

for option in options:
    if len(option.contents) > 0:
        neighborhood = option.contents[0]
        
        print neighborhood
    
        # get the inspections page for a specific establishment and 
        # scrape out the inspection dates and inspection status
        neighborhoodHtml = BeautifulSoup(scraperwiki.scrape(url, { "cboNhood": neighborhood, "isPostBack": "true" }))

        # scrape_table function: gets passed an individual page to scrape
        data_tables = neighborhoodHtml.find("div", { "class" : "mainLeadStory" }).findAll("table")

        if len(data_tables) > 1:
            data_table = data_tables[1]
            rows = data_table.findAll("tr")
            for row in rows:
                # Set up our data record - we'll need it later
                record = {}
                table_cells = row.findAll("td")

                if table_cells:

                    licenseNo = table_cells[0].contents[0]['href'].replace('insphistory.asp?licno=','')
                    print licenseNo
                    record['LicenseNo'] = licenseNo
                    record['Establishment'] = table_cells[0].text
                    record['Address'] = table_cells[1].text
                    record['Neighborhood'] = table_cells[2].text
                    # Print out the data we've gathered
                    print record
                    print '------------'

                    # Finally, save the record to the datastore - 'Artist' is our unique key
                    scraperwiki.datastore.save(["LicenseNo", 'Establishment', 'Address', 'Neighborhood'], record)
                    

'''
                    # this is how you get the detail for each license but its too slow and hits the scraperwiki cpu limit
                    # Get the list of inspections for this establishment

                    inspectionHtml = BeautifulSoup(scraperwiki.scrape('http://www.cityofboston.gov/isd/health/mfc/insphistory.asp?licno=' + licenseNo))
                    inspections = inspectionHtml.find("div", { "class" : "mainLeadStory" }).findAll("li")

                    for inspection in inspections:
                    record['LicenseNo'] = licenseNo
                    record['Establishment'] = table_cells[0].text
                    record['Address'] = table_cells[1].text
                    record['Neighborhood'] = table_cells[2].text
                    inspectDate = datetime.strptime(inspection.text.split('-',1)[0], "%A, %B %d, %Y")
                    record['InspectionDate'] = inspectDate.strftime("%Y-%m-%d")
                    record['InspectionStatus'] = inspection.text.split('-',1)[1]
'''

