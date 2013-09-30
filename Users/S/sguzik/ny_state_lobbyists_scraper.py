import scraperwiki
import mechanize
import lxml.html
import urllib, urlparse
import re, json


url = "https://apps.jcope.ny.gov/lrr/Menu_reports_public.aspx"

year = "2011"

cj = mechanize.CookieJar()
br = mechanize.Browser()
br1 = mechanize.Browser()


def Main():
    maxgridbutton = SetupBrowsers(year)
    vmaxgridbutton = "maxgridbutton_%s" % year
    vcurrgridbutton = "currgridbutton_%s" % year
    prevmaxgridbutton = scraperwiki.sqlite.get_var(vmaxgridbutton, 0)
    if maxgridbutton != prevmaxgridbutton:
        print "New %s vmaxgridbutton=%d  previous=%d" % (vmaxgridbutton, maxgridbutton, prevmaxgridbutton)
        scraperwiki.sqlite.save_var(vmaxgridbutton, maxgridbutton)
    
    currgridbutton = scraperwiki.sqlite.get_var(vcurrgridbutton, 0)  # starts at 0 
    while currgridbutton <= maxgridbutton:   
        GetLobbyGrid(currgridbutton, year)
        currgridbutton += 1
        scraperwiki.sqlite.save_var(vcurrgridbutton, currgridbutton)


def SetupBrowsers(year):
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_cookiejar(cj)
    br1.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br1.set_cookiejar(cj)

    # get to the form (with its cookies)
    response = br.open(url)
    for a in br.links():
        if a.text == 'Click here to execute Client Query':
            link = a
    response = br.follow_link(link)
    br.select_form("form1")
    
    # fill in the form
    br["ddlQYear"] = [year]
    response = br.submit()
    htmlI = response.read()
    #print htmlI
    #ParseHtable(htmlI)

    br.select_form("form1")
    br.set_all_readonly(False)
    return max(map(int, re.findall("DisplayGrid_0_14_(\d+)\$ViewBTN", htmlI)))


def GetLobbyGrid(d, year):
    dt = 'DisplayGrid_0_14_%d$ViewBTN' % d
    br["__EVENTTARGET"] = dt
    br["__EVENTARGUMENT"] = ''
    br.find_control("btnSearch").disabled = True
    #print br.form
    request = br.click()
    #print request
    response1 = br1.open(request)
    
    # find the window open hidden in the script
    html1 = response1.read()
    root1 = lxml.html.fromstring(html1)
    for s in root1.cssselect("script"):
        if s.text:
            ms = re.match("var myWin;myWin=window.open\('(LB_HtmlCSR.aspx\?.*?)',", s.text)
            if ms:
                loblink = ms.group(1)
    uloblink = urlparse.urljoin(br1.geturl(), loblink)
    response2 = br1.open(uloblink)
    html2 = response2.read()
    #print "LobbyGrid", dt, len(html2)
    scraperwiki.sqlite.save(["dt", "year"], {"dt":dt, "year":year, "html2":html2}, "indivlobb")

Main()


def ParseHtable(htable):
    mhtable = re.search("(?s)DisplayGrid.Data =\s*(\[\[.*?\]\])", htable)
    jtable = mhtable.group(1)
    jtable = jtable.replace("\\'", ";;;APOS;;;")
    jtable = jtable.replace("'", '"')
    jtable = jtable.replace(";;;APOS;;;", "'")
    jtable = jtable.replace(",]", "]")
    jdata = json.loads(jtable)
    headers = ["n1", "year", "f1", "addr1", "addr2", "f2", "addre3", "city", "state", "f3", "month", "f4", "monthrange", "f5"]
    ldata = [ ]
    for jt in jdata:
        data = dict(zip(headers, jt))
        ldata.append(data)
    scraperwiki.sqlite.save([], ldata)
import scraperwiki
import mechanize
import lxml.html
import urllib, urlparse
import re, json


url = "https://apps.jcope.ny.gov/lrr/Menu_reports_public.aspx"

year = "2011"

cj = mechanize.CookieJar()
br = mechanize.Browser()
br1 = mechanize.Browser()


def Main():
    maxgridbutton = SetupBrowsers(year)
    vmaxgridbutton = "maxgridbutton_%s" % year
    vcurrgridbutton = "currgridbutton_%s" % year
    prevmaxgridbutton = scraperwiki.sqlite.get_var(vmaxgridbutton, 0)
    if maxgridbutton != prevmaxgridbutton:
        print "New %s vmaxgridbutton=%d  previous=%d" % (vmaxgridbutton, maxgridbutton, prevmaxgridbutton)
        scraperwiki.sqlite.save_var(vmaxgridbutton, maxgridbutton)
    
    currgridbutton = scraperwiki.sqlite.get_var(vcurrgridbutton, 0)  # starts at 0 
    while currgridbutton <= maxgridbutton:   
        GetLobbyGrid(currgridbutton, year)
        currgridbutton += 1
        scraperwiki.sqlite.save_var(vcurrgridbutton, currgridbutton)


def SetupBrowsers(year):
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_cookiejar(cj)
    br1.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br1.set_cookiejar(cj)

    # get to the form (with its cookies)
    response = br.open(url)
    for a in br.links():
        if a.text == 'Click here to execute Client Query':
            link = a
    response = br.follow_link(link)
    br.select_form("form1")
    
    # fill in the form
    br["ddlQYear"] = [year]
    response = br.submit()
    htmlI = response.read()
    #print htmlI
    #ParseHtable(htmlI)

    br.select_form("form1")
    br.set_all_readonly(False)
    return max(map(int, re.findall("DisplayGrid_0_14_(\d+)\$ViewBTN", htmlI)))


def GetLobbyGrid(d, year):
    dt = 'DisplayGrid_0_14_%d$ViewBTN' % d
    br["__EVENTTARGET"] = dt
    br["__EVENTARGUMENT"] = ''
    br.find_control("btnSearch").disabled = True
    #print br.form
    request = br.click()
    #print request
    response1 = br1.open(request)
    
    # find the window open hidden in the script
    html1 = response1.read()
    root1 = lxml.html.fromstring(html1)
    for s in root1.cssselect("script"):
        if s.text:
            ms = re.match("var myWin;myWin=window.open\('(LB_HtmlCSR.aspx\?.*?)',", s.text)
            if ms:
                loblink = ms.group(1)
    uloblink = urlparse.urljoin(br1.geturl(), loblink)
    response2 = br1.open(uloblink)
    html2 = response2.read()
    #print "LobbyGrid", dt, len(html2)
    scraperwiki.sqlite.save(["dt", "year"], {"dt":dt, "year":year, "html2":html2}, "indivlobb")

Main()


def ParseHtable(htable):
    mhtable = re.search("(?s)DisplayGrid.Data =\s*(\[\[.*?\]\])", htable)
    jtable = mhtable.group(1)
    jtable = jtable.replace("\\'", ";;;APOS;;;")
    jtable = jtable.replace("'", '"')
    jtable = jtable.replace(";;;APOS;;;", "'")
    jtable = jtable.replace(",]", "]")
    jdata = json.loads(jtable)
    headers = ["n1", "year", "f1", "addr1", "addr2", "f2", "addre3", "city", "state", "f3", "month", "f4", "monthrange", "f5"]
    ldata = [ ]
    for jt in jdata:
        data = dict(zip(headers, jt))
        ldata.append(data)
    scraperwiki.sqlite.save([], ldata)
