import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://services.parliament.uk/bills/AllBills.rss'
rss = scraperwiki.scrape(starting_url)

rss_soup = BeautifulSoup(rss)

for item in rss_soup.findAll('item'):

    page_url = item.guid.contents[0]
    page_html = scraperwiki.scrape(page_url)
    html_soup = BeautifulSoup(page_html)
    name1 = None
    name2 = None
    department1 = None
    department2 = None

    #title
    title = html_soup.find('h1').string

    #status
    last_event = html_soup.find('div', {'class': 'last-event'}).find('img')['alt']

    #other details
    detail = html_soup.find('dl', {'class': 'bill-agents'})
    dts = detail.findAll('dt')
    dds = detail.findAll('dd')

    counter = 0
    key_values = {}
    for dd in dds:
        if counter < len(dts):
            if dts[counter].string == None:
                key = 'unknown' 
            else:                
                key = dts[counter].string.replace(':', '')
                if key == 'Sponsors' or key == 'Sponsor':
                    key = 'Sponsor 1'
        else:
            key = 'Sponsor 2'

        key_values[key] = dd.contents
        key_values['id'] = counter

        #Bill type
        bill_type = key_values['Type of Bill'][0]
        
        #split out department name and MP name
        if 'Sponsor 1' in key_values:
            name1 = key_values['Sponsor 1'][0]
            department1 = key_values['Sponsor 1'][3].string.strip()
    
        if 'Sponsor 2' in key_values:
            name2 = key_values['Sponsor 2'][0]
            department2 = key_values['Sponsor 2'][3].string.strip()

        #increase counter

        counter = counter + 1


    #save
    data = {'title': title, 'url': page_url, 'sponsor name 1': name1, 'sponsor name 2': name2, 'sponsor department 1': department1,'sponsor department 2': department2, 'bill type': bill_type}
        
    scraperwiki.datastore.save(['url',], data=data)