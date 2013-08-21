###############################################################################
# scraper for america's billionaires http://www.forbes.com/forbes-400/list
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def scrape_list(starting_url):
    #print starting_url
    html = scraperwiki.scrape(starting_url)
    soup = BeautifulSoup(html)
    #print html
    #Rank    Name Net Worth Age Residence Source 
    for table in soup.findAll('tbody'):
        rows = table.findAll('tr')
        #print rows
        for row in rows:
            record = {'rank':None, 'name':None, 'worth':None, 'age':None, 'residence':None, 'source':None}             
            
            name=row.find('h3')
            record['name'] = name.text
    
            rank=row.find('td',{'class':'rank'})
            record['rank'] =rank.text

            worth = row.find('td',{'class':'worth'})
            record['worth'] = worth.text

            otherdata = row.findAll('td')
            #print otherdata 
            record['age'] = otherdata[3].text
            record['residence'] = otherdata[4].text
            record['source'] = otherdata[5].text     

            #print record
            scraperwiki.sqlite.save(unique_keys=['rank','name'], data=record)


pages=[1, 2, 3, 4]
#pages=['1']

for i in range(len(pages)):
    scrape_list('http://www.forbes.com/forbes-400/list/#p_' + `pages[i]` +'_s_arank_All%20industries_All%20states_All%20categories_')


