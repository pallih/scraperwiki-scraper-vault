#far better to use the API...

import scraperwiki

import lxml.html

def crunchScraper(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    #for item in root.xpath('//h2[@id="current_relationships"]/following-sibling::div[not(preceding::h2[id="former_relationships"])]/div[@class="col1_people_name "]'):
    cname=root.xpath('//title')[0].text.split('|')[0].strip()
    print 'current'
    groupdata=[]
    for item in root.xpath('//h2[@id="current_relationships"]/following-sibling::div[@class="col1_content"]//div[not(preceding::h2[@id="former_relationships"]) ]'):#and @class="col1_people_name "
        #Should really add a datestamp...
        data={'company':url,'cname':cname,'currency':'current'}
        if (item.xpath('./a')):
            if item.xpath('./a/@href')[0] !='#':
                print '..',item.xpath('./a/@href')[0],item.xpath('./a/@title')[0]
                data['name']=item.xpath('./a/@title')[0]
                data['id']=item.xpath('./a/@href')[0]
        else:
            print item.xpath('.')[0].text
            if item.xpath('.')[0].text !=None: data['role']=item.xpath('.')[0].text
            else: data['role']=''
        if 'id' in data: groupdata.append(data)
    print groupdata
    scraperwiki.sqlite.save(unique_keys=['id','company'], table_name='eduCrunchbase', data=groupdata)
    print 'previous'
    groupdata=[]
    for item in root.xpath('//h2[@id="former_relationships"]/following-sibling::div[@class="col1_content"]//div'):
        data={'company':url,'cname':cname,'currency':'previous'}
        if (item.xpath('./a')):
            if item.xpath('./a/@href')[0] !='#':
                print '..',item.xpath('./a/@href')[0],item.xpath('./a/@title')[0]
                data['name']=item.xpath('./a/@title')[0]
                data['id']=item.xpath('./a/@href')[0]
        else:
            print item.xpath('.')[0].text
            if item.xpath('.')[0].text !=None: data['role']=item.xpath('.')[0].text
            else: data['role']=''
        if 'id' in data: groupdata.append(data)
    print groupdata
    scraperwiki.sqlite.save(unique_keys=['id','company'], table_name='eduCrunchbase', data=groupdata)

urls=["http://www.crunchbase.com/company/2u", "http://www.crunchbase.com/company/kno", "http://www.crunchbase.com/company/desire2learn", "http://www.crunchbase.com/company/kaltura", "http://www.crunchbase.com/company/rafter", "http://www.crunchbase.com/company/knewton", "http://www.crunchbase.com/company/grockit", "http://www.crunchbase.com/company/xueersi", "http://www.crunchbase.com/company/edmodo", "http://www.crunchbase.com/company/parchment", "http://www.crunchbase.com/company/axilogix-education", "http://www.crunchbase.com/company/connectedu", "http://www.crunchbase.com/company/knowledge-adventure", "http://www.crunchbase.com/company/altius-education", "http://www.crunchbase.com/company/flat-world-knowledge", "http://www.crunchbase.com/company/zeebo", "http://www.crunchbase.com/company/coursera", "http://www.crunchbase.com/company/universitynow", "http://www.crunchbase.com/company/everfi", "http://www.crunchbase.com/company/trovix", "http://www.crunchbase.com/company/bloomfire", "http://www.crunchbase.com/company/apreso-classroom", "http://www.crunchbase.com/company/classteacher-learning-systems", "http://www.crunchbase.com/company/k-12-techno-services", "http://www.crunchbase.com/company/revolution-prep"]

for u in urls:
    crunchScraper(u)