import scraperwiki
import lxml.html     

# Blank Python

# URL Pattern = http://idris.idrc.ca/app/Search?request=viewsinglerecord&num=1 - 

html = scraperwiki.scrape("http://idris.idrc.ca/app/Search?request=viewsinglerecord&num=1")
root = lxml.html.fromstring(html)
count = int(root.cssselect("div[class='searchSummary']")[0].text_content().split('of')[1].split('ordered')[0].strip())
print count

for page in range(1, count):
    try:
        html = scraperwiki.scrape("http://idris.idrc.ca/app/Search?request=viewsinglerecord&num="+str(page))
        root = lxml.html.fromstring(html)
        data = {}
        data['title'] = root.cssselect("span[class='doctitle']")[0].text_content()
        data['iati_identifier'] = root.cssselect("div[class='summary'] span")[1].text_content().replace('Project Number','').strip()
        data['start_date'] = root.cssselect("div[class='summary'] span")[2].text_content().replace('Start Date','').replace('&nbsp;','').strip()
        data['programme_area'] = root.cssselect("div[class='summary'] span")[1].text_content().replace('Program Area/Group','').strip()
        
        data['location'] = []
        for location in root.cssselect("table table")[0].cssselect("a"):
            data['location'].append(location.text_content().replace('&nbsp;','').strip())
        
        
        for field in root.cssselect("div[class='fullcontent'] tr"):
            fieldname = field.cssselect("td")[0].text_content().replace('&nbsp;','').strip().replace('(','').replace(')','')
            try:
                fieldvalue = field.cssselect("td")[1].text_content().replace('&nbsp;','').strip()
                if fieldname:
                    data[fieldname] = fieldvalue
            except:
                data['Recipient Institution'] = fieldname
        
        # Note, we could then look to also grab publications data related to this activity...
    
        scraperwiki.sqlite.save(unique_keys=['iati_identifier'], data=data)
    except: 
        pass    
        
    
