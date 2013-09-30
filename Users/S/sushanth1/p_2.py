"""
Data will be stored in the following format: (one row for each company)

URL, Company Name, Revenue, ....


"""
import scraperwiki
from lxml import etree

def get_company_info(url):
    
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
            if(flag==1):
                netprofit=profit.text
                flag=0
            if(profit.text=="Reported Net Profit"):
                flag=flag+1
    
    
            if(incomeflag==1):            
                totalincome=profit.text
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
    
    
        data = {
            'url': url,
            'name': tree.find('.//title').text.split('Share Price')[0],
            'industry':industry,
            'location':location,
            'phoneno':phoneNo,
            'netprofit':netprofit,
            'keyexecutives':'. '.join(keyexec),
            'totalincome':totalincome,
        }
        print repr(data)
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)
    
    except:
        print 'Url not found'

def get_companies(letter):
  
    url = 'http://www.indiainfoline.com/Markets/Company/%s.aspx' % letter
    text = scraperwiki.scrape(url)
    tree = etree.HTML(text)
    for link in tree.findall('.//div[@class="topnews_middle"]//a'):
        href = link.get('href')
        if href and href.startswith('/Markets/Company/'):
            get_company_info('http://www.indiainfoline.com' + href)
  

for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    get_companies(letter)
"""
Data will be stored in the following format: (one row for each company)

URL, Company Name, Revenue, ....


"""
import scraperwiki
from lxml import etree

def get_company_info(url):
    
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
            if(flag==1):
                netprofit=profit.text
                flag=0
            if(profit.text=="Reported Net Profit"):
                flag=flag+1
    
    
            if(incomeflag==1):            
                totalincome=profit.text
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
    
    
        data = {
            'url': url,
            'name': tree.find('.//title').text.split('Share Price')[0],
            'industry':industry,
            'location':location,
            'phoneno':phoneNo,
            'netprofit':netprofit,
            'keyexecutives':'. '.join(keyexec),
            'totalincome':totalincome,
        }
        print repr(data)
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)
    
    except:
        print 'Url not found'

def get_companies(letter):
  
    url = 'http://www.indiainfoline.com/Markets/Company/%s.aspx' % letter
    text = scraperwiki.scrape(url)
    tree = etree.HTML(text)
    for link in tree.findall('.//div[@class="topnews_middle"]//a'):
        href = link.get('href')
        if href and href.startswith('/Markets/Company/'):
            get_company_info('http://www.indiainfoline.com' + href)
  

for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    get_companies(letter)
