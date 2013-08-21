import scraperwiki
import lxml.html
# Blank Python
import urllib2
import socket
import array

#USES DATA PUBLISHED BY 'NETCRAFT http://news.netcraft.com/about-netcraft/ AN INTERNET SECURITY AND DATA PROVISION COMPANY

base_url = 'http://toolbar.netcraft.com/stats/topsites?c='
country= 'IT'
end_url= '&submit=Refresh'
url=base_url+country+end_url

html1 = scraperwiki.scrape(url)
root = lxml.html.fromstring(html1)
table =""
count=0

ranges = []

#make a list of the ip ranges/netblocks
for el in root.cssselect("tr.TBtr a"):
    try:
        urls = el.attrib['href']
        netblock = urls.split('?')
        if netblock[0]=='/netblock':
            ranges.append(urls)
    except:
        count +=1

#make a list of the ip ranges/netblocks
for el in root.cssselect("tr.TBtr2 a"):
    try:
        urls = el.attrib['href']
        netblock = urls.split('?')
        if netblock[0]=='/netblock':
            ranges.append(urls)
    except:
        count +=1


print len(ranges)
count =0 

for el in ranges:
    splitrange=el.split(",")
    #print splitrange[len(splitrange)-2], splitrange[len(splitrange)-1]
    print count
    count+=1
    #scraperwiki.sqlite.save(unique_keys=["a"], data={"a":count,"b":splitrange[len(splitrange)-2],"c":splitrange[len(splitrange)-1]})

count =0

for el in root.cssselect("tr.TBtr"):
    try:
        domain = socket.gethostbyname(el[1].text_content().split('/')[2])
    except:
        domain = "didn't resolve"
    scraperwiki.sqlite.save(unique_keys=["a"], data={"a":el[1].text_content(),"b":domain,"c":ranges[count]})
    count +=1

for el in root.cssselect("tr.TBtr2"):
    try:
        domain = socket.gethostbyname(el[1].text_content().split('/')[2])
    except:
        domain = "didn't resolv"
    scraperwiki.sqlite.save(unique_keys=["a"], data={"a":el[1].text_content(),"b":domain,"c":ranges[count]})
    count +=1
