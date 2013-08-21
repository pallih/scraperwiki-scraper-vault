# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime

url = "http://www.thetakeoverpanel.org.uk/disclosure/disclosure-table"

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def ScrapeRecord(table):
    data = { }
    rows = list(table)

    troffee = rows.pop(0)
    mofferee = re.match("OFFEREE: (.*)$", troffee[0][0].text)
    assert mofferee, lxml.etree.tostring(troffee)
    data["offeree"] = mofferee.group(1).strip()
    
    trcommence = rows.pop(0)
    mcd = re.match("Offer period commenced: (\d\d):(\d\d) (\d+)-(\w\w\w)-(\d\d\d\d)$", trcommence[0].text)
    assert mcd, lxml.etree.tostring(trcommence)

    imonth = months.index(mcd.group(4))+1
    commencedate = datetime.datetime(int(mcd.group(5)), imonth, int(mcd.group(3)), int(mcd.group(1)), int(mcd.group(2)))
    data["commencedate"] = commencedate
    
    isin = []

    while True:
        tr3 = rows.pop(0)   # isin nonsense
        if len(tr3) == 3:
            c2 = tr3[1].text
            mc2= re.match("ISIN: (.*)$", c2)
            if mc2: 
                isin.append(mc2.group(1))
            else:
                assert c2 == u'\xa0'
            continue
        
        break

    data["isin"] = ",".join(isin)

    mofferor = re.match("OFFEROR: (.*)$", tr3[0][0].text)
    assert mofferor, lxml.etree.tostring(tr3)
    offerer = mofferor.group(1).strip()

    if rows:
        data["offerer"] = offerer
        tr4 = rows.pop(0)

        mcd = re.match("Offeror identified: (\d\d):(\d\d) (\d+)-(\w\w\w)-(\d\d\d\d)$", tr4[0].text)
        assert mcd, lxml.etree.tostring(tr4)
    
        imonth = months.index(mcd.group(4))+1
        identifieddate = datetime.datetime(int(mcd.group(5)), imonth, int(mcd.group(3)), int(mcd.group(1)), int(mcd.group(2)))
        data["identifieddate"] = identifieddate

    else:
        assert offerer == 'No named offeror'

    return data


# stock symbols can be obtained using this lookup
# iurl = "http://investegate.co.uk/Index.aspx?searchtype=5&words=%s" % isin
# iurl2 = "http://investegate.co.uk/Index.aspx?%s" % urllib.urlencode({ "searchtype":"2", "words":data.get("offeree")})
# txt = urllib.urlopen(url).read()
# c = re.findall('<a href="/Compdata\.aspx\?(.*)">', txt)

scrapedate = datetime.datetime.now()

def Main():
    root = lxml.html.parse(url).getroot()
    disctable= root.cssselect('div.disclosuretable')[0]
    tdisctable = lxml.html.tostring(disctable)

    try:
        prevdisctable = scraperwiki.sqlite.select("text from disctable order by scrapedate desc limit 1")[0]["text"]
        if tdisctable == prevdisctable:
            print "No change"
            return
    except scraperwiki.sqlite.NoSuchTableSqliteError:
        pass
    scraperwiki.sqlite.save(["scrapedate"], {"scrapedate":scrapedate, "text":tdisctable}, table_name="disctable")

    title = disctable[0].text_content()
    assert title == u'THE TAKEOVER PANEL \u2013 DISCLOSURE TABLE', title
    tabledate = disctable[1].text_content()

    # we should look for changes and record, handling the missing entries
    for t in disctable[2:]:
        assert t.tag == "table", lxml.html.tostring(t)
        if len(t) == 1 and t[0][0].text == 'Notes:':
            break
        if len(t) <= 2:
            v = [ lxml.etree.tostring(tr)  for tr in t ]
            #print "\n".join(v)
            continue
        data = ScrapeRecord(t)
        scraperwiki.sqlite.save(unique_keys=["offeree", "commencedate"], data=data)

# need to get the change date
        
Main()

                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime

url = "http://www.thetakeoverpanel.org.uk/disclosure/disclosure-table"

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def ScrapeRecord(table):
    data = { }
    rows = list(table)

    troffee = rows.pop(0)
    mofferee = re.match("OFFEREE: (.*)$", troffee[0][0].text)
    assert mofferee, lxml.etree.tostring(troffee)
    data["offeree"] = mofferee.group(1).strip()
    
    trcommence = rows.pop(0)
    mcd = re.match("Offer period commenced: (\d\d):(\d\d) (\d+)-(\w\w\w)-(\d\d\d\d)$", trcommence[0].text)
    assert mcd, lxml.etree.tostring(trcommence)

    imonth = months.index(mcd.group(4))+1
    commencedate = datetime.datetime(int(mcd.group(5)), imonth, int(mcd.group(3)), int(mcd.group(1)), int(mcd.group(2)))
    data["commencedate"] = commencedate
    
    isin = []

    while True:
        tr3 = rows.pop(0)   # isin nonsense
        if len(tr3) == 3:
            c2 = tr3[1].text
            mc2= re.match("ISIN: (.*)$", c2)
            if mc2: 
                isin.append(mc2.group(1))
            else:
                assert c2 == u'\xa0'
            continue
        
        break

    data["isin"] = ",".join(isin)

    mofferor = re.match("OFFEROR: (.*)$", tr3[0][0].text)
    assert mofferor, lxml.etree.tostring(tr3)
    offerer = mofferor.group(1).strip()

    if rows:
        data["offerer"] = offerer
        tr4 = rows.pop(0)

        mcd = re.match("Offeror identified: (\d\d):(\d\d) (\d+)-(\w\w\w)-(\d\d\d\d)$", tr4[0].text)
        assert mcd, lxml.etree.tostring(tr4)
    
        imonth = months.index(mcd.group(4))+1
        identifieddate = datetime.datetime(int(mcd.group(5)), imonth, int(mcd.group(3)), int(mcd.group(1)), int(mcd.group(2)))
        data["identifieddate"] = identifieddate

    else:
        assert offerer == 'No named offeror'

    return data


# stock symbols can be obtained using this lookup
# iurl = "http://investegate.co.uk/Index.aspx?searchtype=5&words=%s" % isin
# iurl2 = "http://investegate.co.uk/Index.aspx?%s" % urllib.urlencode({ "searchtype":"2", "words":data.get("offeree")})
# txt = urllib.urlopen(url).read()
# c = re.findall('<a href="/Compdata\.aspx\?(.*)">', txt)

scrapedate = datetime.datetime.now()

def Main():
    root = lxml.html.parse(url).getroot()
    disctable= root.cssselect('div.disclosuretable')[0]
    tdisctable = lxml.html.tostring(disctable)

    try:
        prevdisctable = scraperwiki.sqlite.select("text from disctable order by scrapedate desc limit 1")[0]["text"]
        if tdisctable == prevdisctable:
            print "No change"
            return
    except scraperwiki.sqlite.NoSuchTableSqliteError:
        pass
    scraperwiki.sqlite.save(["scrapedate"], {"scrapedate":scrapedate, "text":tdisctable}, table_name="disctable")

    title = disctable[0].text_content()
    assert title == u'THE TAKEOVER PANEL \u2013 DISCLOSURE TABLE', title
    tabledate = disctable[1].text_content()

    # we should look for changes and record, handling the missing entries
    for t in disctable[2:]:
        assert t.tag == "table", lxml.html.tostring(t)
        if len(t) == 1 and t[0][0].text == 'Notes:':
            break
        if len(t) <= 2:
            v = [ lxml.etree.tostring(tr)  for tr in t ]
            #print "\n".join(v)
            continue
        data = ScrapeRecord(t)
        scraperwiki.sqlite.save(unique_keys=["offeree", "commencedate"], data=data)

# need to get the change date
        
Main()

                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime

url = "http://www.thetakeoverpanel.org.uk/disclosure/disclosure-table"

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def ScrapeRecord(table):
    data = { }
    rows = list(table)

    troffee = rows.pop(0)
    mofferee = re.match("OFFEREE: (.*)$", troffee[0][0].text)
    assert mofferee, lxml.etree.tostring(troffee)
    data["offeree"] = mofferee.group(1).strip()
    
    trcommence = rows.pop(0)
    mcd = re.match("Offer period commenced: (\d\d):(\d\d) (\d+)-(\w\w\w)-(\d\d\d\d)$", trcommence[0].text)
    assert mcd, lxml.etree.tostring(trcommence)

    imonth = months.index(mcd.group(4))+1
    commencedate = datetime.datetime(int(mcd.group(5)), imonth, int(mcd.group(3)), int(mcd.group(1)), int(mcd.group(2)))
    data["commencedate"] = commencedate
    
    isin = []

    while True:
        tr3 = rows.pop(0)   # isin nonsense
        if len(tr3) == 3:
            c2 = tr3[1].text
            mc2= re.match("ISIN: (.*)$", c2)
            if mc2: 
                isin.append(mc2.group(1))
            else:
                assert c2 == u'\xa0'
            continue
        
        break

    data["isin"] = ",".join(isin)

    mofferor = re.match("OFFEROR: (.*)$", tr3[0][0].text)
    assert mofferor, lxml.etree.tostring(tr3)
    offerer = mofferor.group(1).strip()

    if rows:
        data["offerer"] = offerer
        tr4 = rows.pop(0)

        mcd = re.match("Offeror identified: (\d\d):(\d\d) (\d+)-(\w\w\w)-(\d\d\d\d)$", tr4[0].text)
        assert mcd, lxml.etree.tostring(tr4)
    
        imonth = months.index(mcd.group(4))+1
        identifieddate = datetime.datetime(int(mcd.group(5)), imonth, int(mcd.group(3)), int(mcd.group(1)), int(mcd.group(2)))
        data["identifieddate"] = identifieddate

    else:
        assert offerer == 'No named offeror'

    return data


# stock symbols can be obtained using this lookup
# iurl = "http://investegate.co.uk/Index.aspx?searchtype=5&words=%s" % isin
# iurl2 = "http://investegate.co.uk/Index.aspx?%s" % urllib.urlencode({ "searchtype":"2", "words":data.get("offeree")})
# txt = urllib.urlopen(url).read()
# c = re.findall('<a href="/Compdata\.aspx\?(.*)">', txt)

scrapedate = datetime.datetime.now()

def Main():
    root = lxml.html.parse(url).getroot()
    disctable= root.cssselect('div.disclosuretable')[0]
    tdisctable = lxml.html.tostring(disctable)

    try:
        prevdisctable = scraperwiki.sqlite.select("text from disctable order by scrapedate desc limit 1")[0]["text"]
        if tdisctable == prevdisctable:
            print "No change"
            return
    except scraperwiki.sqlite.NoSuchTableSqliteError:
        pass
    scraperwiki.sqlite.save(["scrapedate"], {"scrapedate":scrapedate, "text":tdisctable}, table_name="disctable")

    title = disctable[0].text_content()
    assert title == u'THE TAKEOVER PANEL \u2013 DISCLOSURE TABLE', title
    tabledate = disctable[1].text_content()

    # we should look for changes and record, handling the missing entries
    for t in disctable[2:]:
        assert t.tag == "table", lxml.html.tostring(t)
        if len(t) == 1 and t[0][0].text == 'Notes:':
            break
        if len(t) <= 2:
            v = [ lxml.etree.tostring(tr)  for tr in t ]
            #print "\n".join(v)
            continue
        data = ScrapeRecord(t)
        scraperwiki.sqlite.save(unique_keys=["offeree", "commencedate"], data=data)

# need to get the change date
        
Main()

                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime

url = "http://www.thetakeoverpanel.org.uk/disclosure/disclosure-table"

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def ScrapeRecord(table):
    data = { }
    rows = list(table)

    troffee = rows.pop(0)
    mofferee = re.match("OFFEREE: (.*)$", troffee[0][0].text)
    assert mofferee, lxml.etree.tostring(troffee)
    data["offeree"] = mofferee.group(1).strip()
    
    trcommence = rows.pop(0)
    mcd = re.match("Offer period commenced: (\d\d):(\d\d) (\d+)-(\w\w\w)-(\d\d\d\d)$", trcommence[0].text)
    assert mcd, lxml.etree.tostring(trcommence)

    imonth = months.index(mcd.group(4))+1
    commencedate = datetime.datetime(int(mcd.group(5)), imonth, int(mcd.group(3)), int(mcd.group(1)), int(mcd.group(2)))
    data["commencedate"] = commencedate
    
    isin = []

    while True:
        tr3 = rows.pop(0)   # isin nonsense
        if len(tr3) == 3:
            c2 = tr3[1].text
            mc2= re.match("ISIN: (.*)$", c2)
            if mc2: 
                isin.append(mc2.group(1))
            else:
                assert c2 == u'\xa0'
            continue
        
        break

    data["isin"] = ",".join(isin)

    mofferor = re.match("OFFEROR: (.*)$", tr3[0][0].text)
    assert mofferor, lxml.etree.tostring(tr3)
    offerer = mofferor.group(1).strip()

    if rows:
        data["offerer"] = offerer
        tr4 = rows.pop(0)

        mcd = re.match("Offeror identified: (\d\d):(\d\d) (\d+)-(\w\w\w)-(\d\d\d\d)$", tr4[0].text)
        assert mcd, lxml.etree.tostring(tr4)
    
        imonth = months.index(mcd.group(4))+1
        identifieddate = datetime.datetime(int(mcd.group(5)), imonth, int(mcd.group(3)), int(mcd.group(1)), int(mcd.group(2)))
        data["identifieddate"] = identifieddate

    else:
        assert offerer == 'No named offeror'

    return data


# stock symbols can be obtained using this lookup
# iurl = "http://investegate.co.uk/Index.aspx?searchtype=5&words=%s" % isin
# iurl2 = "http://investegate.co.uk/Index.aspx?%s" % urllib.urlencode({ "searchtype":"2", "words":data.get("offeree")})
# txt = urllib.urlopen(url).read()
# c = re.findall('<a href="/Compdata\.aspx\?(.*)">', txt)

scrapedate = datetime.datetime.now()

def Main():
    root = lxml.html.parse(url).getroot()
    disctable= root.cssselect('div.disclosuretable')[0]
    tdisctable = lxml.html.tostring(disctable)

    try:
        prevdisctable = scraperwiki.sqlite.select("text from disctable order by scrapedate desc limit 1")[0]["text"]
        if tdisctable == prevdisctable:
            print "No change"
            return
    except scraperwiki.sqlite.NoSuchTableSqliteError:
        pass
    scraperwiki.sqlite.save(["scrapedate"], {"scrapedate":scrapedate, "text":tdisctable}, table_name="disctable")

    title = disctable[0].text_content()
    assert title == u'THE TAKEOVER PANEL \u2013 DISCLOSURE TABLE', title
    tabledate = disctable[1].text_content()

    # we should look for changes and record, handling the missing entries
    for t in disctable[2:]:
        assert t.tag == "table", lxml.html.tostring(t)
        if len(t) == 1 and t[0][0].text == 'Notes:':
            break
        if len(t) <= 2:
            v = [ lxml.etree.tostring(tr)  for tr in t ]
            #print "\n".join(v)
            continue
        data = ScrapeRecord(t)
        scraperwiki.sqlite.save(unique_keys=["offeree", "commencedate"], data=data)

# need to get the change date
        
Main()

                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime

url = "http://www.thetakeoverpanel.org.uk/disclosure/disclosure-table"

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def ScrapeRecord(table):
    data = { }
    rows = list(table)

    troffee = rows.pop(0)
    mofferee = re.match("OFFEREE: (.*)$", troffee[0][0].text)
    assert mofferee, lxml.etree.tostring(troffee)
    data["offeree"] = mofferee.group(1).strip()
    
    trcommence = rows.pop(0)
    mcd = re.match("Offer period commenced: (\d\d):(\d\d) (\d+)-(\w\w\w)-(\d\d\d\d)$", trcommence[0].text)
    assert mcd, lxml.etree.tostring(trcommence)

    imonth = months.index(mcd.group(4))+1
    commencedate = datetime.datetime(int(mcd.group(5)), imonth, int(mcd.group(3)), int(mcd.group(1)), int(mcd.group(2)))
    data["commencedate"] = commencedate
    
    isin = []

    while True:
        tr3 = rows.pop(0)   # isin nonsense
        if len(tr3) == 3:
            c2 = tr3[1].text
            mc2= re.match("ISIN: (.*)$", c2)
            if mc2: 
                isin.append(mc2.group(1))
            else:
                assert c2 == u'\xa0'
            continue
        
        break

    data["isin"] = ",".join(isin)

    mofferor = re.match("OFFEROR: (.*)$", tr3[0][0].text)
    assert mofferor, lxml.etree.tostring(tr3)
    offerer = mofferor.group(1).strip()

    if rows:
        data["offerer"] = offerer
        tr4 = rows.pop(0)

        mcd = re.match("Offeror identified: (\d\d):(\d\d) (\d+)-(\w\w\w)-(\d\d\d\d)$", tr4[0].text)
        assert mcd, lxml.etree.tostring(tr4)
    
        imonth = months.index(mcd.group(4))+1
        identifieddate = datetime.datetime(int(mcd.group(5)), imonth, int(mcd.group(3)), int(mcd.group(1)), int(mcd.group(2)))
        data["identifieddate"] = identifieddate

    else:
        assert offerer == 'No named offeror'

    return data


# stock symbols can be obtained using this lookup
# iurl = "http://investegate.co.uk/Index.aspx?searchtype=5&words=%s" % isin
# iurl2 = "http://investegate.co.uk/Index.aspx?%s" % urllib.urlencode({ "searchtype":"2", "words":data.get("offeree")})
# txt = urllib.urlopen(url).read()
# c = re.findall('<a href="/Compdata\.aspx\?(.*)">', txt)

scrapedate = datetime.datetime.now()

def Main():
    root = lxml.html.parse(url).getroot()
    disctable= root.cssselect('div.disclosuretable')[0]
    tdisctable = lxml.html.tostring(disctable)

    try:
        prevdisctable = scraperwiki.sqlite.select("text from disctable order by scrapedate desc limit 1")[0]["text"]
        if tdisctable == prevdisctable:
            print "No change"
            return
    except scraperwiki.sqlite.NoSuchTableSqliteError:
        pass
    scraperwiki.sqlite.save(["scrapedate"], {"scrapedate":scrapedate, "text":tdisctable}, table_name="disctable")

    title = disctable[0].text_content()
    assert title == u'THE TAKEOVER PANEL \u2013 DISCLOSURE TABLE', title
    tabledate = disctable[1].text_content()

    # we should look for changes and record, handling the missing entries
    for t in disctable[2:]:
        assert t.tag == "table", lxml.html.tostring(t)
        if len(t) == 1 and t[0][0].text == 'Notes:':
            break
        if len(t) <= 2:
            v = [ lxml.etree.tostring(tr)  for tr in t ]
            #print "\n".join(v)
            continue
        data = ScrapeRecord(t)
        scraperwiki.sqlite.save(unique_keys=["offeree", "commencedate"], data=data)

# need to get the change date
        
Main()

                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime

url = "http://www.thetakeoverpanel.org.uk/disclosure/disclosure-table"

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def ScrapeRecord(table):
    data = { }
    rows = list(table)

    troffee = rows.pop(0)
    mofferee = re.match("OFFEREE: (.*)$", troffee[0][0].text)
    assert mofferee, lxml.etree.tostring(troffee)
    data["offeree"] = mofferee.group(1).strip()
    
    trcommence = rows.pop(0)
    mcd = re.match("Offer period commenced: (\d\d):(\d\d) (\d+)-(\w\w\w)-(\d\d\d\d)$", trcommence[0].text)
    assert mcd, lxml.etree.tostring(trcommence)

    imonth = months.index(mcd.group(4))+1
    commencedate = datetime.datetime(int(mcd.group(5)), imonth, int(mcd.group(3)), int(mcd.group(1)), int(mcd.group(2)))
    data["commencedate"] = commencedate
    
    isin = []

    while True:
        tr3 = rows.pop(0)   # isin nonsense
        if len(tr3) == 3:
            c2 = tr3[1].text
            mc2= re.match("ISIN: (.*)$", c2)
            if mc2: 
                isin.append(mc2.group(1))
            else:
                assert c2 == u'\xa0'
            continue
        
        break

    data["isin"] = ",".join(isin)

    mofferor = re.match("OFFEROR: (.*)$", tr3[0][0].text)
    assert mofferor, lxml.etree.tostring(tr3)
    offerer = mofferor.group(1).strip()

    if rows:
        data["offerer"] = offerer
        tr4 = rows.pop(0)

        mcd = re.match("Offeror identified: (\d\d):(\d\d) (\d+)-(\w\w\w)-(\d\d\d\d)$", tr4[0].text)
        assert mcd, lxml.etree.tostring(tr4)
    
        imonth = months.index(mcd.group(4))+1
        identifieddate = datetime.datetime(int(mcd.group(5)), imonth, int(mcd.group(3)), int(mcd.group(1)), int(mcd.group(2)))
        data["identifieddate"] = identifieddate

    else:
        assert offerer == 'No named offeror'

    return data


# stock symbols can be obtained using this lookup
# iurl = "http://investegate.co.uk/Index.aspx?searchtype=5&words=%s" % isin
# iurl2 = "http://investegate.co.uk/Index.aspx?%s" % urllib.urlencode({ "searchtype":"2", "words":data.get("offeree")})
# txt = urllib.urlopen(url).read()
# c = re.findall('<a href="/Compdata\.aspx\?(.*)">', txt)

scrapedate = datetime.datetime.now()

def Main():
    root = lxml.html.parse(url).getroot()
    disctable= root.cssselect('div.disclosuretable')[0]
    tdisctable = lxml.html.tostring(disctable)

    try:
        prevdisctable = scraperwiki.sqlite.select("text from disctable order by scrapedate desc limit 1")[0]["text"]
        if tdisctable == prevdisctable:
            print "No change"
            return
    except scraperwiki.sqlite.NoSuchTableSqliteError:
        pass
    scraperwiki.sqlite.save(["scrapedate"], {"scrapedate":scrapedate, "text":tdisctable}, table_name="disctable")

    title = disctable[0].text_content()
    assert title == u'THE TAKEOVER PANEL \u2013 DISCLOSURE TABLE', title
    tabledate = disctable[1].text_content()

    # we should look for changes and record, handling the missing entries
    for t in disctable[2:]:
        assert t.tag == "table", lxml.html.tostring(t)
        if len(t) == 1 and t[0][0].text == 'Notes:':
            break
        if len(t) <= 2:
            v = [ lxml.etree.tostring(tr)  for tr in t ]
            #print "\n".join(v)
            continue
        data = ScrapeRecord(t)
        scraperwiki.sqlite.save(unique_keys=["offeree", "commencedate"], data=data)

# need to get the change date
        
Main()

                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import datetime

url = "http://www.thetakeoverpanel.org.uk/disclosure/disclosure-table"

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def ScrapeRecord(table):
    data = { }
    rows = list(table)

    troffee = rows.pop(0)
    mofferee = re.match("OFFEREE: (.*)$", troffee[0][0].text)
    assert mofferee, lxml.etree.tostring(troffee)
    data["offeree"] = mofferee.group(1).strip()
    
    trcommence = rows.pop(0)
    mcd = re.match("Offer period commenced: (\d\d):(\d\d) (\d+)-(\w\w\w)-(\d\d\d\d)$", trcommence[0].text)
    assert mcd, lxml.etree.tostring(trcommence)

    imonth = months.index(mcd.group(4))+1
    commencedate = datetime.datetime(int(mcd.group(5)), imonth, int(mcd.group(3)), int(mcd.group(1)), int(mcd.group(2)))
    data["commencedate"] = commencedate
    
    isin = []

    while True:
        tr3 = rows.pop(0)   # isin nonsense
        if len(tr3) == 3:
            c2 = tr3[1].text
            mc2= re.match("ISIN: (.*)$", c2)
            if mc2: 
                isin.append(mc2.group(1))
            else:
                assert c2 == u'\xa0'
            continue
        
        break

    data["isin"] = ",".join(isin)

    mofferor = re.match("OFFEROR: (.*)$", tr3[0][0].text)
    assert mofferor, lxml.etree.tostring(tr3)
    offerer = mofferor.group(1).strip()

    if rows:
        data["offerer"] = offerer
        tr4 = rows.pop(0)

        mcd = re.match("Offeror identified: (\d\d):(\d\d) (\d+)-(\w\w\w)-(\d\d\d\d)$", tr4[0].text)
        assert mcd, lxml.etree.tostring(tr4)
    
        imonth = months.index(mcd.group(4))+1
        identifieddate = datetime.datetime(int(mcd.group(5)), imonth, int(mcd.group(3)), int(mcd.group(1)), int(mcd.group(2)))
        data["identifieddate"] = identifieddate

    else:
        assert offerer == 'No named offeror'

    return data


# stock symbols can be obtained using this lookup
# iurl = "http://investegate.co.uk/Index.aspx?searchtype=5&words=%s" % isin
# iurl2 = "http://investegate.co.uk/Index.aspx?%s" % urllib.urlencode({ "searchtype":"2", "words":data.get("offeree")})
# txt = urllib.urlopen(url).read()
# c = re.findall('<a href="/Compdata\.aspx\?(.*)">', txt)

scrapedate = datetime.datetime.now()

def Main():
    root = lxml.html.parse(url).getroot()
    disctable= root.cssselect('div.disclosuretable')[0]
    tdisctable = lxml.html.tostring(disctable)

    try:
        prevdisctable = scraperwiki.sqlite.select("text from disctable order by scrapedate desc limit 1")[0]["text"]
        if tdisctable == prevdisctable:
            print "No change"
            return
    except scraperwiki.sqlite.NoSuchTableSqliteError:
        pass
    scraperwiki.sqlite.save(["scrapedate"], {"scrapedate":scrapedate, "text":tdisctable}, table_name="disctable")

    title = disctable[0].text_content()
    assert title == u'THE TAKEOVER PANEL \u2013 DISCLOSURE TABLE', title
    tabledate = disctable[1].text_content()

    # we should look for changes and record, handling the missing entries
    for t in disctable[2:]:
        assert t.tag == "table", lxml.html.tostring(t)
        if len(t) == 1 and t[0][0].text == 'Notes:':
            break
        if len(t) <= 2:
            v = [ lxml.etree.tostring(tr)  for tr in t ]
            #print "\n".join(v)
            continue
        data = ScrapeRecord(t)
        scraperwiki.sqlite.save(unique_keys=["offeree", "commencedate"], data=data)

# need to get the change date
        
Main()

                        

