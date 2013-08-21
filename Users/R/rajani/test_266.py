import scraperwiki

# Blank Python
"""
Data will be stored in the following format: (one row for each company)

URL, Company Name, Revenue, ....


"""
import scraperwiki
from lxml import etree

def get_company_info(url,company_count):
    
    try:
        
        text = scraperwiki.scrape(url)
        tree = etree.HTML(text)
        keyexec=[]
        length=0
        count=0
        netprofit=0
        urllist=[]
        totalincome=0
        urllist=url.split('Company/')
        profiturl=str(urllist[0])+str("Company/Fundamentals/Profit-Loss/")+str(urllist[1])
        
        
        tree1 = etree.HTML(scraperwiki.scrape(profiturl))
        flag=0
        incomeflag=0
        
        for profit in tree1.findall('.//tr//td'):
            #print 'profit',profit.text
            if(flag==1):         
                netprofit=profit.text.replace(',','')
                break
            if(profit.text=="Reported Net Profit" or profit.text=="Net Profit"):
                flag=flag+1
    
    
            if(incomeflag==1):            
                totalincome=profit.text.replace(',','')
                incomeflag=0
            if(profit.text=="Total Income"):            
                incomeflag=incomeflag+1
                   
              
        count=0
        for j in tree.findall('.//*[@class="Rborder"]'):
            length=length+1
        for k in tree.findall('.//*[@class="Rborder"]//h4'):
            if(count<length):
                
                keyexec.append(k.text.replace(' ,',':'))
            count=count+1
        
        for key in tree.findall('.//h2[@class="MCnt1"]'):
            children = key.getchildren()
            indus=children[-1].tail.split('Industry:')
            industry=indus[1][1:-16]


        for year in tree.findall('.//tr[@class="tbl_header_company"]'):
            children = year.getchildren()
            yr=children[-1].tail.split('Particulars')
            print "year",children
        
        for details in tree.findall('.//div[@class="LH"]//tr//td'):              
            try:
                address_data=details.getchildren()
                phno=address_data[3].tail.split('Phone : ')
                location=address_data[1].tail+address_data[2].tail
                phoneNo=phno[1]
                break                       
            except:
                continue
        if(netprofit==0):
            netprofit=""
        if(totalincome==0):
            totalincome=""
        name=tree.find('.//h1').text
        data = {
            'url': url,
            'name': name,
            'industry':industry,
            'location':location,
            'phoneno':phoneNo,
            'netprofit':netprofit,
            'keyexecutives':'. '.join(keyexec),
            'totalincome':totalincome,
        }
        loc_data=location.split(',')
        state_data=(loc_data[1]).split('-')
        state=state_data[0]
        states=['Andhra Pradesh','Karnataka','Tamil Nadu']
        #print state
        if(name=='Amara Raja Batteries Ltd'):
            print name,company_count
        if(state in states):
            #print 'The state is ',state,' and the location is ', location  
            #print repr(data)
            scraperwiki.sqlite.save(unique_keys=['url'], data=data)
    
    except:
        print 'Url not found'

def get_companies(letter,start,end):
    print letter
    try:
        url = 'http://www.indiainfoline.com/Markets/Company/%s.aspx' % letter
        text = scraperwiki.scrape(url)
        tree = etree.HTML(text)
        company_count=0
        for link in tree.findall('.//div[@class="topnews_middle"]//a'):
            company_count=company_count+1
            if(company_count<start):
                #print company_count
                pass
            else:
                href = link.get('href')
                if href and href.startswith('/Markets/Company/'):
                    get_company_info('http://www.indiainfoline.com' + href,company_count)
    except:
        print 'Internet connection problem'

for letter in 'PQRSTUVWXYZ':
    get_companies(letter,232,100)
