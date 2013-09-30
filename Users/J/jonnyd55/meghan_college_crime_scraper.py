import scraperwiki
import lxml.html

#build array, creates CSV 
oducrime = []

#SCrape the site
odu = scraperwiki.scrape('http://www.odu.edu/af/police/crimes/incidents/index.php?sort=&perpage=500&start=0&filter=')
#starts text parsing
crime = lxml.html.fromstring(odu)
#Finds table inside HTML, pulls rows you want
rows = crime.xpath("//table[@class='standardtable']/tr")[1:]
#Create loop to pull in each row as text
for row in rows:
    #This populates AN array
    log_dict={}
    log_dict ["IncDate"] = row[0].text_content()
    log_dict ["OccDate"] = row[1].text_content()
    log_dict ["Location"] = row[2].text_content()
    log_dict ["Category"] = row[3].text_content()
    log_dict ["IncNumber"] = row[4].text_content()
    log_dict ["Disposition"] = row[5].text_content()
    #Populating the array named oducrime
    oducrime.append(log_dict)
print oducrime

#Builds database and saves 
for FinalCrime in oducrime:
    scraperwiki.sqlite.save(["IncNumber"], FinalCrime, table_name='odu_crime')

import scraperwiki
import lxml.html

#build array, creates CSV 
oducrime = []

#SCrape the site
odu = scraperwiki.scrape('http://www.odu.edu/af/police/crimes/incidents/index.php?sort=&perpage=500&start=0&filter=')
#starts text parsing
crime = lxml.html.fromstring(odu)
#Finds table inside HTML, pulls rows you want
rows = crime.xpath("//table[@class='standardtable']/tr")[1:]
#Create loop to pull in each row as text
for row in rows:
    #This populates AN array
    log_dict={}
    log_dict ["IncDate"] = row[0].text_content()
    log_dict ["OccDate"] = row[1].text_content()
    log_dict ["Location"] = row[2].text_content()
    log_dict ["Category"] = row[3].text_content()
    log_dict ["IncNumber"] = row[4].text_content()
    log_dict ["Disposition"] = row[5].text_content()
    #Populating the array named oducrime
    oducrime.append(log_dict)
print oducrime

#Builds database and saves 
for FinalCrime in oducrime:
    scraperwiki.sqlite.save(["IncNumber"], FinalCrime, table_name='odu_crime')

