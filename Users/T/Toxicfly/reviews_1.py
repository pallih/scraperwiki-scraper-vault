import scraperwiki
import string
from scrapemark import scrape
import scraperwiki
data = scraperwiki.scrape("https://dl.dropboxusercontent.com/u/87106626/Apps.csv")
line = 0
import csv
reader = csv.reader(data.splitlines())
headerline = reader.next()

for row in reader:
 try:
     URL = row[0]+'&tab=r'
     html = scraperwiki.scrape(URL)
     #temp = html.split(':postedBy')
     #html = temp[1]
     #print html
     html = html.replace(':postedBy','>||')
     html = html.replace(':createdDate','>||')
     html = html.replace(':reviewShortDescription','>||')
     scrape_data = scrape("""
    {*

<DIV id=listingDetailPage:AppExchangeLayout:listingDetailForm:listingDetailReviewsTab:reviewsTabComponent:latestRevsContainer class=feed-container>{{ [mobile].[title2] }}</DIV>

    *}
    """, html=html);
    
     data = [{'URL': URL, 'Raw':p['title2'][0]} for p in scrape_data['mobile']]
    
     scraperwiki.sqlite.save(unique_keys=["Raw"], data=data)
 except:
    URL = '' 
    print 'Excwption'
