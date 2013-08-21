import scraperwiki
from string import Template
import re
from math import ceil
from BeautifulSoup import BeautifulSoup

start_page = scraperwiki.sqlite.get_var("current_page", 1) 
page = start_page 
num_pages = 1
max_pages = 500

for p in range(1, max_pages):
    page = start_page + p
    if page > num_pages:
        page -= num_pages
    scraperwiki.sqlite.save_var("current_page", page)

    page_url = Template("http://www.cra-arc.gc.ca/ebci/haip/srch/basicsearchresult-eng.action?s=+&k=&b=true&f=25&p=$page").substitute(page=page)
    
    html = scraperwiki.scrape(page_url)
    soup = BeautifulSoup(html)
    
    for result in soup.find('div', {'class':'center'}).findAll('div', {'class':'alignLeft'}, recursive=False):
        record = {}
        for entry in result.findAll('div'):
            entry_content = str(entry)
            entry_content = entry_content.replace('<div>','')
            entry_content = entry_content.replace('</div>','')
            entry_content = entry_content.replace('&nbsp;',' ')
        
            for sub_entry in entry_content.split('<b>'):
                parts = sub_entry.split(':</b>')
                if len(parts) > 1:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    m = re.search('<a[^>]+>([^<]+)<\/a>', key)
                    if m:
                        key = m.group(1).strip()
                    m = re.search('<a[^>]+>([^<]+)<\/a>', value)
                    if m:
                        value = m.group(1).strip()
                    if key == "Charity Name":
                        m = re.search('(.+)\s+\/\s+([A-Z,\d]+)', value)
                        if m:
                            name = m.group(1).strip()
                            id = m.group(2).strip()
                            record['ID'] = id
                            record['Name'] = name
                    else:
                        key = key.replace('/',' ')
                        key = key.replace('\s+','_')
                        record[key] = value

        if record.has_key('ID'):
            #print record
            # save records to the datastore
            scraperwiki.sqlite.save(["ID"], record) 

    m = re.search('<b>([\d,]+) matches found\.<\/b>', html)
    if m:
        num_results = int(m.group(1).replace(',',''))
        num_pages = ceil(num_results / 25.0)
