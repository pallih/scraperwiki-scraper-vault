import scraperwiki
import lxml.html
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer

url='http://www.petrolpump.co.in/oil-companies/bpcl/retail-outlets/index.htm'
http = httplib2.Http()
status, response = http.request('http://www.petrolpump.co.in/oil-companies/bpcl/retail-outlets/index.htm')
l=[]
place_url=[]
for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    if link.has_key('href'):
        l=link['href'].split(':')
        if l[0]=="http":
            continue
        else:
            #print link['href']
            place_url.append(link['href'])
        l=[]
complete_urls=[]
for i in place_url:
    complete_urls.append(url[:-9]+i)
temp=[]
url="http://www.petrolpump.co.in/oil-companies/bpcl/retail-outlets/Delhi.htm"
html=scraperwiki.scrape(url)
root=lxml.html.fromstring(html)
flag=False
flag1=False
flag2=True
row=[]
count=0
sl_no=1
c=0
html=scraperwiki.scrape(url)
root=lxml.html.fromstring(html)
for el in root.cssselect("table "):
    for el2 in root.cssselect(" tr td"):
        #print el2.text_content()
        var=el2.text_content()
        #print var
        if var.count('National Service Station')>0:
            if flag2==True:
                flag2=False
            else:
                flag2==True
        if flag and var=='\r\n':
            flag1=True
            break
        if flag:
            print var
            temp.append(var)
            if count<2:
                row.append(var)
                count+=1
            else:
                count=0
                #print len(row)
                if flag2:
                    scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Petrol_pump":row[0],"Address":row[1]})
                    flag2=False
                else:
                    scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"Petrol_pump":row[1],"Address":row[0]})
                    flag2=True
                sl_no+=1
                row=[]
                #print var
        if var.count('Address')>0:
            c+=1
            print "works"
            if c== 2:
                flag=True
    if flag1:
        break
print temp
            
        
    