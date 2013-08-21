import scraperwiki
import re
import time
import urlparse
import codecs
import chardet
from scraperwiki.sqlite import save

baseurl = "http://canada.odmp.org/search.php?searching=1&lastname=&agency=&agencyid=&state=&yearfrom=1865&yearto=2013&cause=&outofstate=&adv=&offset=" 
urlender = "#results"

columns = [
    'Name','Office Link','Force','Photo link','End of Watch','Age','Tour of Duty','Cause of Death','Desription'
]

deadcount = 0

def officerscraper(officerlink):
    officerpagesource = scraperwiki.scrape(officerlink)
    re.sub('û', 'u', officerpagesource)
    re.sub('é', 'e', officerpagesource)
    d = chardet.detect(officerpagesource)
    if type(officerpagesource) != unicode:
        officerpagesource = officerpagesource.decode(d['encoding']).encode('utf-8','replace') 
    name = re.search('span class="officername">(.+?)<', officerpagesource)
    name = name.group(1)
    force = re.search('class="officername">(.+?)<\/span><br><strong>(.+?)<', officerpagesource)
    force = force.group(2)
    eow = re.search('<br>End of Watch:(.+?)<', officerpagesource)
    eow = eow.group(1)
    photolink = re.search('<img(.+?)class="officerpic(.+?)>', officerpagesource)
    photolink = re.search('src="(.+?)"', photolink.group(0))
    photolink = "http://canada.odmp.org" + photolink.group(1)
    age = re.search('<strong>Age:(.+?)<br>', officerpagesource)
    age = age.group(1)
    age = re.sub('<\/strong>', '', age)
    age = re.sub('<font color="#d0d0d0">', '', age)
    age = re.sub('<\/font>', '', age)
    tod = re.search('<strong>Tour of Duty:(.+?)<', officerpagesource)
    tod = tod.group(1)
    tod = re.sub('<\/strong>', '', tod)
    cod = re.search('<strong>Cause of Death:(.+?)<', officerpagesource)
    cod = cod.group(1)
    cod = re.sub('<\/strong>', '', cod)
    description = re.search('Suspect Info(.+?)<\/strong>(.+?)<\/p><p>(.+?)<', officerpagesource)
    description = description.group(3)
    record = {}
    try:
        record['Name'] = name
    except:
        record['Name'] = "Invalid characters"
    try:
        record['Force'] = force
    except:
        record['Force'] = "Invalid characters"
    try:
        record['Photo Link'] = photolink
    except:
        record['Photo Link'] = "Invalid characters"
    try:
        record['End of Watch'] = eow
    except:
        record['End of Watch'] = "Invalid characters"
    try:
        record['Age'] = age
    except:
        record['Age'] = "Invalid characters"
    try:
        record['Tour of Duty'] = tod
    except:
        record['Tour of Duty'] = "Invalid characters"
    try:
        record['Cause of Death'] = cod
    except:
        record['Cause of Death'] = "Invalid characters"
    try:
        record['Description'] = description
    except:
        record['Description'] = "Invalid characters"
    try:
        record['Officer Link'] = officerlink
    except:
        record['Description'] = "Invalid characters"
    save([], record)
        
def officercounter(searchpage):
    listpagesource = scraperwiki.scrape(searchpage)
    for every_officer in re.finditer('href="\/officer\/(.+?)"', listpagesource):
        officerbaselink = "http://canada.odmp.org/officer/"
        officerlink = officerbaselink + every_officer.group(1)
        officerscraper(officerlink)
        time.sleep(1)
    time.sleep(1)

while deadcount < 851: 
    searchpage = baseurl + str(deadcount) + urlender
    officercounter(searchpage)
    deadcount = deadcount + 25
