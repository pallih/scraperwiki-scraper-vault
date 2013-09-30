import scraperwiki
import urllib
import lxml.html.soupparser
from time import sleep
import resource
# Blank Python

def detailpage(urlfragment):
    #print urlfragment
    html = scraperwiki.scrape('https://rn.ftc.gov/pls/textilern/'+urlfragment)
    root = lxml.html.soupparser.fromstring(html)
    data={}
    for row in map(lxml.html.HtmlElement.text_content, root.cssselect('table tr')):
        s=row.split(':')
        data[s[0]]=s[1]
    #print data
    return data
"""        
RN Type:    RN
RN Number:    137278
Legal Name:    PICKLE PEA, LLC
Company Name:    PICKLE PEAS
Business Type:    WHOLESALER
Address Line 1:    PO BOX 513
City:    OLD SAYBROOK
State Code:    CT
Zip:    06475
Phone:    203-913 9291 Ext:
Product Line:    INFANT CLOTHING, SHIRTS, ONESIES, PANTS
"""


def querypage(start=1):
    assert (start-1)%10 == 0, "Strange start number: start %d"%start # check we're using reasonable pages
    rows=0
    url='https://rn.ftc.gov/pls/textilern/wrnquery$tts_rn.querylist' # post

    form={
        "P_RN_TYPE":"",
        "P_RN_busTYPE":"",
        "P_RN_SEQ":"",
        "P_L_CO_LEGAL_NAME":"",
        "P_L_CO_COMPANY_NAME":"",
        "P_L_CO_ADD_CITY":"",
        "P_L_CO_ADD_STATE_CODE":"",
        "P_L_CO_ADD_ZIP":"",
        "P_PRODUCT_LINE":"",
        "Z_START":str(start), # increase by 10 every time.
        "Z_ACTION":"Next", # Last or Query
        "Z_CHK":"0"
    }

    # note, 1/Next will give you the second page; use 11/Last to get first page.
    if start==-9:
        print "Start = -9 special case"
        form['Z_START']='11'
        form['Z_ACTION']='First'
    
    fileh=urllib.urlopen(url,urllib.urlencode(form))
    html=fileh.read()
    fileh.close()
    #print html
    root = lxml.html.soupparser.fromstring(html) # doesn't find table otherwise
    for row in root.cssselect("table tr")[1:]: # Keep 1, skip column headers
        rows=rows+1
        dataurl=row[0].cssselect('a')[0].attrib['href']
        data=detailpage(dataurl)
        data['url']=dataurl
        scraperwiki.sqlite.save(unique_keys=['url'], data=data) # given that the URL contals type/number, this *should* be a reasonal key.
        sleep(1)
    assert rows>0, "No rows found: start #%d"%start
    assert rows==10, "Funny number of rows found (%d): start %d"%(rows,start)
    
querynum=scraperwiki.sqlite.get_var('querynum',-9)
querynum=max(23051,querynum)
delay=1
bail=False
while not bail:
    print "Querying %s"%querynum
    try:
        querypage(querynum)
        delay=1
        #print "memory: ",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    except Exception, e:
        scraperwiki.sqlite.save_var('querynum',querynum)
        print "Error, querynum %s; state saved just in case"%querynum
        print e
        if "ScraperWiki" in e:
            print type(e)
            print "Bailing!"
            assert False,"ScraperWiki asked me to stop (State Saved)"
            bail=True

        delay=delay*2
        querynum=querynum-10 # to offset later change.
        if delay>5000:
            assert False, "Delayed out."
        sleep(delay) # wait an increasing number of minutes
    querynum=querynum+10
    
    import scraperwiki
import urllib
import lxml.html.soupparser
from time import sleep
import resource
# Blank Python

def detailpage(urlfragment):
    #print urlfragment
    html = scraperwiki.scrape('https://rn.ftc.gov/pls/textilern/'+urlfragment)
    root = lxml.html.soupparser.fromstring(html)
    data={}
    for row in map(lxml.html.HtmlElement.text_content, root.cssselect('table tr')):
        s=row.split(':')
        data[s[0]]=s[1]
    #print data
    return data
"""        
RN Type:    RN
RN Number:    137278
Legal Name:    PICKLE PEA, LLC
Company Name:    PICKLE PEAS
Business Type:    WHOLESALER
Address Line 1:    PO BOX 513
City:    OLD SAYBROOK
State Code:    CT
Zip:    06475
Phone:    203-913 9291 Ext:
Product Line:    INFANT CLOTHING, SHIRTS, ONESIES, PANTS
"""


def querypage(start=1):
    assert (start-1)%10 == 0, "Strange start number: start %d"%start # check we're using reasonable pages
    rows=0
    url='https://rn.ftc.gov/pls/textilern/wrnquery$tts_rn.querylist' # post

    form={
        "P_RN_TYPE":"",
        "P_RN_busTYPE":"",
        "P_RN_SEQ":"",
        "P_L_CO_LEGAL_NAME":"",
        "P_L_CO_COMPANY_NAME":"",
        "P_L_CO_ADD_CITY":"",
        "P_L_CO_ADD_STATE_CODE":"",
        "P_L_CO_ADD_ZIP":"",
        "P_PRODUCT_LINE":"",
        "Z_START":str(start), # increase by 10 every time.
        "Z_ACTION":"Next", # Last or Query
        "Z_CHK":"0"
    }

    # note, 1/Next will give you the second page; use 11/Last to get first page.
    if start==-9:
        print "Start = -9 special case"
        form['Z_START']='11'
        form['Z_ACTION']='First'
    
    fileh=urllib.urlopen(url,urllib.urlencode(form))
    html=fileh.read()
    fileh.close()
    #print html
    root = lxml.html.soupparser.fromstring(html) # doesn't find table otherwise
    for row in root.cssselect("table tr")[1:]: # Keep 1, skip column headers
        rows=rows+1
        dataurl=row[0].cssselect('a')[0].attrib['href']
        data=detailpage(dataurl)
        data['url']=dataurl
        scraperwiki.sqlite.save(unique_keys=['url'], data=data) # given that the URL contals type/number, this *should* be a reasonal key.
        sleep(1)
    assert rows>0, "No rows found: start #%d"%start
    assert rows==10, "Funny number of rows found (%d): start %d"%(rows,start)
    
querynum=scraperwiki.sqlite.get_var('querynum',-9)
querynum=max(23051,querynum)
delay=1
bail=False
while not bail:
    print "Querying %s"%querynum
    try:
        querypage(querynum)
        delay=1
        #print "memory: ",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    except Exception, e:
        scraperwiki.sqlite.save_var('querynum',querynum)
        print "Error, querynum %s; state saved just in case"%querynum
        print e
        if "ScraperWiki" in e:
            print type(e)
            print "Bailing!"
            assert False,"ScraperWiki asked me to stop (State Saved)"
            bail=True

        delay=delay*2
        querynum=querynum-10 # to offset later change.
        if delay>5000:
            assert False, "Delayed out."
        sleep(delay) # wait an increasing number of minutes
    querynum=querynum+10
    
    