###############################################################################
# Basic scraper
# Public collection
# Marek Sotak - http://twitter.com/sotak
# My first python script ever ;)
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# total 4186 - we certainly are able to scrape this number
# TODO: scrape the total number of entries the hard way
# starting_url = 'http://aplikace.mvcr.cz/seznam-verejnych-sbirek/Default.aspx'
# html = scraperwiki.scrape(starting_url)
# soup = BeautifulSoup(html)
# aspnetForm
# + set the limit - start over when done

# available fields array - lucky they are using ids per field
fields = {
    'osoba' : 'ctl00_Application_LBL_OSOBA_VALUE',
    'sidlo' : 'ctl00_Application_LBL_SIDLO_VALUE',
    'ico' : 'ctl00_Application_LBL_ICO_VALUE',
    'oznaceni' : 'ctl00_Application_LBL_DESCR_VALUE',
    'region' : 'ctl00_Application_LBL_REGION_VALUE',
    'doba_od' :'ctl00_Application_LBL_DOBA_OD_VALUE',
    'doba_do' : 'ctl00_Application_LBL_DOBA_OD_VALUE',
    'zpusob' : 'ctl00_Application_LBL_WAYS_VALUE',
    'ucel' :'ctl00_Application_LBL_OTHER_PURPOSES_VALUE',
    'banka' : 'ctl00_Application_LBL_OTHER_BANKS_VALUE',
    'info' : 'ctl00_Application_LBL_OTHER_TEXT_VALUE',
    'ukoncena_od' : 'ctl00_Application_LBL_FINISHED_VALUE'
    }
# taxonomies to clean up the data - how the collection is being collected
methods = {
    'pokladničky' : 'pokladničky',
    'pokladničkami' : 'pokladničky',
    'sběrací listiny' : 'sběrací listiny',
    'prodej předmětů' : 'prodej předmětů',
    'pronájem telefonní linky' : 'pronájem telefonní linky',
    'prodej vstupenek' : 'prodej vstupenek',
    'bankovní účet' : 'bankovní účet',
    'DMS' : 'DMS',
    'Dárcovská SMS' : 'DMS',
    'prodej pamětních mincí a pamětních listů' : 'prodej pamětních mincí a pamětních listů',
    'prodej kalendářů' : 'prodej kalendářů',
    }
# purpose of the collection
purposes = [
    'rozvoj tělovýchovy a sportu',
    'ochrana životního prostředí',
    'humanitární, charitativní',
    'ochrana kulturních památek, tradic',
    'ostatní účely',
    'rozvoj vzdělání'
    ]

# metadata get
i = scraperwiki.sqlite.get_var('last_id', 1)
# run through 500 sites each run
for i in range(i, i+500):
    # retrieve a page
    # TODO: handle errors
    starting_url = 'http://aplikace.mvcr.cz/seznam-verejnych-sbirek/Detail.aspx?id=' + str(i)
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)

    # use BeautifulSoup to get all items
    record = { "id" : i }
    cz = ', Česká republika'
    for field in fields:
        field_value = soup.find("span", { "id" : fields[field] }).text
        # process fields that require special handling - TODO: more formatting
        if field == 'sidlo':
            field_value = field_value + cz.decode('utf-8')
            sidlo = field_value
        if field == 'osoba':
            osoba = field_value
        # process the taxonomy
        elif field == 'zpusob':
            method_category = []
            for method in methods:
                myvalue = method.decode('utf-8')
                if (field_value.find(myvalue) > -1):
                    field_value = field_value.replace(myvalue, '')
                    method_category.append(methods[method].decode('utf-8'))
            record['zpusob_kategorie'] = ', '.join(method_category)
                
        # process the purpose
        elif field == 'ucel':
            for purpose in purposes:
                mypurpose = purpose.decode('utf-8')
                if (field_value.find(mypurpose) > -1):
                    record['ucel_kategorie'] = purpose.decode('utf-8')
                    field_value = field_value.replace(purpose.decode('utf-8'), '')
        # process the location
        elif field == 'region':
            if (field_value == 'obce :'):
                field_value = osoba

        record[field] = field_value

    #save records to the datastore
    scraperwiki.sqlite.save(["id"], record)
    scraperwiki.sqlite.save_var('last_id', i+1)
###############################################################################
# Basic scraper
# Public collection
# Marek Sotak - http://twitter.com/sotak
# My first python script ever ;)
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# total 4186 - we certainly are able to scrape this number
# TODO: scrape the total number of entries the hard way
# starting_url = 'http://aplikace.mvcr.cz/seznam-verejnych-sbirek/Default.aspx'
# html = scraperwiki.scrape(starting_url)
# soup = BeautifulSoup(html)
# aspnetForm
# + set the limit - start over when done

# available fields array - lucky they are using ids per field
fields = {
    'osoba' : 'ctl00_Application_LBL_OSOBA_VALUE',
    'sidlo' : 'ctl00_Application_LBL_SIDLO_VALUE',
    'ico' : 'ctl00_Application_LBL_ICO_VALUE',
    'oznaceni' : 'ctl00_Application_LBL_DESCR_VALUE',
    'region' : 'ctl00_Application_LBL_REGION_VALUE',
    'doba_od' :'ctl00_Application_LBL_DOBA_OD_VALUE',
    'doba_do' : 'ctl00_Application_LBL_DOBA_OD_VALUE',
    'zpusob' : 'ctl00_Application_LBL_WAYS_VALUE',
    'ucel' :'ctl00_Application_LBL_OTHER_PURPOSES_VALUE',
    'banka' : 'ctl00_Application_LBL_OTHER_BANKS_VALUE',
    'info' : 'ctl00_Application_LBL_OTHER_TEXT_VALUE',
    'ukoncena_od' : 'ctl00_Application_LBL_FINISHED_VALUE'
    }
# taxonomies to clean up the data - how the collection is being collected
methods = {
    'pokladničky' : 'pokladničky',
    'pokladničkami' : 'pokladničky',
    'sběrací listiny' : 'sběrací listiny',
    'prodej předmětů' : 'prodej předmětů',
    'pronájem telefonní linky' : 'pronájem telefonní linky',
    'prodej vstupenek' : 'prodej vstupenek',
    'bankovní účet' : 'bankovní účet',
    'DMS' : 'DMS',
    'Dárcovská SMS' : 'DMS',
    'prodej pamětních mincí a pamětních listů' : 'prodej pamětních mincí a pamětních listů',
    'prodej kalendářů' : 'prodej kalendářů',
    }
# purpose of the collection
purposes = [
    'rozvoj tělovýchovy a sportu',
    'ochrana životního prostředí',
    'humanitární, charitativní',
    'ochrana kulturních památek, tradic',
    'ostatní účely',
    'rozvoj vzdělání'
    ]

# metadata get
i = scraperwiki.sqlite.get_var('last_id', 1)
# run through 500 sites each run
for i in range(i, i+500):
    # retrieve a page
    # TODO: handle errors
    starting_url = 'http://aplikace.mvcr.cz/seznam-verejnych-sbirek/Detail.aspx?id=' + str(i)
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)

    # use BeautifulSoup to get all items
    record = { "id" : i }
    cz = ', Česká republika'
    for field in fields:
        field_value = soup.find("span", { "id" : fields[field] }).text
        # process fields that require special handling - TODO: more formatting
        if field == 'sidlo':
            field_value = field_value + cz.decode('utf-8')
            sidlo = field_value
        if field == 'osoba':
            osoba = field_value
        # process the taxonomy
        elif field == 'zpusob':
            method_category = []
            for method in methods:
                myvalue = method.decode('utf-8')
                if (field_value.find(myvalue) > -1):
                    field_value = field_value.replace(myvalue, '')
                    method_category.append(methods[method].decode('utf-8'))
            record['zpusob_kategorie'] = ', '.join(method_category)
                
        # process the purpose
        elif field == 'ucel':
            for purpose in purposes:
                mypurpose = purpose.decode('utf-8')
                if (field_value.find(mypurpose) > -1):
                    record['ucel_kategorie'] = purpose.decode('utf-8')
                    field_value = field_value.replace(purpose.decode('utf-8'), '')
        # process the location
        elif field == 'region':
            if (field_value == 'obce :'):
                field_value = osoba

        record[field] = field_value

    #save records to the datastore
    scraperwiki.sqlite.save(["id"], record)
    scraperwiki.sqlite.save_var('last_id', i+1)
