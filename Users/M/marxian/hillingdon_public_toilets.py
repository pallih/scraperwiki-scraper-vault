import scraperwiki
from geopy import geocoders 
import xlrd

xlbin = scraperwiki.scrape("http://publicloo.neontribe.co.uk/data/hillingdon-gla-v2.xls")
book = xlrd.open_workbook(file_contents=xlbin)
sheet = book.sheet_by_index(0)    

ONS_CODE = "E09000017"

# We need to transform most of this data through 90 degrees...

# Make a store of header values  - which we find in column B
fields = sheet.col_values(1, 1) # grab the values from the field column (omit the header)


for loodex in range (4, sheet.ncols):
    rawloo = {}
    col = sheet.col_values(loodex, 1)
    for fdex, field in enumerate(fields):
        if col[fdex]: # Column has data for this field
            val = col[fdex]
            if val == 'y':
                val = True
            if val == 'n':
                val = False
            rawloo[field] = val


    try:
        cleaned_data = {'ons_code': ONS_CODE }
        cleaned_data['name'] = rawloo[u'Name of building / park / location']    
        cleaned_data['address'] = ', '.join([cleaned_data['name'], 'Hillingdon'])

        #Horrid Hack
        cleaned_data['postcode'] = cleaned_data['address']

        # Geocoding is tricky here since there's no explicit locational data
        # We know all of these are libraries so:
        g = geocoders.Google(domain='maps.google.co.uk')    
        place, (lat, lng) = g.geocode(cleaned_data['address'])
        cleaned_data['WGS84_lat'] = lat
        cleaned_data['WGS84_long'] = lng

        cleaned_data['disabled'] = rawloo['Is it wheelchair accessible?']
        cleaned_data['babychanging'] = rawloo['Does it have babychange facilities?']

        scraperwiki.sqlite.save(unique_keys=['name', 'address'], data=cleaned_data)

    except ValueError:
        #We'll pass on any loo which doesn't geocode well
        pass

    



