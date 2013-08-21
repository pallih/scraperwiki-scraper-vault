import scraperwiki
import string
import urllib2

# Blank Python
#scraperwiki.sqlite.execute("drop table bbb")
#scraperwiki.sqlite.execute("create table bbb (`Concern`,`Contact`,`Address`)")
#http://www.commonfloor.com/builders

html = scraperwiki.scrape("http://justdial.com/Mumbai/Masstek-%3Cnear%3E-Near-Sanghvi-Industrial-Estate-Kandivali-West/022P1309422_TXVtYmFpIEFudGlxdWUgRGVhbGVycyBkZWxoaQ==_BZDET")
print html

#mylist=[]

#for index in range(len(mylist)):
#        try:
#            html = scraperwiki.scrape(mylist[index])
#            c=len(html)
#            a=html.find("padding:0px 10px 0px 10px;")
#            b=html.find("float:left;width:530px")
#            d=html[a:-(c-b)]
#            e=index+1
#            f=d.find("<strong>")
#            g=d.find("</strong>")
#            h=len(d)
#            i=d[f+8:-(h-g)]
#            j=d.find("Address:</strong>")
#            k=d.find("padding:3px;")
#            l=d[j+22:-(h-k)-12]
#            m=d.find("Contact:</strong>")
#            o=d[m+17:-50]
#            z=index+1
#            scraperwiki.sqlite.execute("insert into bbb values (?,?,?)", (mylist[index],o,l))
#            scraperwiki.sqlite.commit()
#        except urllib2.HTTPError, err:
#            print err
#            if err.getcode() == 404:
#                continue #not a problem.  move on to next date.
                
     
