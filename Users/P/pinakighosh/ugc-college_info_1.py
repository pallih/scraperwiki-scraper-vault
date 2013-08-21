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
a1="University Contact Information"
b1="VC Information"
c1="Registrars Information"
a="1."
b="2."
c="3."
d=dict()
flag_a=False
flag_b=False
flag_c=False
sl_no=0
for id in l2:
    html = scraperwiki.scrape("http://www.ugc.ac.in/uni_contactinfo.aspx?id="+str(id))
    root = lxml.html.fromstring(html)
    for el in root.cssselect(" div.centerpaneltable table#ctl00_bps_homeCPH_dluniversity"):
        s=1
        for el2 in el.cssselect("div table"):
            for el3 in el.cssselect("tr td"):
                #print el3.text_content()
                #print s
                #s+=1
                text=el3.text_content()
                #print text
                
                if text.count(a)>0:
                    flag_a=True
                    flab_b=False
                    flag_c=False
                    print "a,"+str(flag_a)
                    print "b,"+str(flag_b)
                    print "c,"+str(flag_c)
                elif text.count(b)>0 or text.count("VC's Information")>0:
                    print "here"
                    flag_a=False
                    flag_b=True
                    flag_c=False
                    print "a,"+str(flag_a)
                    print "b,"+str(flag_b)
                    print "c,"+str(flag_c)
                elif text.count(c)>0 or text.count("Registrar's Information")>0:
                    flag_a=False
                    flab_b=False
                    flag_c=True
                    print "a,"+str(flag_a)
                    print "b,"+str(flag_b)
                    print "c,"+str(flag_c)
                if flag_a:
                    d[a1]=text
                elif flag_b:
                    #print '*'*6
                    d[b1]=text
                if flag_c:
                    print '*'*6
                    d[c1]=text
            #print '*'*6
    try:
        print d[a1]
    except:
        print a1
    try:
        print d[b1]
    except:
        print b1
    try:
        print d[c1]
    except:
        print c1
    scraperwiki.sqlite.save(unique_keys=["sl_no"],data={"sl_no":sl_no,"UCI":d[a1],"VCI":d[b1],"RI":d[c1]})
    sl_no+=1