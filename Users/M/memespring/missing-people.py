import re
import scraperwiki
import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore

#scrape rss feed
rss = scraperwiki.scrape('http://www.missingpeople.org.uk/areyoumissing/missing/rss/')
rss = BeautifulSoup.BeautifulSoup(rss)


#loop through each row
for item in rss.findAll('item'):
    
    name =  item.title.string
    description =  item.description.string.split('/>')[1].replace('<p>', '').replace('</p>', '')
    image = item.description.string.split('/>')[0].replace('<img src="', '').replace('" align="right"', '')
    image = image.strip(' ')
    image = image.replace(' ', '%20')
    link = item.link.string

       #try and extract the date the person went missing
    date_missing = None    
    regex = re.compile('(since|on) (([0-9]|[0-9][0-9])?[th]?[\s\.]?(January|February|March|April|May|June|July|August|September|October|November|December) (19|20)\d\d)', re.IGNORECASE)
    if regex.search(description):
        date_missing = regex.search(description).group(2)
        date_missing = date_missing.replace('th ', '')

        try:
            date_missing = datetime.strptime(date_missing, "%d %B %Y")
        except:
            try:
                date_missing = datetime.strptime(date_missing, "%e %B %Y")
            except:
                date_missing = None
            
    #try and match the location they were last seen
    from_location = None    
    regex = re.compile('from ([A-Z|\s]\w+(,( [A-Z|a-z]\w+)+)?).*since|(in [A-Z|\s]\w+(,( [A-Z|a-z]\w+)+)?)')
    if regex.search(description):
        from_location = regex.search(description).group(1)
        
    #save
    data = { 'name' : name, 'description' : description, 'image': image, 'from_location': from_location, 'link': link}
    #datastore.save(unique_keys=['link'], data=data, date=date_missing)
    datastore.save(unique_keys=['link'], data=data)
    









