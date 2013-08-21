import scraperwiki
import lxml.html
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import string

char=string.ascii_uppercase
alpha=[]
for i in char:
    alpha.append('&page='+i)
url='http://www.chennaiiq.com/india/pincode/index.asp'
http = httplib2.Http()
status, response = http.request(url)
l=[]
state=[]
state_list=[]
for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    if link.has_key('href'):
        l=link['href']
        if l[:4]=='?id=':
            #print link['href']
            state_list.append(link['href'][17:])
            state.append(url+link['href'])
        else:
            continue
state_url=[]
for i in state:
    var=i.split('&state_name=')
    var[-1]='&state_name='+var[-1].replace(' ','%20')
    state_url.append("".join(var))
data=[]
count=0
sl_no=1
state_url=state_url[30:32]
state_list=state_list[30:32]
alpha=alpha[14:]
for i in state_url:
    print i
for j in range(len(state_url)):
    for i in alpha:
        #if j==30 
        url1=state_url[j]+i
        print url1
        html=scraperwiki.scrape(url1)
        root=lxml.html.fromstring(html)
        for el in root.cssselect("table.TBox tr.tab"):
            for el2 in el.cssselect("tr.tab td"):
                data.append(el2.text_content())
            if len(data)==5:
                #print data[2]+data[4]           
                scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"State":state_list[j],"Place":data[2],"Pincode":data[4]})
                sl_no+=1
            data=[]
            
