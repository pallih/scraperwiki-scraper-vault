import re
import urllib
import csv

#Open URL and make it into a string
url = urllib.urlopen('http://grapevine.ca/mapinner.cgi')
html = url.read()
container = [("Grapevine_ID","Address","Sale_Price","Rental_Price","Listing_type","x","y")]


#CSV Writter
writer = csv.writer(open('grapevine_results.csv', 'wb', buffering=0))

#Finding all the listings in Grapevine.ca
findThis = 'function homes() {'
start = html.find(findThis) + len(findThis)
end = html[start:].find('mgr.addMarkers(gmarkers)') + start
listings = html[start:end].split(';')

#Extracting from all listings
for i in listings:   
    i = i.split('"')

#Anything with less than 5 is invalid
    if len(i) < 4:
        break

#Listing Type
    listing_type = i[0].split('showLocation')[1].replace('(','')

    if listing_type == 'B':
        listing_type = "Both"
        sale_price = i[7].replace(',','')
        rental_price = i[9].replace(',','')

    elif listing_type == 'B2':
        break

    elif listing_type == 'S':
        sale_price = i[7].replace(',','')
        rental_price = ''
        listing_type = 'Sale'
        
    elif listing_type == 'R':
        sale_price = ''
        rental_price = i[7].replace(',','')
        listing_type = 'Rental'
    
#Getting Coordinates Lat & Long
    latLong = i[1].split(',')
    y = latLong[0].strip()
    x = latLong[1].strip()

#Getting other values
    address = i[3]
    grapevine_id = i[5]

#Save it into container
    listing = (grapevine_id,address,sale_price,rental_price,listing_type,x,y)
    container.append(listing)
    
#Save it into CSV
writer.writerows(container)

print "Done!", len(container), "listings found from Grapevine.ca"
