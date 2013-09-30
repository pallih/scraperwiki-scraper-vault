import scraperwiki

# Blank Python


import scraperwiki
import lxml.html
import re


page_counter = 0
record_counter = 0
while True: # loop through pages
    
    page_counter +=1
    pageurl = "http://www.autotrader.co.uk/search/used/cars/land_rover/discovery/postcode/g699dw/radius/1500/price-to/25000/maximum-age/up_to_5_years_old/sort/default/price-from/9000/page/{$page_counter}"

    html = scraperwiki.scrape(pageurl)
    root = lxml.html.fromstring(html)
    for el in root.cssselect("div.searchResult"):    # for each record on this page

        advertReference = int(re.sub('[advert]', '', el.attrib['id'])) #scrape advert reference number


        eg = root.cssselect("div.vehicleTitle a")[0].text  

        model = re.sub('[Land Rover ]', '', eg)
        if eg.find(" GS")>0:  typ = "GS"     #scrape discovery type
        elif eg.find(" SPECIAL EDITION ")>0: typ =  "SE"  
        elif eg.find(" HSE ")>0: typ =  "HSE"  
        elif eg.find(" SE ")>0: typ =  "SE"  
        elif eg.find(" S ")>0: typ =  "S"  
        elif eg.find(" XS ")>0: typ =  "XS"  
        else: typ =  "Other"  
        #year = el.find("h3",0 ).innertext
        year = root.cssselect("h3")[0].text 
        year =  re.sub('[, 4x4]', '', year) # scrape year
        eg = root.cssselect("div.offerPrice span")[0].text
        price = int(re.sub('[\D]', '', eg)) # scrape price as integer
        mileage = root.cssselect("span.mileage")[0].text
        mileage = int(re.sub('[\D]', '', mileage)) # scrape milage as integer
        distance = root.cssselect("span.distanceAmount")[0].text
        distance = int(re.sub('[\D]', '', distance)) # scrape distance as integer
        url = root.cssselect("h2 a")[0].attrib['href']   # scrape url      
        record_counter+=1
        print (record_counter + "\t" + 
        advertReference + "\t" + 
        model + "\t"+
        typ + "\t"+
        year + "\t"+
        distance + "\t"+
        mileage + "\t"+
        price  + "\t"+
        url + "\n")
        if (typ=="GS"): break                     #dont save crappy GS models
        description = el.find("div.searchResultMainText",0 ).innertext
        if description.find(" Cloth ")>0: break  #dont save cloth seats 
        if page_counter <50: 
            scraperwiki.sqlite.save(unique_keys=["guid"], data={ 
            'guid' : advertReference,
            'record' : record_counter,
            'model' : model,
            'type' : typ,
            'year' : year,
            'distance' : distance,
            'mileage' : mileage,
            'price' : price,
            'url' : url
            } //endarray
            ) //endsave

    if (page_counter <50 ):break


import scraperwiki

# Blank Python


import scraperwiki
import lxml.html
import re


page_counter = 0
record_counter = 0
while True: # loop through pages
    
    page_counter +=1
    pageurl = "http://www.autotrader.co.uk/search/used/cars/land_rover/discovery/postcode/g699dw/radius/1500/price-to/25000/maximum-age/up_to_5_years_old/sort/default/price-from/9000/page/{$page_counter}"

    html = scraperwiki.scrape(pageurl)
    root = lxml.html.fromstring(html)
    for el in root.cssselect("div.searchResult"):    # for each record on this page

        advertReference = int(re.sub('[advert]', '', el.attrib['id'])) #scrape advert reference number


        eg = root.cssselect("div.vehicleTitle a")[0].text  

        model = re.sub('[Land Rover ]', '', eg)
        if eg.find(" GS")>0:  typ = "GS"     #scrape discovery type
        elif eg.find(" SPECIAL EDITION ")>0: typ =  "SE"  
        elif eg.find(" HSE ")>0: typ =  "HSE"  
        elif eg.find(" SE ")>0: typ =  "SE"  
        elif eg.find(" S ")>0: typ =  "S"  
        elif eg.find(" XS ")>0: typ =  "XS"  
        else: typ =  "Other"  
        #year = el.find("h3",0 ).innertext
        year = root.cssselect("h3")[0].text 
        year =  re.sub('[, 4x4]', '', year) # scrape year
        eg = root.cssselect("div.offerPrice span")[0].text
        price = int(re.sub('[\D]', '', eg)) # scrape price as integer
        mileage = root.cssselect("span.mileage")[0].text
        mileage = int(re.sub('[\D]', '', mileage)) # scrape milage as integer
        distance = root.cssselect("span.distanceAmount")[0].text
        distance = int(re.sub('[\D]', '', distance)) # scrape distance as integer
        url = root.cssselect("h2 a")[0].attrib['href']   # scrape url      
        record_counter+=1
        print (record_counter + "\t" + 
        advertReference + "\t" + 
        model + "\t"+
        typ + "\t"+
        year + "\t"+
        distance + "\t"+
        mileage + "\t"+
        price  + "\t"+
        url + "\n")
        if (typ=="GS"): break                     #dont save crappy GS models
        description = el.find("div.searchResultMainText",0 ).innertext
        if description.find(" Cloth ")>0: break  #dont save cloth seats 
        if page_counter <50: 
            scraperwiki.sqlite.save(unique_keys=["guid"], data={ 
            'guid' : advertReference,
            'record' : record_counter,
            'model' : model,
            'type' : typ,
            'year' : year,
            'distance' : distance,
            'mileage' : mileage,
            'price' : price,
            'url' : url
            } //endarray
            ) //endsave

    if (page_counter <50 ):break


