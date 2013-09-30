import scraperwiki
import lxml.html, lxml.etree
import urllib2
import urlparse



base_url = 'http://www.nice.org.uk/guidance/index.jsp?action=ByType&type=2&status=3&p=off' 
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def getheadingsfrompdf(pdfurl):
    pdfdata = urllib2.urlopen(pdfurl).read()
    pdfxml = scraperwiki.pdftoxml(pdfdata)
    root = lxml.etree.fromstring(pdfxml)
    
    ldata = [ ]
    for page in root:
        for el in page:
                # needs also to do concatenation between headings that run to two lines, 
                # and handle headings with italics in them <i>
            if el.tag == "text" and el.attrib.get("font") == "10" and len(el) == 1 and el[0].tag == "b":
                data = {"pdfurl":pdfurl, "pagenumber":int(page.attrib.get("number")), "heading":el[0].text}
                ldata.append(data)
    scraperwiki.sqlite.save(["pdfurl", "pagenumber", "heading"], ldata, "subheadings")



def monthdate(d):
    assert len(d) == 8, d
    return "%s-%02d" % (d[4:], months.index(d[:3])+1)

def GetDirectPDF(durl):
    html = urllib2.urlopen(durl).read()
    root = lxml.html.fromstring(html)
    dlink =root.cssselect("div.contentInner a#hyperlink")
    assert dlink
    return urlparse.urljoin(durl, dlink[0].attrib.get("href"))


def guidefrompage(purl):
    phtml = urllib2.urlopen(purl).read()
    proot = lxml.html.fromstring(phtml)
    uloptions = proot.cssselect("div.guidance-content ul.options")
    pdata = { }
    for li in uloptions[0].cssselect("li"):
        if not li.text:
            continue
        key = li.text.strip()
        if key == 'No documents found':
            continue
        if key in ['Full guideline', 'Distribution List']:
            continue
        assert key in ["NICE guidance written for patients and carers", 'Quick reference guide', 'NICE guideline', 'Full guideline'], key
        for a in li:
            assert a.tag == "a"
            format = a.text.strip()
            if format == "Fformat MS Word":
                continue
            if format == "documents":
                continue
            assert format in ["PDF format", "MS Word format"], format
            ckey = "%s - %s" % (key, format[:-7])
            dpdf = a.attrib.get("href")  # holding page
            pdata[ckey] = dpdf
            if format == "PDF format":
                pdfurl = GetDirectPDF(dpdf)
                pdata[key+" - PDF"] = pdfurl
                getheadingsfrompdf(pdfurl)

    return pdata

def Main():
    html = urllib2.urlopen(base_url).read()
    #print html
    root = lxml.html.fromstring(html)
    rows = root.cssselect("table#row tr")
    headers = [ th.text_content().strip()  for th in rows[0] ]
    assert headers == ['Ref', 'Title', 'Date Issued', 'Review'], headers
    for n, row in enumerate(rows[1:]):
        assert row[1][0].tag == "a", lxml.html.tostring(row)
        data = dict(zip(headers, [ td.text_content().strip()  for td in row ]))
        data["link"] = row[1][0].attrib.get("href")
        data['Date Issued'] = monthdate(data['Date Issued'])
        if data['Review'] in ["", "TBC"]:
            data.pop('Review')
        else:
            data['Review'] = monthdate(data['Review'])
        data["rownumber"] = n
        pdata = guidefrompage(data["link"])
        
        data.update(pdata)
        scraperwiki.sqlite.save(["rownumber"], data)

Main()
import scraperwiki
import lxml.html, lxml.etree
import urllib2
import urlparse



base_url = 'http://www.nice.org.uk/guidance/index.jsp?action=ByType&type=2&status=3&p=off' 
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def getheadingsfrompdf(pdfurl):
    pdfdata = urllib2.urlopen(pdfurl).read()
    pdfxml = scraperwiki.pdftoxml(pdfdata)
    root = lxml.etree.fromstring(pdfxml)
    
    ldata = [ ]
    for page in root:
        for el in page:
                # needs also to do concatenation between headings that run to two lines, 
                # and handle headings with italics in them <i>
            if el.tag == "text" and el.attrib.get("font") == "10" and len(el) == 1 and el[0].tag == "b":
                data = {"pdfurl":pdfurl, "pagenumber":int(page.attrib.get("number")), "heading":el[0].text}
                ldata.append(data)
    scraperwiki.sqlite.save(["pdfurl", "pagenumber", "heading"], ldata, "subheadings")



def monthdate(d):
    assert len(d) == 8, d
    return "%s-%02d" % (d[4:], months.index(d[:3])+1)

def GetDirectPDF(durl):
    html = urllib2.urlopen(durl).read()
    root = lxml.html.fromstring(html)
    dlink =root.cssselect("div.contentInner a#hyperlink")
    assert dlink
    return urlparse.urljoin(durl, dlink[0].attrib.get("href"))


def guidefrompage(purl):
    phtml = urllib2.urlopen(purl).read()
    proot = lxml.html.fromstring(phtml)
    uloptions = proot.cssselect("div.guidance-content ul.options")
    pdata = { }
    for li in uloptions[0].cssselect("li"):
        if not li.text:
            continue
        key = li.text.strip()
        if key == 'No documents found':
            continue
        if key in ['Full guideline', 'Distribution List']:
            continue
        assert key in ["NICE guidance written for patients and carers", 'Quick reference guide', 'NICE guideline', 'Full guideline'], key
        for a in li:
            assert a.tag == "a"
            format = a.text.strip()
            if format == "Fformat MS Word":
                continue
            if format == "documents":
                continue
            assert format in ["PDF format", "MS Word format"], format
            ckey = "%s - %s" % (key, format[:-7])
            dpdf = a.attrib.get("href")  # holding page
            pdata[ckey] = dpdf
            if format == "PDF format":
                pdfurl = GetDirectPDF(dpdf)
                pdata[key+" - PDF"] = pdfurl
                getheadingsfrompdf(pdfurl)

    return pdata

def Main():
    html = urllib2.urlopen(base_url).read()
    #print html
    root = lxml.html.fromstring(html)
    rows = root.cssselect("table#row tr")
    headers = [ th.text_content().strip()  for th in rows[0] ]
    assert headers == ['Ref', 'Title', 'Date Issued', 'Review'], headers
    for n, row in enumerate(rows[1:]):
        assert row[1][0].tag == "a", lxml.html.tostring(row)
        data = dict(zip(headers, [ td.text_content().strip()  for td in row ]))
        data["link"] = row[1][0].attrib.get("href")
        data['Date Issued'] = monthdate(data['Date Issued'])
        if data['Review'] in ["", "TBC"]:
            data.pop('Review')
        else:
            data['Review'] = monthdate(data['Review'])
        data["rownumber"] = n
        pdata = guidefrompage(data["link"])
        
        data.update(pdata)
        scraperwiki.sqlite.save(["rownumber"], data)

Main()
import scraperwiki
import lxml.html, lxml.etree
import urllib2
import urlparse



base_url = 'http://www.nice.org.uk/guidance/index.jsp?action=ByType&type=2&status=3&p=off' 
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def getheadingsfrompdf(pdfurl):
    pdfdata = urllib2.urlopen(pdfurl).read()
    pdfxml = scraperwiki.pdftoxml(pdfdata)
    root = lxml.etree.fromstring(pdfxml)
    
    ldata = [ ]
    for page in root:
        for el in page:
                # needs also to do concatenation between headings that run to two lines, 
                # and handle headings with italics in them <i>
            if el.tag == "text" and el.attrib.get("font") == "10" and len(el) == 1 and el[0].tag == "b":
                data = {"pdfurl":pdfurl, "pagenumber":int(page.attrib.get("number")), "heading":el[0].text}
                ldata.append(data)
    scraperwiki.sqlite.save(["pdfurl", "pagenumber", "heading"], ldata, "subheadings")



def monthdate(d):
    assert len(d) == 8, d
    return "%s-%02d" % (d[4:], months.index(d[:3])+1)

def GetDirectPDF(durl):
    html = urllib2.urlopen(durl).read()
    root = lxml.html.fromstring(html)
    dlink =root.cssselect("div.contentInner a#hyperlink")
    assert dlink
    return urlparse.urljoin(durl, dlink[0].attrib.get("href"))


def guidefrompage(purl):
    phtml = urllib2.urlopen(purl).read()
    proot = lxml.html.fromstring(phtml)
    uloptions = proot.cssselect("div.guidance-content ul.options")
    pdata = { }
    for li in uloptions[0].cssselect("li"):
        if not li.text:
            continue
        key = li.text.strip()
        if key == 'No documents found':
            continue
        if key in ['Full guideline', 'Distribution List']:
            continue
        assert key in ["NICE guidance written for patients and carers", 'Quick reference guide', 'NICE guideline', 'Full guideline'], key
        for a in li:
            assert a.tag == "a"
            format = a.text.strip()
            if format == "Fformat MS Word":
                continue
            if format == "documents":
                continue
            assert format in ["PDF format", "MS Word format"], format
            ckey = "%s - %s" % (key, format[:-7])
            dpdf = a.attrib.get("href")  # holding page
            pdata[ckey] = dpdf
            if format == "PDF format":
                pdfurl = GetDirectPDF(dpdf)
                pdata[key+" - PDF"] = pdfurl
                getheadingsfrompdf(pdfurl)

    return pdata

def Main():
    html = urllib2.urlopen(base_url).read()
    #print html
    root = lxml.html.fromstring(html)
    rows = root.cssselect("table#row tr")
    headers = [ th.text_content().strip()  for th in rows[0] ]
    assert headers == ['Ref', 'Title', 'Date Issued', 'Review'], headers
    for n, row in enumerate(rows[1:]):
        assert row[1][0].tag == "a", lxml.html.tostring(row)
        data = dict(zip(headers, [ td.text_content().strip()  for td in row ]))
        data["link"] = row[1][0].attrib.get("href")
        data['Date Issued'] = monthdate(data['Date Issued'])
        if data['Review'] in ["", "TBC"]:
            data.pop('Review')
        else:
            data['Review'] = monthdate(data['Review'])
        data["rownumber"] = n
        pdata = guidefrompage(data["link"])
        
        data.update(pdata)
        scraperwiki.sqlite.save(["rownumber"], data)

Main()
import scraperwiki
import lxml.html, lxml.etree
import urllib2
import urlparse



base_url = 'http://www.nice.org.uk/guidance/index.jsp?action=ByType&type=2&status=3&p=off' 
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def getheadingsfrompdf(pdfurl):
    pdfdata = urllib2.urlopen(pdfurl).read()
    pdfxml = scraperwiki.pdftoxml(pdfdata)
    root = lxml.etree.fromstring(pdfxml)
    
    ldata = [ ]
    for page in root:
        for el in page:
                # needs also to do concatenation between headings that run to two lines, 
                # and handle headings with italics in them <i>
            if el.tag == "text" and el.attrib.get("font") == "10" and len(el) == 1 and el[0].tag == "b":
                data = {"pdfurl":pdfurl, "pagenumber":int(page.attrib.get("number")), "heading":el[0].text}
                ldata.append(data)
    scraperwiki.sqlite.save(["pdfurl", "pagenumber", "heading"], ldata, "subheadings")



def monthdate(d):
    assert len(d) == 8, d
    return "%s-%02d" % (d[4:], months.index(d[:3])+1)

def GetDirectPDF(durl):
    html = urllib2.urlopen(durl).read()
    root = lxml.html.fromstring(html)
    dlink =root.cssselect("div.contentInner a#hyperlink")
    assert dlink
    return urlparse.urljoin(durl, dlink[0].attrib.get("href"))


def guidefrompage(purl):
    phtml = urllib2.urlopen(purl).read()
    proot = lxml.html.fromstring(phtml)
    uloptions = proot.cssselect("div.guidance-content ul.options")
    pdata = { }
    for li in uloptions[0].cssselect("li"):
        if not li.text:
            continue
        key = li.text.strip()
        if key == 'No documents found':
            continue
        if key in ['Full guideline', 'Distribution List']:
            continue
        assert key in ["NICE guidance written for patients and carers", 'Quick reference guide', 'NICE guideline', 'Full guideline'], key
        for a in li:
            assert a.tag == "a"
            format = a.text.strip()
            if format == "Fformat MS Word":
                continue
            if format == "documents":
                continue
            assert format in ["PDF format", "MS Word format"], format
            ckey = "%s - %s" % (key, format[:-7])
            dpdf = a.attrib.get("href")  # holding page
            pdata[ckey] = dpdf
            if format == "PDF format":
                pdfurl = GetDirectPDF(dpdf)
                pdata[key+" - PDF"] = pdfurl
                getheadingsfrompdf(pdfurl)

    return pdata

def Main():
    html = urllib2.urlopen(base_url).read()
    #print html
    root = lxml.html.fromstring(html)
    rows = root.cssselect("table#row tr")
    headers = [ th.text_content().strip()  for th in rows[0] ]
    assert headers == ['Ref', 'Title', 'Date Issued', 'Review'], headers
    for n, row in enumerate(rows[1:]):
        assert row[1][0].tag == "a", lxml.html.tostring(row)
        data = dict(zip(headers, [ td.text_content().strip()  for td in row ]))
        data["link"] = row[1][0].attrib.get("href")
        data['Date Issued'] = monthdate(data['Date Issued'])
        if data['Review'] in ["", "TBC"]:
            data.pop('Review')
        else:
            data['Review'] = monthdate(data['Review'])
        data["rownumber"] = n
        pdata = guidefrompage(data["link"])
        
        data.update(pdata)
        scraperwiki.sqlite.save(["rownumber"], data)

Main()
