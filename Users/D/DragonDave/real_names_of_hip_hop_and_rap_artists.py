# Blank Python
import BeautifulSoup, scraperwiki,re
url = "http://www.whudat.com/hip_hop_real_names/"
html = scraperwiki.scrape(url)
print html
soup = BeautifulSoup.BeautifulSoup(html)

rows=soup.find('div',{'id':'tagbox'}).findAll('tr')

for item in rows:
    a_tag=item.find('td').find('a')
    try:
        artist={'url':a_tag['href'],
                'stage':a_tag.text,
                'real':item.findAll('td')[1].text
               }
    except:
         continue

    # clean up names where there is a band name: format "Band [Artist]" or "Band - Artist"
    if artist['stage'].find('[')>-1:        
        (artist['band'], artist['stage'])=re.search(r'(.*) \[(.*)\]',artist['stage']).groups()
    if artist['stage'].find(' - ')>-1:
        (artist['band'], artist['stage'])=re.search(r'(.*) \- (.*)',artist['stage']).groups()


    scraperwiki.datastore.save(unique_keys=['url'], data=artist)
 