import scraperwiki
from BeautifulSoup import BeautifulSoup
import lxml.html

#Get the HTML from the NSSDC Master Catalog.
html = scraperwiki.scrape("http://nssdc.gsfc.nasa.gov/nmc/spacecraftSearch.do?discipline=All")

#Pass it to BeautifulSoup to make it navigable.
soup = BeautifulSoup(html)

#Grab the table.
table = soup.table

#Grab all the <tr> tags.
tr_list = table.findAll('tr')

#Grab all the <td> children tags.
td_list = []
for tr_entry in tr_list:
    td_entry = tr_entry.findAll('td')
    td_list.append(td_entry)

#First entry is empty, so pop it.
td_list.pop(0)

#Separate the content into four different lists (Spacecraft Name, NSSDC ID, Launch Date, and Record Link)
spacecraft_name_list = []
nssdc_list = []
launch_date_list = []
record_link_list = []
launch_vehicle_list = []
launch_mass_list = []
funding_agency_list = []
discpline_list = []
launch_site_list = []
description_list = []
alternate_name_list = []
for block in td_list: # to limit the items processed, add [x:y] where x is the starting element, and y is the ending (y < 6821)
    name = block[0].a.contents
    spacecraft_name_list.append(name[0])
    nssdc = block[1].contents
    nssdc_list.append(nssdc[0])
    launch_date = block[2].contents
    launch_date_list.append(launch_date[0])
    link = "http://nssdc.gsfc.nasa.gov"+block[0].a['href']
    record_link_list.append(link)
    #start scrape on individual page
    html2 = scraperwiki.scrape(link) 
    # soup2 = BeautifulSoup(html2)

    root = lxml.html.fromstring(html2) # turn our HTML into an lxml object
    divs = root.cssselect("div.urtwo")
    for div in divs:
        totext = lxml.html.tostring(div)
        #print totext
        stext = totext.split('<strong>Launch Vehicle:</strong>&#160;')
        #print stext
        stext2 = stext[1].split('<br>')
        stext3 = stext2[0]
        #print stext3

        launch_vehicle = stext3
        launch_vehicle_list.append(launch_vehicle)

        stext = totext.split('<strong>Mass:</strong>&#160;')
        stext3 = ''
        if len(stext)>1:
            stext2 = stext[1].split('<br>')
            stext3 = stext2[0].replace('&#160;', ' ')
        #print stext3

        launch_mass = stext3
        launch_mass_list.append(launch_mass)

        stext = totext.split('<strong>Launch Site:</strong>&#160;')
        stext3 = ''
        if len(stext)>1:
            stext2 = stext[1].split('<br>')
            stext3 = stext2[0].replace('&#160;', ' ')
        #print stext3

        launch_site = stext3
        launch_site_list.append(launch_site)

        stext = totext.split('<h2>Funding Agenc')
        #print stext
        stext4 = ''
        if len(stext)>1:
            stext2 = stext[1].split('<li>')
            stext3 = stext2[1].split('</li>')
            stext4 = stext3[0]
            #print stext4

        funding_agency = stext4
        funding_agency_list.append(funding_agency)

        stext = totext.split('<h2>Alternate Nam')
        #print stext
        stext4 = ''
        if len(stext)>1:
            stext2 = stext[1].split('<li>')
            stext3 = stext2[1].split('</li>')
            stext4 = stext3[0]
            #print stext4
            

        alternate_name = stext4
        alternate_name_list.append(alternate_name)


        totext2 = lxml.html.tostring(root)
        print totext2
        stext = totext2.split('<h2>Description</h2>')
        #print stext
        stext4 = ''
        if len(stext)>1:
            stext2 = stext[1].split('<p>')
            stext3 = stext2[1].split('</p>')
            stext4 = stext3[0]
            #print stext4

        description = stext4
        description_list.append(description)

        # Just gets first discpline, will get more later
        stext = totext.split('<h2>Discipline')
        #print stext
        stext2 = stext[1].split('<li>')
        stext3 = stext2[1].split('</li>')
        stext4 = stext3[0].replace('&amp;', '&')
        #print stext4

        discpline = stext4
        discpline_list.append(discpline)
        
        

    # print soup2.findAll('div', limit=1)
    # launch_vehicle_list.append(launch_vehicle)
    


new_table = sorted(zip(nssdc_list, spacecraft_name_list, launch_date_list, record_link_list, launch_vehicle_list, launch_mass_list, funding_agency_list, discpline_list, launch_site_list, description_list, alternate_name_list), key=lambda nssdc: nssdc[0])

for item in new_table:
    scraperwiki.sqlite.save(unique_keys=["nssdc_id"], data={"nssdc_id":item[0], "spacecraft_name":item[1], "launch_date":item[2], "record_link":item[3], "launch_vehicle":item[4], "launch_mass":item[5], "funding_agency":item[6], "discpline":item[7], "launch_site":item[8], "description":item[9], "alternate_name":item[10]})
