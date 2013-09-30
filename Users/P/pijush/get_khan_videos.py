import scraperwiki
import lxml.html


# Blank Python

sl='/'
rootUrllist=[]   
furl=[]       
html = scraperwiki.scrape("https://www.khanacademy.org/library")
root = lxml.html.fromstring(html)
#ka=root.cssselect("code#response_body ")
ka=root.cssselect("a")
#print lxml.html.tostring(ka)
print(len(ka))
for c in ka:
    #print c.attrib['href']
    s=lxml.html.tostring(c)
    s=((s.split('"'))[1].split('"')[0])
    if(s[0]!=sl[0]):
        s='/'+s
    #print s[0]
    #print c.getchildren()
    rootUrl='https://www.khanacademy.org'+s #((s.split('"'))[1].split('"')[0])
    
    print rootUrl
    #if(scraperwiki.scrape(rootUrl)):
       # html2=scraperwiki.scrape(rootUrl)
        #root2 = lxml.html.fromstring(html2)
    rootUrllist.append(rootUrl)

    #ka_url=root2.cssselect("a")
    #for k in ka_url:
         #k= s=lxml.html.tostring(k) 
         #if(((k.split('"'))[1].split('"')[0])  ): 
            # k=((k.split('"'))[1].split('"')[0])    
         #print rootUrl+k
print rootUrllist
#print len(rootUrllist)
    #print 'https://www.khanacademy.org'+((s.split('"'))[1].split('"')[0]) 
#for l in rootUrllist:
    #print l