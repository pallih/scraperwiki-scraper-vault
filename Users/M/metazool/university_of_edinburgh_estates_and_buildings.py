###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.ed.ac.uk/schools-departments/estates-buildings/buildings-information/a-z-buildings-list'
html = scraperwiki.scrape(starting_url)
print starting_url
soup = BeautifulSoup(html)

buildings = []
extra_fields = {'Year_of_build':'building_year',
                'Premises_zone':'site',
                'Number_of_floors':'floors',
                'Energy_Grade':'energy',
                'Building_Number':'id',
                'Space_Management_zone':'zone',
                'Gross_internal_area':'area',
                'Listed_building_category':'listed'}


# use BeautifulSoup to get all <td> tags
tds = soup.findAll('li') 
for td in tds:
    link = td.find('a')
    if link is not None:
        href=link.attrs[0][1]
        m = re.search('\d+',href)
        if m is None: continue
        id = m.group()
       

        if href.rfind('Building') > -1:
            #print href
            html = None
            try:
                html = scraperwiki.scrape(href)
            except:
                continue
            soup = BeautifulSoup(html)
            building = { 'name':link.text, 'id':id }
        
            divs = soup.findAll('div')
            # basic building metadata (location)
            for dt in divs: 
                if dt.has_key('class') is True: 
                    sp = dt.findAll('span')
                    for s in sp:        
                        if s['class'] == 'postal-code': 
                            building['postcode'] = s.text
                            #try:
                            #    latlng = scraperwiki.geo.gb_postcode_to_latlng(s.text)
                            #    if latlng is not None:
                            #        building['lat'] = latlng[0]
                            #        building['lng'] = latlng[1]
                            #except: pass
                        if s['class'] == 'street-address': building['address'] = s.text
                        if s['class'] == 'locality': building['town'] = s.text
    
            # extra building attributes
            # attrs = soup.findAll('th',scope='row')
            attrs = soup.findAll('tr')
            extras = extra_fields.keys()
            for a in attrs:
                try:
                    heading = a.find('th').text
                    content = a.find('td').text
                    
                except: 
                    continue
                
                title = heading.replace(' ','_')
                if title in extras:
                 
                    building[extra_fields[title]] = content
                
            print building['name']        
            scraperwiki.sqlite.save(['id'],building)
 
                         
                
    