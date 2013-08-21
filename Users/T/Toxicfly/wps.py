import scraperwiki
from scrapemark import scrape
import scraperwiki
data = scraperwiki.scrape("http://guptaadvocates.com/File/Book2.csv")

line = 0
import csv
reader = csv.reader(data.splitlines())
headerline = reader.next()
for row in reader:
  for page in range(1,2):
     
 
     html = scraperwiki.scrape("http://www.whitepages.com.au/busSearch.do?subscriberName="+row[0]+"&location=brisbane&expandTo=BOOK&refinement=true&refinementType=BusExpandRegion&page=%i"%page)
     print row[0]
     print page
     
     scrape_data = scrape("""
{*
href="mailto: {{ [mobile].[link] }}"
name="{{ [mobile].[name] }}">

<span class="text  ">{{ [mobile].[cat] }}</span>

*}
""", html=html);
     

     data = [{'name':p['name'][0], 'url':p['link'][0], 'Category':p['cat'][0]} for p in scrape_data['mobile']]

     scraperwiki.sqlite.save(unique_keys=["name"], data=data)