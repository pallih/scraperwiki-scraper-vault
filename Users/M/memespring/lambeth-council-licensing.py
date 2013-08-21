import scraperwiki
import BeautifulSoup

from scraperwiki import sqlite

# Lambeth Council Alcohol Licences #

#scrape page
html = scraperwiki.scrape('http://www.lambeth.gov.uk/Services/Business/LicencesStreetTrading/AlcoholEntertainmentLateNightRefreshment/CurrentApplications.htm')
page = BeautifulSoup.BeautifulSoup(html)

#find rows
for infobox in page.findAll('div', {'class': 'infoBox'}):
    for list_item in infobox.findAll('li'):

        address = list_item.find('a').string
        details= list_item.contents[4].split('last date for representations')[0].rstrip(', ').rstrip(' - ')        
        application_pdf_link = 'http://www.lambeth.gov.uk/' + list_item.find('a')['href']
        #date = list_item.contents[4].split('last date for representations')[1]
        
        #try and geolocte it
        postcode = scraperwiki.geo.extract_gb_postcode(address)
        print postcode
        latlng = None
        if postcode:
            latlng =  scraperwiki.geo.gb_postcode_to_latlng(postcode)
            
        

        #build up data object to save
        data = {
          'address' : address,
          'details' : details,                
          'application_pdf_link' : application_pdf_link,
          'latlng' : latlng,
                }
           
        #save to datastore
        sqlite.save(unique_keys=['application_pdf_link'], data=data)




