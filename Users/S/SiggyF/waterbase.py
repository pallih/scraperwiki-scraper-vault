import scraperwiki
import lxml.html

def updateobservationtype():
    # Open the Dutch waterbase html
    html = scraperwiki.scrape("http://live.waterbase.nl/waterbase_wns.cfm?taal=nl")
    # Parse the html
    root = lxml.html.fromstring(html)
    # Loop over the options in the form
    
    for el in list(root.cssselect("select[name=wbwns1]>option")):           
        # get the value that contains the id and the text
        value = el.attrib.get('value')
        text = el.text
        if value:
            # We should be able to get an id and the name
            idtxt, name = value.split('|')
        else:
            continue
        record = {
            'id': int(idtxt),
            'name': name
            }
        # Store these in table observationtype (dutch=waarnemingssoort)
        scraperwiki.sqlite.save(unique_keys=['id'], data=record, table_name="observationtype")

def updatelocations():
    # Lookup all observation types
    rs = scraperwiki.sqlite.execute('SELECT * FROM observationtype;')
    # for all observation types
    for row in rs['data']:
        # generate a url
        rowdict = dict(zip(rs['keys'], row))
        url = 'http://live.waterbase.nl/waterbase_locaties.cfm?whichform=1&wbwns1={}'.format(rowdict['id'])
        # Load it
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        # Loop over the options in the form
        # these options contain the valid observation and location combinations
        for el in list(root.cssselect("select[name=loc]>option")):
            location_id = el.attrib.get('value')
            if not location_id:
                continue
            name = el.text
            record = {
                'observationtype_id': rowdict['id'],
                'location_id': location_id
                }
            # Store the location observation combinations
            scraperwiki.sqlite.save(unique_keys=['observationtype_id','location_id'], data=record, table_name='location_observationtype')
            # Also store the locations
            record = {'id': location_id, 'name': name}
            scraperwiki.sqlite.save(unique_keys=['id'], data=record, table_name="location")

updateobservationtype()
updatelocations()
