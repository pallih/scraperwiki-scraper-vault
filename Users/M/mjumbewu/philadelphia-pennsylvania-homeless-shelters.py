###############################################################################
# Philadelphia Pennsylvania Homeless Shelters
#
# Fields:
#   name
#   phone #
#   address
#   city
#   state
#   zip
#   url
#
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.homelessshelterdirectory.org/cgi-bin/id/city.cgi?city=Philadelphia&state=PA'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# Skip past all the cruft at the top of the page
outer_table = soup.find('table', {'width':'100%'}) 
data_table = outer_table.find('table')
shelter_tds = data_table.findAll('td', {'width':'73%'})

for shelter_td in shelter_tds:
    shelter_name_a = shelter_td.find('a')

    name = shelter_name_a.text
    url = shelter_name_a['href']

    # Since the phone number and address are separated only by <br> elements, we'll have to manually parse them out.
    cell_code = str(shelter_td).\
        replace(str(shelter_name_a), '').\
        replace('<td valign="top" width="73%">', '').\
        replace('</td>','').replace('&nbsp;',' ')
    shelter_info_pieces = [s.strip() for s in cell_code.split('<br />')]
    
    # The first piece is the phone number
    phone = shelter_info_pieces[0]
    
    # Some cells contain a line after the phone number, describing distance from center city.  Some don't.  So, we have to work backward.

    # The last and second-to-last pieces are almost always city/state/zip and address, respectively.
    address = shelter_info_pieces[-3]
    csz = shelter_info_pieces[-2]
    
    # Ignore the verified shelter designation lines.
    if csz.startswith('<!--- Homeless Shelter Directory Verification --->'):
        address = shelter_info_pieces[-4]
        csz = shelter_info_pieces[-3]

    csz_pieces = csz.split(',') # into [city, state/zip]
    city = csz_pieces[0].strip()

    sz_pieces = csz_pieces[1].rsplit(' ', 1) # into [state, zip]
    state = sz_pieces[0].strip()
    zip = sz_pieces[1].strip()
    
    record = {
        'name':name,
        'phone':phone,
        'address':address,
        'city':city,
        'state':state,
        'zip':zip,
        'url':url
    }

    # save records to the datastore
    scraperwiki.sqlite.save(["name"], record) 
    