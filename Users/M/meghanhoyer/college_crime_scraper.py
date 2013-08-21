import scraperwiki
import lxml.html
oducrime = []

odu = scraperwiki.scrape('http://www.odu.edu/af/police/crimes/incidents/index.php?sort=&perpage=500&start=0&filter=')
crime = lxml.html.fromstring(odu)
rows = crime.xpath("//table[@class='standardtable']/tr")
#print headers
for row in rows:
    log_dict={}
    log_dict ["IncDate"] = row[0].text_content()
    log_dict ["OccDate"] = row[1].text_content()
    log_dict ["Location"] = row[2].text_content()
    log_dict ["Category"] = row[3].text_content()
    log_dict ["IncNumber"] = row[4].text_content()
    log_dict ["Disposition"] = row[5].text_content()
    oducrime.append(log_dict)
print oducrime

for FinalCrime in oducrime:
    scraperwiki.sqlite.save(["IncNumber"], FinalCrime, table_name='odu_crime')

