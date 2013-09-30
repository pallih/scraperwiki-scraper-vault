import scraperwiki
import lxml.html
import string

s_no=0
l1=[range(1, 674)]
l2=[]
for i in range(674):
    l2.append(i+1)
    s_no=s_no+1

print len(l2)
#print l2
for id in l2:
    html = scraperwiki.scrape("http://www.ugc.ac.in/uni_contactinfo.aspx?id="+str(id))
    #print html
    #print id
    root = lxml.html.fromstring(html)
    #print root
#select div where data exists
    for el in root.cssselect("div.centerpaneltable tr"):
        for el2 in el.cssselect("tr td"):
            text=''.join(el2.text_content().split())
            l=[]
            l.append(text)
            print l

            d1=dict()
            d1[text]=""
            for i in range(len(text)):
                if i%4==0:
                    key=text[i]
                            
            if el2.text_content().count("1.")>0:
                print "hello"
            else:
                print "bye"
        print "*******"

#saving the data
scraperwiki.sqlite.save(unique_keys=['sl_no'], data=text}import scraperwiki
import lxml.html
import string

s_no=0
l1=[range(1, 674)]
l2=[]
for i in range(674):
    l2.append(i+1)
    s_no=s_no+1

print len(l2)
#print l2
for id in l2:
    html = scraperwiki.scrape("http://www.ugc.ac.in/uni_contactinfo.aspx?id="+str(id))
    #print html
    #print id
    root = lxml.html.fromstring(html)
    #print root
#select div where data exists
    for el in root.cssselect("div.centerpaneltable tr"):
        for el2 in el.cssselect("tr td"):
            text=''.join(el2.text_content().split())
            l=[]
            l.append(text)
            print l

            d1=dict()
            d1[text]=""
            for i in range(len(text)):
                if i%4==0:
                    key=text[i]
                            
            if el2.text_content().count("1.")>0:
                print "hello"
            else:
                print "bye"
        print "*******"

#saving the data
scraperwiki.sqlite.save(unique_keys=['sl_no'], data=text}