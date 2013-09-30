import scraperwiki
import lxml.html
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer

url='http://www.petrolpump.co.in/oil-companies/hpcl/retail-outlets/index.htm'
http = httplib2.Http()
status, response = http.request('http://www.petrolpump.co.in/oil-companies/hpcl/retail-outlets/index.htm')
l=[]
state=[]
for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    if link.has_key('href'):
        l=link['href'].split(':')
        if l[0]=="http":
            continue
        else:
            #print link['href']
            state.append(link['href'])
        l=[]
state_urls=[]
flag=False
flag1=False
br="The Petrol Pump Management Software  The Supermarket Management Software  Mobile Phone Shop Management Software  Medical Store Management Software"
url="http://www.petrolpump.co.in/oil-companies/hpcl/retail-outlets/assam.htm"
for i in state:
    state_urls.append(url[:-9]+i)
#for i in state_urls:
l=[]
sl_no=0
html=scraperwiki.scrape(url)
root=lxml.html.fromstring(html)
temp=[]
l2=[]
for el in root.cssselect("table "):
    for el2 in root.cssselect(" tr td"):
        var=el2.text_content()
        
        if var.count(br)>0:
            flag1=True
            break
        if flag:
             
             temp.append(var)
             #print el2
             #print lxml.html.fromstring(el2)
             l=var.split('\r\n')
             a="".join(l[1:-1])
             d=0
             l1=var.split(':')
             #print l1[-1].replace(' ','')
             #print l1[-1].replace(' ','').isdigit()
             num=l1[-1].replace(' ','')
             num=num.replace('\r\n','')
             tel=""
             for i in num:
                if i.isdigit() or i=='/':
                    tel+=i
             #num=num.replace("""\xa0""",'')
             l2.append(num)
             if len(l)>2:
                 scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Petrol_pump":l[0],"Address":a,"Telephone":tel})
             else:
                scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Petrol_pump":l[0],"Address":l[-1],"Telephone":d})
             sl_no+=1
             #print var
        if var.count('HPCL Retail Outlet/Service Stations in')>0:
            flag=True
    if flag1:
        break
#print l2
#print l
print temp
#for i in temp:
 #   print iimport scraperwiki
import lxml.html
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer

url='http://www.petrolpump.co.in/oil-companies/hpcl/retail-outlets/index.htm'
http = httplib2.Http()
status, response = http.request('http://www.petrolpump.co.in/oil-companies/hpcl/retail-outlets/index.htm')
l=[]
state=[]
for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    if link.has_key('href'):
        l=link['href'].split(':')
        if l[0]=="http":
            continue
        else:
            #print link['href']
            state.append(link['href'])
        l=[]
state_urls=[]
flag=False
flag1=False
br="The Petrol Pump Management Software  The Supermarket Management Software  Mobile Phone Shop Management Software  Medical Store Management Software"
url="http://www.petrolpump.co.in/oil-companies/hpcl/retail-outlets/assam.htm"
for i in state:
    state_urls.append(url[:-9]+i)
#for i in state_urls:
l=[]
sl_no=0
html=scraperwiki.scrape(url)
root=lxml.html.fromstring(html)
temp=[]
l2=[]
for el in root.cssselect("table "):
    for el2 in root.cssselect(" tr td"):
        var=el2.text_content()
        
        if var.count(br)>0:
            flag1=True
            break
        if flag:
             
             temp.append(var)
             #print el2
             #print lxml.html.fromstring(el2)
             l=var.split('\r\n')
             a="".join(l[1:-1])
             d=0
             l1=var.split(':')
             #print l1[-1].replace(' ','')
             #print l1[-1].replace(' ','').isdigit()
             num=l1[-1].replace(' ','')
             num=num.replace('\r\n','')
             tel=""
             for i in num:
                if i.isdigit() or i=='/':
                    tel+=i
             #num=num.replace("""\xa0""",'')
             l2.append(num)
             if len(l)>2:
                 scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Petrol_pump":l[0],"Address":a,"Telephone":tel})
             else:
                scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Petrol_pump":l[0],"Address":l[-1],"Telephone":d})
             sl_no+=1
             #print var
        if var.count('HPCL Retail Outlet/Service Stations in')>0:
            flag=True
    if flag1:
        break
#print l2
#print l
print temp
#for i in temp:
 #   print i