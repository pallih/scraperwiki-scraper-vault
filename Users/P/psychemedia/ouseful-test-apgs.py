###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page


def fullscrape():
    starting_url = 'http://www.publications.parliament.uk/pa/cm/cmallparty/register/contents.htm'
    html = scraperwiki.scrape(starting_url)


    soup = BeautifulSoup(html)
    start=soup.find(text='Section 2: Subject Groups')
    links = start.findAllNext('p',"contentsLink")

    for link in links:
        #print link.a.text,link.a['href']
        apgPageScrape(link.a.text,link.a['href'])
    
def apgPageScrape(apg,page):
    print "Trying",apg
    url="http://www.publications.parliament.uk/pa/cm/cmallparty/register/"+page
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    start=soup.find(text='Main Opposition Party')
    table=start.parent.parent.parent.parent
    table=table.find(text='10')
    table=table.parent.parent.parent
    print table
    
    lines=table.findAll('p')
    #table=table.parent.parent.findAll('td',{"colspan":"3"})
    members=[]
    '''
    exclusions=['Green','CB','Ind','DUP','CB','CBCB','SNP','PC','LD','SDLP','&#160;']
    for line in lines:
        if not line.get('style'):
            m=line.text.encode('utf-8')
            m=m.strip()
            #print ':',line.text
            if m not in exclusions and m !='':
                m=m.replace('-','–')
                m=m.split('–')
                try:
                    unicode(m[0], "ascii")
                except UnicodeError:
                    m[0] = unicode(m[0], "utf-8")
                else:
                    # value was valid ASCII data
                    pass
                if m[0]!='' and len(m[0].split())>1:
                        print '...'+m[0]+'++++'
                        members.append(m[0])
    '''
    for line in lines:
        if not line.get('style'):
            m=line.text.encode('utf-8')
            m=m.strip()    
            m=m.replace('-','–')
            m=m.split('–')
            try:
                unicode(m[0], "ascii")
            except UnicodeError:
                m[0] = unicode(m[0], "utf-8")
            else:
                # value was valid ASCII data
                pass
            if m[0]!='' and len(m[0].split())>1:
                print '...'+m[0]+'++++'
                members.append(m[0])
            
    if len(members)>20:
        members=members[:20]
    
    for m in members:
        #print m
        record= { "id":apg+":"+m, "mp":m,"apg":apg}
        scraperwiki.datastore.save(["id"], record) 
    print "....done",apg
        
#apgPageScrape()

fullscrape()

'''
Tag = soup.find(text='asa')
pTag.findAllNext(text=True)
# use BeautifulSoup to get all <td> tags
tds = soup.findAll('td') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.datastore.save(["td"], record) 
'''