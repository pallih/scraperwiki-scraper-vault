import scraperwiki       

NUMROWS= 100

import lxml.html
#Seattle Police Department 911 Incident Response Info
html = scraperwiki.scrape("https://data.seattle.gov/api/views/3k2p-39jp/rows.xml?max_rows=" + str(NUMROWS))


root = lxml.html.fromstring(html)

events= root.cssselect("row row")

for curr in events:

    eventnum= int(curr.cssselect("cad_event_number")[0].text)
    
    #event clear date
    eventdate = curr.cssselect("event_clearance_date")[0].text_content()
    descriptlist = curr.cssselect("event_clearance_description")
    
    
    if len(descriptlist)>0:
        descript = descriptlist[0].text
    else:
        descript = ""
    myloclist = curr.cssselect("incident_location ")
    
    if len(myloclist)>0:
        myloc = myloclist[0]
        print myloc.attrib["latitude"] + " " + myloc.attrib["longitude"]
        mylat = myloc.attrib["latitude"]
        mylong = myloc.attrib["longitude"]
    else:
        mylat = ""
        mylong = ""

    data = {
        'Number': eventnum,
        'Clearance Date': eventdate,
        'Lat': mylat,
        'Long': mylong,
        'Description': descript
    }

    scraperwiki.sqlite.save(unique_keys=['Number'],data=data)



