import scraperwiki
import lxml.html
import urllib
import urlparse
import datetime
import re

url = "http://www.publications.parliament.uk/pa/cm/cmregmem/110124/part1contents.htm"

urlmainindex = "http://www.publications.parliament.uk/pa/cm/cmregmem.htm"


def Main():
    mainindexroot = lxml.html.parse(urlmainindex).getroot()
    urlyears = [ urlparse.urljoin(urlmainindex, a.attrib.get("href"))  for a in mainindexroot.cssselect("div#maincontent a")  if re.search("Members.*?Interests", a.text or "") ]

    for urlyear in urlyears:
        yearindexroot = lxml.html.parse(urlyear).getroot()
        urlversions = [ urlparse.urljoin(urlyear, a.attrib.get("href"))  for a in yearindexroot.cssselect("div#maincontent a")  if re.search("\s*Part 1", a.text or "") ]
        for url in urlversions:
            ScrapeRegmemVersion(url)
            #break  # do only one

        break  # do only one


def ScrapeRegmemVersion(url):
    root = lxml.html.parse(url).getroot()
    paras = root.cssselect('#wrapper #content #content-small table td p')
    assert paras[2].attrib.get("class") == "atozLinks"
    ilimit = scraperwiki.sqlite.get_var(url, 2)
    for i, p in enumerate(paras):
        if i <= ilimit:
            continue
        a = p.cssselect("a")[0]
        print i, a.text
        if a.text == "Terms of Reference":
            continue
        mpurl = urlparse.urljoin(url, a.attrib.get("href"))
        ScrapeRegmemPage(mpurl)
        scraperwiki.sqlite.save_var(url, i)


def flatten(elem):
    result = [ unicode(elem.text or "") ]
    for x in elem:
        result.append(flatten(x))
    result.append(elem.tail or "")
    return "".join(result)

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def ScrapeRegmemPage(mpurl):
    mproot = lxml.html.parse(mpurl).getroot()
    h1date = mproot.cssselect("h1.mainTitle br")[0].tail
    
    mdate = re.match("\s*As at (\d+)[thstnd]+ (\w+) (\d\d\d\d)", h1date)
    assert mdate, h1date
    date = datetime.date(int(mdate.group(3)), months.index(mdate.group(2))+1, int(mdate.group(1)))
    
    dpn = mproot.cssselect('#content-small .prevNext')[0].getnext()
    lines = [ ]
    while dpn.tag != "div":
        if dpn.tag == "h2":
            mpname = dpn.text
        elif dpn.tag == "h3":
            lines.append("")
            lines.append("")
            lines.append("** "+flatten(dpn))
        elif dpn.tag == "p":
            if dpn.attrib.get("class") == "indent":
                pp = " "
            elif dpn.attrib.get("class") == "indent2":
                pp = "  "
            else:
                pp = ""
            lines.append(pp+re.sub("\n", " ", flatten(dpn)).strip())
        else:
            assert False, lxml.html.tostring(dpn)
        dpn = dpn.getnext()
    data = { "mpname":mpname, "date":date, "mpurl":mpurl, "content":"\n".join(lines) }
    #data["mpid"] = getmpid(mpname, data["date"])
    scraperwiki.sqlite.save(unique_keys=["mpname", "date"], data=data)


Main()

import scraperwiki
import lxml.html
import urllib
import urlparse
import datetime
import re

url = "http://www.publications.parliament.uk/pa/cm/cmregmem/110124/part1contents.htm"

urlmainindex = "http://www.publications.parliament.uk/pa/cm/cmregmem.htm"


def Main():
    mainindexroot = lxml.html.parse(urlmainindex).getroot()
    urlyears = [ urlparse.urljoin(urlmainindex, a.attrib.get("href"))  for a in mainindexroot.cssselect("div#maincontent a")  if re.search("Members.*?Interests", a.text or "") ]

    for urlyear in urlyears:
        yearindexroot = lxml.html.parse(urlyear).getroot()
        urlversions = [ urlparse.urljoin(urlyear, a.attrib.get("href"))  for a in yearindexroot.cssselect("div#maincontent a")  if re.search("\s*Part 1", a.text or "") ]
        for url in urlversions:
            ScrapeRegmemVersion(url)
            #break  # do only one

        break  # do only one


def ScrapeRegmemVersion(url):
    root = lxml.html.parse(url).getroot()
    paras = root.cssselect('#wrapper #content #content-small table td p')
    assert paras[2].attrib.get("class") == "atozLinks"
    ilimit = scraperwiki.sqlite.get_var(url, 2)
    for i, p in enumerate(paras):
        if i <= ilimit:
            continue
        a = p.cssselect("a")[0]
        print i, a.text
        if a.text == "Terms of Reference":
            continue
        mpurl = urlparse.urljoin(url, a.attrib.get("href"))
        ScrapeRegmemPage(mpurl)
        scraperwiki.sqlite.save_var(url, i)


def flatten(elem):
    result = [ unicode(elem.text or "") ]
    for x in elem:
        result.append(flatten(x))
    result.append(elem.tail or "")
    return "".join(result)

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def ScrapeRegmemPage(mpurl):
    mproot = lxml.html.parse(mpurl).getroot()
    h1date = mproot.cssselect("h1.mainTitle br")[0].tail
    
    mdate = re.match("\s*As at (\d+)[thstnd]+ (\w+) (\d\d\d\d)", h1date)
    assert mdate, h1date
    date = datetime.date(int(mdate.group(3)), months.index(mdate.group(2))+1, int(mdate.group(1)))
    
    dpn = mproot.cssselect('#content-small .prevNext')[0].getnext()
    lines = [ ]
    while dpn.tag != "div":
        if dpn.tag == "h2":
            mpname = dpn.text
        elif dpn.tag == "h3":
            lines.append("")
            lines.append("")
            lines.append("** "+flatten(dpn))
        elif dpn.tag == "p":
            if dpn.attrib.get("class") == "indent":
                pp = " "
            elif dpn.attrib.get("class") == "indent2":
                pp = "  "
            else:
                pp = ""
            lines.append(pp+re.sub("\n", " ", flatten(dpn)).strip())
        else:
            assert False, lxml.html.tostring(dpn)
        dpn = dpn.getnext()
    data = { "mpname":mpname, "date":date, "mpurl":mpurl, "content":"\n".join(lines) }
    #data["mpid"] = getmpid(mpname, data["date"])
    scraperwiki.sqlite.save(unique_keys=["mpname", "date"], data=data)


Main()

import scraperwiki
import lxml.html
import urllib
import urlparse
import datetime
import re

url = "http://www.publications.parliament.uk/pa/cm/cmregmem/110124/part1contents.htm"

urlmainindex = "http://www.publications.parliament.uk/pa/cm/cmregmem.htm"


def Main():
    mainindexroot = lxml.html.parse(urlmainindex).getroot()
    urlyears = [ urlparse.urljoin(urlmainindex, a.attrib.get("href"))  for a in mainindexroot.cssselect("div#maincontent a")  if re.search("Members.*?Interests", a.text or "") ]

    for urlyear in urlyears:
        yearindexroot = lxml.html.parse(urlyear).getroot()
        urlversions = [ urlparse.urljoin(urlyear, a.attrib.get("href"))  for a in yearindexroot.cssselect("div#maincontent a")  if re.search("\s*Part 1", a.text or "") ]
        for url in urlversions:
            ScrapeRegmemVersion(url)
            #break  # do only one

        break  # do only one


def ScrapeRegmemVersion(url):
    root = lxml.html.parse(url).getroot()
    paras = root.cssselect('#wrapper #content #content-small table td p')
    assert paras[2].attrib.get("class") == "atozLinks"
    ilimit = scraperwiki.sqlite.get_var(url, 2)
    for i, p in enumerate(paras):
        if i <= ilimit:
            continue
        a = p.cssselect("a")[0]
        print i, a.text
        if a.text == "Terms of Reference":
            continue
        mpurl = urlparse.urljoin(url, a.attrib.get("href"))
        ScrapeRegmemPage(mpurl)
        scraperwiki.sqlite.save_var(url, i)


def flatten(elem):
    result = [ unicode(elem.text or "") ]
    for x in elem:
        result.append(flatten(x))
    result.append(elem.tail or "")
    return "".join(result)

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def ScrapeRegmemPage(mpurl):
    mproot = lxml.html.parse(mpurl).getroot()
    h1date = mproot.cssselect("h1.mainTitle br")[0].tail
    
    mdate = re.match("\s*As at (\d+)[thstnd]+ (\w+) (\d\d\d\d)", h1date)
    assert mdate, h1date
    date = datetime.date(int(mdate.group(3)), months.index(mdate.group(2))+1, int(mdate.group(1)))
    
    dpn = mproot.cssselect('#content-small .prevNext')[0].getnext()
    lines = [ ]
    while dpn.tag != "div":
        if dpn.tag == "h2":
            mpname = dpn.text
        elif dpn.tag == "h3":
            lines.append("")
            lines.append("")
            lines.append("** "+flatten(dpn))
        elif dpn.tag == "p":
            if dpn.attrib.get("class") == "indent":
                pp = " "
            elif dpn.attrib.get("class") == "indent2":
                pp = "  "
            else:
                pp = ""
            lines.append(pp+re.sub("\n", " ", flatten(dpn)).strip())
        else:
            assert False, lxml.html.tostring(dpn)
        dpn = dpn.getnext()
    data = { "mpname":mpname, "date":date, "mpurl":mpurl, "content":"\n".join(lines) }
    #data["mpid"] = getmpid(mpname, data["date"])
    scraperwiki.sqlite.save(unique_keys=["mpname", "date"], data=data)


Main()

import scraperwiki
import lxml.html
import urllib
import urlparse
import datetime
import re

url = "http://www.publications.parliament.uk/pa/cm/cmregmem/110124/part1contents.htm"

urlmainindex = "http://www.publications.parliament.uk/pa/cm/cmregmem.htm"


def Main():
    mainindexroot = lxml.html.parse(urlmainindex).getroot()
    urlyears = [ urlparse.urljoin(urlmainindex, a.attrib.get("href"))  for a in mainindexroot.cssselect("div#maincontent a")  if re.search("Members.*?Interests", a.text or "") ]

    for urlyear in urlyears:
        yearindexroot = lxml.html.parse(urlyear).getroot()
        urlversions = [ urlparse.urljoin(urlyear, a.attrib.get("href"))  for a in yearindexroot.cssselect("div#maincontent a")  if re.search("\s*Part 1", a.text or "") ]
        for url in urlversions:
            ScrapeRegmemVersion(url)
            #break  # do only one

        break  # do only one


def ScrapeRegmemVersion(url):
    root = lxml.html.parse(url).getroot()
    paras = root.cssselect('#wrapper #content #content-small table td p')
    assert paras[2].attrib.get("class") == "atozLinks"
    ilimit = scraperwiki.sqlite.get_var(url, 2)
    for i, p in enumerate(paras):
        if i <= ilimit:
            continue
        a = p.cssselect("a")[0]
        print i, a.text
        if a.text == "Terms of Reference":
            continue
        mpurl = urlparse.urljoin(url, a.attrib.get("href"))
        ScrapeRegmemPage(mpurl)
        scraperwiki.sqlite.save_var(url, i)


def flatten(elem):
    result = [ unicode(elem.text or "") ]
    for x in elem:
        result.append(flatten(x))
    result.append(elem.tail or "")
    return "".join(result)

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def ScrapeRegmemPage(mpurl):
    mproot = lxml.html.parse(mpurl).getroot()
    h1date = mproot.cssselect("h1.mainTitle br")[0].tail
    
    mdate = re.match("\s*As at (\d+)[thstnd]+ (\w+) (\d\d\d\d)", h1date)
    assert mdate, h1date
    date = datetime.date(int(mdate.group(3)), months.index(mdate.group(2))+1, int(mdate.group(1)))
    
    dpn = mproot.cssselect('#content-small .prevNext')[0].getnext()
    lines = [ ]
    while dpn.tag != "div":
        if dpn.tag == "h2":
            mpname = dpn.text
        elif dpn.tag == "h3":
            lines.append("")
            lines.append("")
            lines.append("** "+flatten(dpn))
        elif dpn.tag == "p":
            if dpn.attrib.get("class") == "indent":
                pp = " "
            elif dpn.attrib.get("class") == "indent2":
                pp = "  "
            else:
                pp = ""
            lines.append(pp+re.sub("\n", " ", flatten(dpn)).strip())
        else:
            assert False, lxml.html.tostring(dpn)
        dpn = dpn.getnext()
    data = { "mpname":mpname, "date":date, "mpurl":mpurl, "content":"\n".join(lines) }
    #data["mpid"] = getmpid(mpname, data["date"])
    scraperwiki.sqlite.save(unique_keys=["mpname", "date"], data=data)


Main()

import scraperwiki
import lxml.html
import urllib
import urlparse
import datetime
import re

url = "http://www.publications.parliament.uk/pa/cm/cmregmem/110124/part1contents.htm"

urlmainindex = "http://www.publications.parliament.uk/pa/cm/cmregmem.htm"


def Main():
    mainindexroot = lxml.html.parse(urlmainindex).getroot()
    urlyears = [ urlparse.urljoin(urlmainindex, a.attrib.get("href"))  for a in mainindexroot.cssselect("div#maincontent a")  if re.search("Members.*?Interests", a.text or "") ]

    for urlyear in urlyears:
        yearindexroot = lxml.html.parse(urlyear).getroot()
        urlversions = [ urlparse.urljoin(urlyear, a.attrib.get("href"))  for a in yearindexroot.cssselect("div#maincontent a")  if re.search("\s*Part 1", a.text or "") ]
        for url in urlversions:
            ScrapeRegmemVersion(url)
            #break  # do only one

        break  # do only one


def ScrapeRegmemVersion(url):
    root = lxml.html.parse(url).getroot()
    paras = root.cssselect('#wrapper #content #content-small table td p')
    assert paras[2].attrib.get("class") == "atozLinks"
    ilimit = scraperwiki.sqlite.get_var(url, 2)
    for i, p in enumerate(paras):
        if i <= ilimit:
            continue
        a = p.cssselect("a")[0]
        print i, a.text
        if a.text == "Terms of Reference":
            continue
        mpurl = urlparse.urljoin(url, a.attrib.get("href"))
        ScrapeRegmemPage(mpurl)
        scraperwiki.sqlite.save_var(url, i)


def flatten(elem):
    result = [ unicode(elem.text or "") ]
    for x in elem:
        result.append(flatten(x))
    result.append(elem.tail or "")
    return "".join(result)

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def ScrapeRegmemPage(mpurl):
    mproot = lxml.html.parse(mpurl).getroot()
    h1date = mproot.cssselect("h1.mainTitle br")[0].tail
    
    mdate = re.match("\s*As at (\d+)[thstnd]+ (\w+) (\d\d\d\d)", h1date)
    assert mdate, h1date
    date = datetime.date(int(mdate.group(3)), months.index(mdate.group(2))+1, int(mdate.group(1)))
    
    dpn = mproot.cssselect('#content-small .prevNext')[0].getnext()
    lines = [ ]
    while dpn.tag != "div":
        if dpn.tag == "h2":
            mpname = dpn.text
        elif dpn.tag == "h3":
            lines.append("")
            lines.append("")
            lines.append("** "+flatten(dpn))
        elif dpn.tag == "p":
            if dpn.attrib.get("class") == "indent":
                pp = " "
            elif dpn.attrib.get("class") == "indent2":
                pp = "  "
            else:
                pp = ""
            lines.append(pp+re.sub("\n", " ", flatten(dpn)).strip())
        else:
            assert False, lxml.html.tostring(dpn)
        dpn = dpn.getnext()
    data = { "mpname":mpname, "date":date, "mpurl":mpurl, "content":"\n".join(lines) }
    #data["mpid"] = getmpid(mpname, data["date"])
    scraperwiki.sqlite.save(unique_keys=["mpname", "date"], data=data)


Main()

import scraperwiki
import lxml.html
import urllib
import urlparse
import datetime
import re

url = "http://www.publications.parliament.uk/pa/cm/cmregmem/110124/part1contents.htm"

urlmainindex = "http://www.publications.parliament.uk/pa/cm/cmregmem.htm"


def Main():
    mainindexroot = lxml.html.parse(urlmainindex).getroot()
    urlyears = [ urlparse.urljoin(urlmainindex, a.attrib.get("href"))  for a in mainindexroot.cssselect("div#maincontent a")  if re.search("Members.*?Interests", a.text or "") ]

    for urlyear in urlyears:
        yearindexroot = lxml.html.parse(urlyear).getroot()
        urlversions = [ urlparse.urljoin(urlyear, a.attrib.get("href"))  for a in yearindexroot.cssselect("div#maincontent a")  if re.search("\s*Part 1", a.text or "") ]
        for url in urlversions:
            ScrapeRegmemVersion(url)
            #break  # do only one

        break  # do only one


def ScrapeRegmemVersion(url):
    root = lxml.html.parse(url).getroot()
    paras = root.cssselect('#wrapper #content #content-small table td p')
    assert paras[2].attrib.get("class") == "atozLinks"
    ilimit = scraperwiki.sqlite.get_var(url, 2)
    for i, p in enumerate(paras):
        if i <= ilimit:
            continue
        a = p.cssselect("a")[0]
        print i, a.text
        if a.text == "Terms of Reference":
            continue
        mpurl = urlparse.urljoin(url, a.attrib.get("href"))
        ScrapeRegmemPage(mpurl)
        scraperwiki.sqlite.save_var(url, i)


def flatten(elem):
    result = [ unicode(elem.text or "") ]
    for x in elem:
        result.append(flatten(x))
    result.append(elem.tail or "")
    return "".join(result)

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def ScrapeRegmemPage(mpurl):
    mproot = lxml.html.parse(mpurl).getroot()
    h1date = mproot.cssselect("h1.mainTitle br")[0].tail
    
    mdate = re.match("\s*As at (\d+)[thstnd]+ (\w+) (\d\d\d\d)", h1date)
    assert mdate, h1date
    date = datetime.date(int(mdate.group(3)), months.index(mdate.group(2))+1, int(mdate.group(1)))
    
    dpn = mproot.cssselect('#content-small .prevNext')[0].getnext()
    lines = [ ]
    while dpn.tag != "div":
        if dpn.tag == "h2":
            mpname = dpn.text
        elif dpn.tag == "h3":
            lines.append("")
            lines.append("")
            lines.append("** "+flatten(dpn))
        elif dpn.tag == "p":
            if dpn.attrib.get("class") == "indent":
                pp = " "
            elif dpn.attrib.get("class") == "indent2":
                pp = "  "
            else:
                pp = ""
            lines.append(pp+re.sub("\n", " ", flatten(dpn)).strip())
        else:
            assert False, lxml.html.tostring(dpn)
        dpn = dpn.getnext()
    data = { "mpname":mpname, "date":date, "mpurl":mpurl, "content":"\n".join(lines) }
    #data["mpid"] = getmpid(mpname, data["date"])
    scraperwiki.sqlite.save(unique_keys=["mpname", "date"], data=data)


Main()

import scraperwiki
import lxml.html
import urllib
import urlparse
import datetime
import re

url = "http://www.publications.parliament.uk/pa/cm/cmregmem/110124/part1contents.htm"

urlmainindex = "http://www.publications.parliament.uk/pa/cm/cmregmem.htm"


def Main():
    mainindexroot = lxml.html.parse(urlmainindex).getroot()
    urlyears = [ urlparse.urljoin(urlmainindex, a.attrib.get("href"))  for a in mainindexroot.cssselect("div#maincontent a")  if re.search("Members.*?Interests", a.text or "") ]

    for urlyear in urlyears:
        yearindexroot = lxml.html.parse(urlyear).getroot()
        urlversions = [ urlparse.urljoin(urlyear, a.attrib.get("href"))  for a in yearindexroot.cssselect("div#maincontent a")  if re.search("\s*Part 1", a.text or "") ]
        for url in urlversions:
            ScrapeRegmemVersion(url)
            #break  # do only one

        break  # do only one


def ScrapeRegmemVersion(url):
    root = lxml.html.parse(url).getroot()
    paras = root.cssselect('#wrapper #content #content-small table td p')
    assert paras[2].attrib.get("class") == "atozLinks"
    ilimit = scraperwiki.sqlite.get_var(url, 2)
    for i, p in enumerate(paras):
        if i <= ilimit:
            continue
        a = p.cssselect("a")[0]
        print i, a.text
        if a.text == "Terms of Reference":
            continue
        mpurl = urlparse.urljoin(url, a.attrib.get("href"))
        ScrapeRegmemPage(mpurl)
        scraperwiki.sqlite.save_var(url, i)


def flatten(elem):
    result = [ unicode(elem.text or "") ]
    for x in elem:
        result.append(flatten(x))
    result.append(elem.tail or "")
    return "".join(result)

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def ScrapeRegmemPage(mpurl):
    mproot = lxml.html.parse(mpurl).getroot()
    h1date = mproot.cssselect("h1.mainTitle br")[0].tail
    
    mdate = re.match("\s*As at (\d+)[thstnd]+ (\w+) (\d\d\d\d)", h1date)
    assert mdate, h1date
    date = datetime.date(int(mdate.group(3)), months.index(mdate.group(2))+1, int(mdate.group(1)))
    
    dpn = mproot.cssselect('#content-small .prevNext')[0].getnext()
    lines = [ ]
    while dpn.tag != "div":
        if dpn.tag == "h2":
            mpname = dpn.text
        elif dpn.tag == "h3":
            lines.append("")
            lines.append("")
            lines.append("** "+flatten(dpn))
        elif dpn.tag == "p":
            if dpn.attrib.get("class") == "indent":
                pp = " "
            elif dpn.attrib.get("class") == "indent2":
                pp = "  "
            else:
                pp = ""
            lines.append(pp+re.sub("\n", " ", flatten(dpn)).strip())
        else:
            assert False, lxml.html.tostring(dpn)
        dpn = dpn.getnext()
    data = { "mpname":mpname, "date":date, "mpurl":mpurl, "content":"\n".join(lines) }
    #data["mpid"] = getmpid(mpname, data["date"])
    scraperwiki.sqlite.save(unique_keys=["mpname", "date"], data=data)


Main()

import scraperwiki
import lxml.html
import urllib
import urlparse
import datetime
import re

url = "http://www.publications.parliament.uk/pa/cm/cmregmem/110124/part1contents.htm"

urlmainindex = "http://www.publications.parliament.uk/pa/cm/cmregmem.htm"


def Main():
    mainindexroot = lxml.html.parse(urlmainindex).getroot()
    urlyears = [ urlparse.urljoin(urlmainindex, a.attrib.get("href"))  for a in mainindexroot.cssselect("div#maincontent a")  if re.search("Members.*?Interests", a.text or "") ]

    for urlyear in urlyears:
        yearindexroot = lxml.html.parse(urlyear).getroot()
        urlversions = [ urlparse.urljoin(urlyear, a.attrib.get("href"))  for a in yearindexroot.cssselect("div#maincontent a")  if re.search("\s*Part 1", a.text or "") ]
        for url in urlversions:
            ScrapeRegmemVersion(url)
            #break  # do only one

        break  # do only one


def ScrapeRegmemVersion(url):
    root = lxml.html.parse(url).getroot()
    paras = root.cssselect('#wrapper #content #content-small table td p')
    assert paras[2].attrib.get("class") == "atozLinks"
    ilimit = scraperwiki.sqlite.get_var(url, 2)
    for i, p in enumerate(paras):
        if i <= ilimit:
            continue
        a = p.cssselect("a")[0]
        print i, a.text
        if a.text == "Terms of Reference":
            continue
        mpurl = urlparse.urljoin(url, a.attrib.get("href"))
        ScrapeRegmemPage(mpurl)
        scraperwiki.sqlite.save_var(url, i)


def flatten(elem):
    result = [ unicode(elem.text or "") ]
    for x in elem:
        result.append(flatten(x))
    result.append(elem.tail or "")
    return "".join(result)

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def ScrapeRegmemPage(mpurl):
    mproot = lxml.html.parse(mpurl).getroot()
    h1date = mproot.cssselect("h1.mainTitle br")[0].tail
    
    mdate = re.match("\s*As at (\d+)[thstnd]+ (\w+) (\d\d\d\d)", h1date)
    assert mdate, h1date
    date = datetime.date(int(mdate.group(3)), months.index(mdate.group(2))+1, int(mdate.group(1)))
    
    dpn = mproot.cssselect('#content-small .prevNext')[0].getnext()
    lines = [ ]
    while dpn.tag != "div":
        if dpn.tag == "h2":
            mpname = dpn.text
        elif dpn.tag == "h3":
            lines.append("")
            lines.append("")
            lines.append("** "+flatten(dpn))
        elif dpn.tag == "p":
            if dpn.attrib.get("class") == "indent":
                pp = " "
            elif dpn.attrib.get("class") == "indent2":
                pp = "  "
            else:
                pp = ""
            lines.append(pp+re.sub("\n", " ", flatten(dpn)).strip())
        else:
            assert False, lxml.html.tostring(dpn)
        dpn = dpn.getnext()
    data = { "mpname":mpname, "date":date, "mpurl":mpurl, "content":"\n".join(lines) }
    #data["mpid"] = getmpid(mpname, data["date"])
    scraperwiki.sqlite.save(unique_keys=["mpname", "date"], data=data)


Main()

import scraperwiki
import lxml.html
import urllib
import urlparse
import datetime
import re

url = "http://www.publications.parliament.uk/pa/cm/cmregmem/110124/part1contents.htm"

urlmainindex = "http://www.publications.parliament.uk/pa/cm/cmregmem.htm"


def Main():
    mainindexroot = lxml.html.parse(urlmainindex).getroot()
    urlyears = [ urlparse.urljoin(urlmainindex, a.attrib.get("href"))  for a in mainindexroot.cssselect("div#maincontent a")  if re.search("Members.*?Interests", a.text or "") ]

    for urlyear in urlyears:
        yearindexroot = lxml.html.parse(urlyear).getroot()
        urlversions = [ urlparse.urljoin(urlyear, a.attrib.get("href"))  for a in yearindexroot.cssselect("div#maincontent a")  if re.search("\s*Part 1", a.text or "") ]
        for url in urlversions:
            ScrapeRegmemVersion(url)
            #break  # do only one

        break  # do only one


def ScrapeRegmemVersion(url):
    root = lxml.html.parse(url).getroot()
    paras = root.cssselect('#wrapper #content #content-small table td p')
    assert paras[2].attrib.get("class") == "atozLinks"
    ilimit = scraperwiki.sqlite.get_var(url, 2)
    for i, p in enumerate(paras):
        if i <= ilimit:
            continue
        a = p.cssselect("a")[0]
        print i, a.text
        if a.text == "Terms of Reference":
            continue
        mpurl = urlparse.urljoin(url, a.attrib.get("href"))
        ScrapeRegmemPage(mpurl)
        scraperwiki.sqlite.save_var(url, i)


def flatten(elem):
    result = [ unicode(elem.text or "") ]
    for x in elem:
        result.append(flatten(x))
    result.append(elem.tail or "")
    return "".join(result)

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def ScrapeRegmemPage(mpurl):
    mproot = lxml.html.parse(mpurl).getroot()
    h1date = mproot.cssselect("h1.mainTitle br")[0].tail
    
    mdate = re.match("\s*As at (\d+)[thstnd]+ (\w+) (\d\d\d\d)", h1date)
    assert mdate, h1date
    date = datetime.date(int(mdate.group(3)), months.index(mdate.group(2))+1, int(mdate.group(1)))
    
    dpn = mproot.cssselect('#content-small .prevNext')[0].getnext()
    lines = [ ]
    while dpn.tag != "div":
        if dpn.tag == "h2":
            mpname = dpn.text
        elif dpn.tag == "h3":
            lines.append("")
            lines.append("")
            lines.append("** "+flatten(dpn))
        elif dpn.tag == "p":
            if dpn.attrib.get("class") == "indent":
                pp = " "
            elif dpn.attrib.get("class") == "indent2":
                pp = "  "
            else:
                pp = ""
            lines.append(pp+re.sub("\n", " ", flatten(dpn)).strip())
        else:
            assert False, lxml.html.tostring(dpn)
        dpn = dpn.getnext()
    data = { "mpname":mpname, "date":date, "mpurl":mpurl, "content":"\n".join(lines) }
    #data["mpid"] = getmpid(mpname, data["date"])
    scraperwiki.sqlite.save(unique_keys=["mpname", "date"], data=data)


Main()

import scraperwiki
import lxml.html
import urllib
import urlparse
import datetime
import re

url = "http://www.publications.parliament.uk/pa/cm/cmregmem/110124/part1contents.htm"

urlmainindex = "http://www.publications.parliament.uk/pa/cm/cmregmem.htm"


def Main():
    mainindexroot = lxml.html.parse(urlmainindex).getroot()
    urlyears = [ urlparse.urljoin(urlmainindex, a.attrib.get("href"))  for a in mainindexroot.cssselect("div#maincontent a")  if re.search("Members.*?Interests", a.text or "") ]

    for urlyear in urlyears:
        yearindexroot = lxml.html.parse(urlyear).getroot()
        urlversions = [ urlparse.urljoin(urlyear, a.attrib.get("href"))  for a in yearindexroot.cssselect("div#maincontent a")  if re.search("\s*Part 1", a.text or "") ]
        for url in urlversions:
            ScrapeRegmemVersion(url)
            #break  # do only one

        break  # do only one


def ScrapeRegmemVersion(url):
    root = lxml.html.parse(url).getroot()
    paras = root.cssselect('#wrapper #content #content-small table td p')
    assert paras[2].attrib.get("class") == "atozLinks"
    ilimit = scraperwiki.sqlite.get_var(url, 2)
    for i, p in enumerate(paras):
        if i <= ilimit:
            continue
        a = p.cssselect("a")[0]
        print i, a.text
        if a.text == "Terms of Reference":
            continue
        mpurl = urlparse.urljoin(url, a.attrib.get("href"))
        ScrapeRegmemPage(mpurl)
        scraperwiki.sqlite.save_var(url, i)


def flatten(elem):
    result = [ unicode(elem.text or "") ]
    for x in elem:
        result.append(flatten(x))
    result.append(elem.tail or "")
    return "".join(result)

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def ScrapeRegmemPage(mpurl):
    mproot = lxml.html.parse(mpurl).getroot()
    h1date = mproot.cssselect("h1.mainTitle br")[0].tail
    
    mdate = re.match("\s*As at (\d+)[thstnd]+ (\w+) (\d\d\d\d)", h1date)
    assert mdate, h1date
    date = datetime.date(int(mdate.group(3)), months.index(mdate.group(2))+1, int(mdate.group(1)))
    
    dpn = mproot.cssselect('#content-small .prevNext')[0].getnext()
    lines = [ ]
    while dpn.tag != "div":
        if dpn.tag == "h2":
            mpname = dpn.text
        elif dpn.tag == "h3":
            lines.append("")
            lines.append("")
            lines.append("** "+flatten(dpn))
        elif dpn.tag == "p":
            if dpn.attrib.get("class") == "indent":
                pp = " "
            elif dpn.attrib.get("class") == "indent2":
                pp = "  "
            else:
                pp = ""
            lines.append(pp+re.sub("\n", " ", flatten(dpn)).strip())
        else:
            assert False, lxml.html.tostring(dpn)
        dpn = dpn.getnext()
    data = { "mpname":mpname, "date":date, "mpurl":mpurl, "content":"\n".join(lines) }
    #data["mpid"] = getmpid(mpname, data["date"])
    scraperwiki.sqlite.save(unique_keys=["mpname", "date"], data=data)


Main()

import scraperwiki
import lxml.html
import urllib
import urlparse
import datetime
import re

url = "http://www.publications.parliament.uk/pa/cm/cmregmem/110124/part1contents.htm"

urlmainindex = "http://www.publications.parliament.uk/pa/cm/cmregmem.htm"


def Main():
    mainindexroot = lxml.html.parse(urlmainindex).getroot()
    urlyears = [ urlparse.urljoin(urlmainindex, a.attrib.get("href"))  for a in mainindexroot.cssselect("div#maincontent a")  if re.search("Members.*?Interests", a.text or "") ]

    for urlyear in urlyears:
        yearindexroot = lxml.html.parse(urlyear).getroot()
        urlversions = [ urlparse.urljoin(urlyear, a.attrib.get("href"))  for a in yearindexroot.cssselect("div#maincontent a")  if re.search("\s*Part 1", a.text or "") ]
        for url in urlversions:
            ScrapeRegmemVersion(url)
            #break  # do only one

        break  # do only one


def ScrapeRegmemVersion(url):
    root = lxml.html.parse(url).getroot()
    paras = root.cssselect('#wrapper #content #content-small table td p')
    assert paras[2].attrib.get("class") == "atozLinks"
    ilimit = scraperwiki.sqlite.get_var(url, 2)
    for i, p in enumerate(paras):
        if i <= ilimit:
            continue
        a = p.cssselect("a")[0]
        print i, a.text
        if a.text == "Terms of Reference":
            continue
        mpurl = urlparse.urljoin(url, a.attrib.get("href"))
        ScrapeRegmemPage(mpurl)
        scraperwiki.sqlite.save_var(url, i)


def flatten(elem):
    result = [ unicode(elem.text or "") ]
    for x in elem:
        result.append(flatten(x))
    result.append(elem.tail or "")
    return "".join(result)

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def ScrapeRegmemPage(mpurl):
    mproot = lxml.html.parse(mpurl).getroot()
    h1date = mproot.cssselect("h1.mainTitle br")[0].tail
    
    mdate = re.match("\s*As at (\d+)[thstnd]+ (\w+) (\d\d\d\d)", h1date)
    assert mdate, h1date
    date = datetime.date(int(mdate.group(3)), months.index(mdate.group(2))+1, int(mdate.group(1)))
    
    dpn = mproot.cssselect('#content-small .prevNext')[0].getnext()
    lines = [ ]
    while dpn.tag != "div":
        if dpn.tag == "h2":
            mpname = dpn.text
        elif dpn.tag == "h3":
            lines.append("")
            lines.append("")
            lines.append("** "+flatten(dpn))
        elif dpn.tag == "p":
            if dpn.attrib.get("class") == "indent":
                pp = " "
            elif dpn.attrib.get("class") == "indent2":
                pp = "  "
            else:
                pp = ""
            lines.append(pp+re.sub("\n", " ", flatten(dpn)).strip())
        else:
            assert False, lxml.html.tostring(dpn)
        dpn = dpn.getnext()
    data = { "mpname":mpname, "date":date, "mpurl":mpurl, "content":"\n".join(lines) }
    #data["mpid"] = getmpid(mpname, data["date"])
    scraperwiki.sqlite.save(unique_keys=["mpname", "date"], data=data)


Main()

import scraperwiki
import lxml.html
import urllib
import urlparse
import datetime
import re

url = "http://www.publications.parliament.uk/pa/cm/cmregmem/110124/part1contents.htm"

urlmainindex = "http://www.publications.parliament.uk/pa/cm/cmregmem.htm"


def Main():
    mainindexroot = lxml.html.parse(urlmainindex).getroot()
    urlyears = [ urlparse.urljoin(urlmainindex, a.attrib.get("href"))  for a in mainindexroot.cssselect("div#maincontent a")  if re.search("Members.*?Interests", a.text or "") ]

    for urlyear in urlyears:
        yearindexroot = lxml.html.parse(urlyear).getroot()
        urlversions = [ urlparse.urljoin(urlyear, a.attrib.get("href"))  for a in yearindexroot.cssselect("div#maincontent a")  if re.search("\s*Part 1", a.text or "") ]
        for url in urlversions:
            ScrapeRegmemVersion(url)
            #break  # do only one

        break  # do only one


def ScrapeRegmemVersion(url):
    root = lxml.html.parse(url).getroot()
    paras = root.cssselect('#wrapper #content #content-small table td p')
    assert paras[2].attrib.get("class") == "atozLinks"
    ilimit = scraperwiki.sqlite.get_var(url, 2)
    for i, p in enumerate(paras):
        if i <= ilimit:
            continue
        a = p.cssselect("a")[0]
        print i, a.text
        if a.text == "Terms of Reference":
            continue
        mpurl = urlparse.urljoin(url, a.attrib.get("href"))
        ScrapeRegmemPage(mpurl)
        scraperwiki.sqlite.save_var(url, i)


def flatten(elem):
    result = [ unicode(elem.text or "") ]
    for x in elem:
        result.append(flatten(x))
    result.append(elem.tail or "")
    return "".join(result)

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def ScrapeRegmemPage(mpurl):
    mproot = lxml.html.parse(mpurl).getroot()
    h1date = mproot.cssselect("h1.mainTitle br")[0].tail
    
    mdate = re.match("\s*As at (\d+)[thstnd]+ (\w+) (\d\d\d\d)", h1date)
    assert mdate, h1date
    date = datetime.date(int(mdate.group(3)), months.index(mdate.group(2))+1, int(mdate.group(1)))
    
    dpn = mproot.cssselect('#content-small .prevNext')[0].getnext()
    lines = [ ]
    while dpn.tag != "div":
        if dpn.tag == "h2":
            mpname = dpn.text
        elif dpn.tag == "h3":
            lines.append("")
            lines.append("")
            lines.append("** "+flatten(dpn))
        elif dpn.tag == "p":
            if dpn.attrib.get("class") == "indent":
                pp = " "
            elif dpn.attrib.get("class") == "indent2":
                pp = "  "
            else:
                pp = ""
            lines.append(pp+re.sub("\n", " ", flatten(dpn)).strip())
        else:
            assert False, lxml.html.tostring(dpn)
        dpn = dpn.getnext()
    data = { "mpname":mpname, "date":date, "mpurl":mpurl, "content":"\n".join(lines) }
    #data["mpid"] = getmpid(mpname, data["date"])
    scraperwiki.sqlite.save(unique_keys=["mpname", "date"], data=data)


Main()

