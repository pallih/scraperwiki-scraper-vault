import scraperwiki
from BeautifulSoup import BeautifulSoup

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

#Separate the content into three different lists (Spacecraft Name, NSSDC ID, and Launch Date)
spacecraft_name_list = []
nssdc_list = []
launch_date_list = []
for block in td_list:
    name = block[0].a.contents
    spacecraft_name_list.append(name)
    nssdc = block[1].contents
    nssdc_list.append(nssdc)
    launch_date = block[2].contents
    launch_date_list.append(launch_date)

new_table = sorted(zip(nssdc_list, spacecraft_name_list, launch_date_list), key=lambda nssdc: nssdc[0])

for item in new_table:
    scraperwiki.sqlite.save(unique_keys=["nssdc_id"], data={"nssdc_id":item[0], "spacecraft_name":item[1], "launch_date":item[2]})

import scraperwiki
from BeautifulSoup import BeautifulSoup

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

#Separate the content into three different lists (Spacecraft Name, NSSDC ID, and Launch Date)
spacecraft_name_list = []
nssdc_list = []
launch_date_list = []
for block in td_list:
    name = block[0].a.contents
    spacecraft_name_list.append(name)
    nssdc = block[1].contents
    nssdc_list.append(nssdc)
    launch_date = block[2].contents
    launch_date_list.append(launch_date)

new_table = sorted(zip(nssdc_list, spacecraft_name_list, launch_date_list), key=lambda nssdc: nssdc[0])

for item in new_table:
    scraperwiki.sqlite.save(unique_keys=["nssdc_id"], data={"nssdc_id":item[0], "spacecraft_name":item[1], "launch_date":item[2]})

