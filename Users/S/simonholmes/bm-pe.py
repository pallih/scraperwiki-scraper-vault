###############################################################################
# Pub explorer scraper
# http://www.pub-explorer.com/sitemap.htm
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def getDetails(soup):
    if soup.find("td", {"bgcolor":"#EBE0B1"}) > -1:
        thisname = soup.findAll("td", {"bgcolor":"#EBE0B1"})[1].find("p").text
        pgstyle = "beige"
    else:
        thisname = soup.find("td", {"bgcolor":"#990033"}).find("p").text
        pgstyle = "red"
    print "Getting details for " + thisname
    record = {}
    if pgstyle == "beige":
        contenttbls = soup.findAll("table", { "width" : "98%" })
    else:
        contenttbls = soup.findAll("table", { "width" : "750" })
    adr = ""
    mgr = ""
    contact = ""
    website = ""
    email = ""
    tel = ""
    contacttd = 0
    adrcontent = ""
    thisID = ""
    for table in contenttbls:
        tdi = 0        
        content = table.findAll("td")
        if len(content) > 5:
            for td in content:
                #print str(tdi) 
                #print td
                if td.text.find("GENERAL MANAGER") > -1:
                    #print "mgr at " + str(tdi+1)
                    mgr = content[tdi+1].text
                    mgr = mgr[:mgr.find(".")]
                elif td.text.find("CONTACT US") > -1:
                    contacttd = tdi+1
                    contact = content[tdi+1].text 
                    adrcontent = content[tdi+1]
                elif td.text.find("ADDRESS") > -1:
                    adr = content[tdi+1].text
                    if adr.find("Tel.") > -1:
                        contacttd = tdi+1
                        adrcontent = content[tdi+1]
                        contact = adr[adr.find("Tel."):]
                        adr = adr[:adr.find("Tel.")]
                elif td.text.find("WEBSITE") > -1:
                    if content[tdi+1].find("a") > -1:
                        if content[tdi+1].find("a","href") > -1:
                            website = content[tdi+1].find("a")["href"]
                elif td.text.find("EXPLORER") > -1 and td.text.find("REFERENCE") > -1 :
                    thisID = content[tdi+1].text
                tdi = tdi + 1
    if adr <> "":
        if contact <> "":
            if contact.find("&nbsp;") > -1:
                tel = contact[contact.find(". ")+2:contact.find("&nbsp;")].strip()
            else:
                tel = contact[contact.find("Tel")+4:].strip()
            if adrcontent.find("a") > -1:
                if adrcontent.find("a").text.find("@") > -1:
                    email = adrcontent.find("a").text
        address = adr.split(",")
        adrlast = len(address)
        #print "adrlast = " + str(adrlast)
        add1a = address[0].strip()
        adrtmp = address[adrlast-1].strip()
        if adrtmp.find("&nbsp;") > -1:
            add3 = adrtmp[adrtmp.find("&nbsp;")+6:].strip() # postcode
            add2b = adrtmp[:adrtmp.find("&nbsp;")].strip() # locality
        else:
            add3 = adrtmp.strip() # postcode
            add2b = address[adrlast-2].strip()
        #print add2b[:add2b.find("&nbsp;")]
        if add3.find(".") > -1:
            add3 = add3[:add3.find(".")]
        add2a = ""
        if adrlast > 2:
            add1b = address[1].strip()
            if add1b.find("&nbsp;") == 0:
                add1b = add1b[add1b.find("&nbsp;")+6:].strip()
            if adrlast > 3:
                add2a = address[adrlast-2].strip() # dependent locality
                if add2a.find("&nbsp;") == 0:
                    add2a = add2a[add2a.find("&nbsp;")+6:].strip()
        else:
            add1b = ""
        #print "add3 = " + add3
        if add3.find("&nbsp") > -1:
            add3 = add3[:add3.find("&nbsp")]
        if add2b.find("&nbsp") > -1:
            add2b = add2b[:add2b.find("&nbsp")]
        from datetime import datetime
        from datetime import datetime
        if thisID == "":
            thisID = thisname + ' '.join(add3.split())
        record['ThisID'] = thisID[:thisID.find(".")]
        record['BusinessID'] = ""
        record['ReferrerID'] = 2
        record['RepID'] = ""
        record['BusinessChainID'] = 99
        record['CompanyName'] = ' '.join(thisname.split())
        record['BuildingName'] = ""
        record['ThoroughFare'] = ' '.join(add1a.split())
        record['ThoroughFare2'] = ' '.join(add1b.split())
        record['DependentLocality'] = ' '.join(add2a.split())
        record['Locality'] = ' '.join(add2b.split())
        record['PostalCode'] = ' '.join(add3.split())
        record['Country'] = "United Kingdom"
        record['Lat'] = ""
        record['Lng'] = ""
        record['Verified'] = ""
        record['BusinessTypeID'] = 2
        record['BusinessTypeOther'] = ""
        record['BusinessSubCats'] = ",8,"
        record['BusinessSubCatOther'] = ""
        record['ChangingID'] = 1
        record['NursingID'] = 3
        record['Website'] = website
        record['ContactName'] = ' '.join(mgr.split())
        record['ContactPosition'] = "General Manager"
        record['Telephone'] = ' '.join(tel.split())
        record['Email'] = email
        record['Fax'] = ""
        record['LastModified'] = datetime.now()
        record['CreationDate'] = datetime.now()
        record['UsagePolicyID'] = 1
        record['AddressStatusID'] = 1
        record['latlngStatusID'] = 2
        scraperwiki.datastore.save(["ThisID"], record)

def openPage(pageURL):
    locallisthtml = scraperwiki.scrape(pageURL)
    localsoup = BeautifulSoup(locallisthtml)
    trs = localsoup.find("table",{"width":"770"}).findAll("tr")
    thisi = 0
    for tr in trs:
        thisi = thisi + 1
        tds = tr.findAll("td")
        if len(tds)>1:
            thisa = tds[1].find("a")['href']
            if thisa.find("../") > - 1:
                starting_url = siteurl + thisa[3:]
            else:
                starting_url = siteurl + localfolder + "/" + thisa
            print str(thisi) + " " + starting_url
            if starting_url <> "http://www.pub-explorer.com/olpg/the-blackswan/ashover/index.htm" and starting_url.find("/http") == -1:
                html = scraperwiki.scrape(starting_url)
                soup = BeautifulSoup(html)
                ps = soup.findAll("p",{"align":"RIGHT"})
                for p in ps:
                    ptext = p.text
                    #print ptext
                    if ptext.find("Baby Chang") > - 1 or ptext.find("baby chang") > - 1:
                        if starting_url <> "http://www.pub-explorer.com/notts/pub/hutt.htm":
                            getDetails(soup)
                        break
            

siteurl = "http://www.pub-explorer.com/"
listurl = 'http://www.pub-explorer.com/sitemap.htm'
listhtml = scraperwiki.scrape(listurl)
listsoup = BeautifulSoup(listhtml)
tabs = listsoup.findAll("table",{"width" : "750"})
tmpi = 0
for table in tabs:
    if tmpi == 0 or tmpi == 3:
        #not this table
        print "Ignoring table"
    else:
        print "Reading table " + str(tmpi)
        links = table.findAll("a")
        ilink = 0
        for link in links:
            if (tmpi == 1 and ilink > 34) or (tmpi == 2 and ilink > 8):
                href = link["href"]
                if href == "index.html" or href == "search.htm" or href == "contacts.htm" or href == "themedpubs/themedpubindex.htm" or href == "pubguide.htm" or href == "realale/camra.htm" or href == "about.htm" or href == "wsussex/westsussexpubs.htm":
                    #ignore it
                    print "ignoring " + href 
                else:
                    #get to it
                    localfolder = href[:href.find("/")]
                    locallisturl = siteurl + href 
                    print "Going to " + localfolder + " at " + locallisturl
                    openPage(locallisturl)
            ilink = ilink + 1
    tmpi = tmpi + 1
openPage("http://www.pub-explorer.com/wyorks/pubssofar.htm")

###############################################################################
# Pub explorer scraper
# http://www.pub-explorer.com/sitemap.htm
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup

def getDetails(soup):
    if soup.find("td", {"bgcolor":"#EBE0B1"}) > -1:
        thisname = soup.findAll("td", {"bgcolor":"#EBE0B1"})[1].find("p").text
        pgstyle = "beige"
    else:
        thisname = soup.find("td", {"bgcolor":"#990033"}).find("p").text
        pgstyle = "red"
    print "Getting details for " + thisname
    record = {}
    if pgstyle == "beige":
        contenttbls = soup.findAll("table", { "width" : "98%" })
    else:
        contenttbls = soup.findAll("table", { "width" : "750" })
    adr = ""
    mgr = ""
    contact = ""
    website = ""
    email = ""
    tel = ""
    contacttd = 0
    adrcontent = ""
    thisID = ""
    for table in contenttbls:
        tdi = 0        
        content = table.findAll("td")
        if len(content) > 5:
            for td in content:
                #print str(tdi) 
                #print td
                if td.text.find("GENERAL MANAGER") > -1:
                    #print "mgr at " + str(tdi+1)
                    mgr = content[tdi+1].text
                    mgr = mgr[:mgr.find(".")]
                elif td.text.find("CONTACT US") > -1:
                    contacttd = tdi+1
                    contact = content[tdi+1].text 
                    adrcontent = content[tdi+1]
                elif td.text.find("ADDRESS") > -1:
                    adr = content[tdi+1].text
                    if adr.find("Tel.") > -1:
                        contacttd = tdi+1
                        adrcontent = content[tdi+1]
                        contact = adr[adr.find("Tel."):]
                        adr = adr[:adr.find("Tel.")]
                elif td.text.find("WEBSITE") > -1:
                    if content[tdi+1].find("a") > -1:
                        if content[tdi+1].find("a","href") > -1:
                            website = content[tdi+1].find("a")["href"]
                elif td.text.find("EXPLORER") > -1 and td.text.find("REFERENCE") > -1 :
                    thisID = content[tdi+1].text
                tdi = tdi + 1
    if adr <> "":
        if contact <> "":
            if contact.find("&nbsp;") > -1:
                tel = contact[contact.find(". ")+2:contact.find("&nbsp;")].strip()
            else:
                tel = contact[contact.find("Tel")+4:].strip()
            if adrcontent.find("a") > -1:
                if adrcontent.find("a").text.find("@") > -1:
                    email = adrcontent.find("a").text
        address = adr.split(",")
        adrlast = len(address)
        #print "adrlast = " + str(adrlast)
        add1a = address[0].strip()
        adrtmp = address[adrlast-1].strip()
        if adrtmp.find("&nbsp;") > -1:
            add3 = adrtmp[adrtmp.find("&nbsp;")+6:].strip() # postcode
            add2b = adrtmp[:adrtmp.find("&nbsp;")].strip() # locality
        else:
            add3 = adrtmp.strip() # postcode
            add2b = address[adrlast-2].strip()
        #print add2b[:add2b.find("&nbsp;")]
        if add3.find(".") > -1:
            add3 = add3[:add3.find(".")]
        add2a = ""
        if adrlast > 2:
            add1b = address[1].strip()
            if add1b.find("&nbsp;") == 0:
                add1b = add1b[add1b.find("&nbsp;")+6:].strip()
            if adrlast > 3:
                add2a = address[adrlast-2].strip() # dependent locality
                if add2a.find("&nbsp;") == 0:
                    add2a = add2a[add2a.find("&nbsp;")+6:].strip()
        else:
            add1b = ""
        #print "add3 = " + add3
        if add3.find("&nbsp") > -1:
            add3 = add3[:add3.find("&nbsp")]
        if add2b.find("&nbsp") > -1:
            add2b = add2b[:add2b.find("&nbsp")]
        from datetime import datetime
        from datetime import datetime
        if thisID == "":
            thisID = thisname + ' '.join(add3.split())
        record['ThisID'] = thisID[:thisID.find(".")]
        record['BusinessID'] = ""
        record['ReferrerID'] = 2
        record['RepID'] = ""
        record['BusinessChainID'] = 99
        record['CompanyName'] = ' '.join(thisname.split())
        record['BuildingName'] = ""
        record['ThoroughFare'] = ' '.join(add1a.split())
        record['ThoroughFare2'] = ' '.join(add1b.split())
        record['DependentLocality'] = ' '.join(add2a.split())
        record['Locality'] = ' '.join(add2b.split())
        record['PostalCode'] = ' '.join(add3.split())
        record['Country'] = "United Kingdom"
        record['Lat'] = ""
        record['Lng'] = ""
        record['Verified'] = ""
        record['BusinessTypeID'] = 2
        record['BusinessTypeOther'] = ""
        record['BusinessSubCats'] = ",8,"
        record['BusinessSubCatOther'] = ""
        record['ChangingID'] = 1
        record['NursingID'] = 3
        record['Website'] = website
        record['ContactName'] = ' '.join(mgr.split())
        record['ContactPosition'] = "General Manager"
        record['Telephone'] = ' '.join(tel.split())
        record['Email'] = email
        record['Fax'] = ""
        record['LastModified'] = datetime.now()
        record['CreationDate'] = datetime.now()
        record['UsagePolicyID'] = 1
        record['AddressStatusID'] = 1
        record['latlngStatusID'] = 2
        scraperwiki.datastore.save(["ThisID"], record)

def openPage(pageURL):
    locallisthtml = scraperwiki.scrape(pageURL)
    localsoup = BeautifulSoup(locallisthtml)
    trs = localsoup.find("table",{"width":"770"}).findAll("tr")
    thisi = 0
    for tr in trs:
        thisi = thisi + 1
        tds = tr.findAll("td")
        if len(tds)>1:
            thisa = tds[1].find("a")['href']
            if thisa.find("../") > - 1:
                starting_url = siteurl + thisa[3:]
            else:
                starting_url = siteurl + localfolder + "/" + thisa
            print str(thisi) + " " + starting_url
            if starting_url <> "http://www.pub-explorer.com/olpg/the-blackswan/ashover/index.htm" and starting_url.find("/http") == -1:
                html = scraperwiki.scrape(starting_url)
                soup = BeautifulSoup(html)
                ps = soup.findAll("p",{"align":"RIGHT"})
                for p in ps:
                    ptext = p.text
                    #print ptext
                    if ptext.find("Baby Chang") > - 1 or ptext.find("baby chang") > - 1:
                        if starting_url <> "http://www.pub-explorer.com/notts/pub/hutt.htm":
                            getDetails(soup)
                        break
            

siteurl = "http://www.pub-explorer.com/"
listurl = 'http://www.pub-explorer.com/sitemap.htm'
listhtml = scraperwiki.scrape(listurl)
listsoup = BeautifulSoup(listhtml)
tabs = listsoup.findAll("table",{"width" : "750"})
tmpi = 0
for table in tabs:
    if tmpi == 0 or tmpi == 3:
        #not this table
        print "Ignoring table"
    else:
        print "Reading table " + str(tmpi)
        links = table.findAll("a")
        ilink = 0
        for link in links:
            if (tmpi == 1 and ilink > 34) or (tmpi == 2 and ilink > 8):
                href = link["href"]
                if href == "index.html" or href == "search.htm" or href == "contacts.htm" or href == "themedpubs/themedpubindex.htm" or href == "pubguide.htm" or href == "realale/camra.htm" or href == "about.htm" or href == "wsussex/westsussexpubs.htm":
                    #ignore it
                    print "ignoring " + href 
                else:
                    #get to it
                    localfolder = href[:href.find("/")]
                    locallisturl = siteurl + href 
                    print "Going to " + localfolder + " at " + locallisturl
                    openPage(locallisturl)
            ilink = ilink + 1
    tmpi = tmpi + 1
openPage("http://www.pub-explorer.com/wyorks/pubssofar.htm")

