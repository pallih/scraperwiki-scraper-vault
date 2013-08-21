"""One scraper to download all Fingal datasets into sql database so we can see them all together"""

# depagenation not complete
import scraperwiki
import mechanize
import re
import csv

url = "http://data.fingal.ie/ViewDataSets/"

br2 = mechanize.Browser()

def ScrapeCSVlink(title, request):
    response = br2.open(request)
    csvtext = response.read()
    print csvtext
    rows = list(csv.reader(csvtext.splitlines()))
    print title, rows[0]
    headers = [ re.sub("[^\w\s_]", "", th)  for th in rows[0] ]
    while not headers[-1]:
         headers.pop()
    ldata = [ ]
    for row in rows[1:]:
        if not "".join(row):
            continue
        lrow = [ td.decode("latin1")  for td in row ]
        while len(lrow) < len(headers):
            lrow.append("")
        data = dict(zip(headers, lrow))
        if data:
            ldata.append(data)
    scraperwiki.sqlite.save(headers, ldata, title)


def ExtractCSVlinks(br):
    res = [ ]
    for link in br.links():
        attrib = dict(link.attrs)
        if attrib.get("title", "")[-4:] == " CSV" and link.text == 'HyperLink[IMG]':
            print attrib["title"], link
            res.append((attrib, br.click_link(link)))
    return res


links = [ ]
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(url)
while True:
    links.extend(ExtractCSVlinks(br))
    html = br.response().read()
    mnext = re.search("""<a id="lnkNext" href="javascript:__doPostBack\(&#39;(.*?)&#39;,&#39;(.*?)&#39;\)">Next >></a>""", html)
    if not mnext:
        break
    br.form = list(br.forms())[0]
    print br.form
    br.set_all_readonly(False)
    br["__EVENTTARGET"] = mnext.group(1)
    br["__EVENTARGUMENT"] = mnext.group(2)
    for control in br.form.controls:
        if control.type == "submit":
            control.disabled = True
    response = br.submit()

for attrib, request in links:
    title = re.sub("[^\w\s]", "", attrib["title"][:-4]).strip()
    ScrapeCSVlink(title, request)






"""One scraper to download all Fingal datasets into sql database so we can see them all together"""

# depagenation not complete
import scraperwiki
import mechanize
import re
import csv

url = "http://data.fingal.ie/ViewDataSets/"

br2 = mechanize.Browser()

def ScrapeCSVlink(title, request):
    response = br2.open(request)
    csvtext = response.read()
    print csvtext
    rows = list(csv.reader(csvtext.splitlines()))
    print title, rows[0]
    headers = [ re.sub("[^\w\s_]", "", th)  for th in rows[0] ]
    while not headers[-1]:
         headers.pop()
    ldata = [ ]
    for row in rows[1:]:
        if not "".join(row):
            continue
        lrow = [ td.decode("latin1")  for td in row ]
        while len(lrow) < len(headers):
            lrow.append("")
        data = dict(zip(headers, lrow))
        if data:
            ldata.append(data)
    scraperwiki.sqlite.save(headers, ldata, title)


def ExtractCSVlinks(br):
    res = [ ]
    for link in br.links():
        attrib = dict(link.attrs)
        if attrib.get("title", "")[-4:] == " CSV" and link.text == 'HyperLink[IMG]':
            print attrib["title"], link
            res.append((attrib, br.click_link(link)))
    return res


links = [ ]
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open(url)
while True:
    links.extend(ExtractCSVlinks(br))
    html = br.response().read()
    mnext = re.search("""<a id="lnkNext" href="javascript:__doPostBack\(&#39;(.*?)&#39;,&#39;(.*?)&#39;\)">Next >></a>""", html)
    if not mnext:
        break
    br.form = list(br.forms())[0]
    print br.form
    br.set_all_readonly(False)
    br["__EVENTTARGET"] = mnext.group(1)
    br["__EVENTARGUMENT"] = mnext.group(2)
    for control in br.form.controls:
        if control.type == "submit":
            control.disabled = True
    response = br.submit()

for attrib, request in links:
    title = re.sub("[^\w\s]", "", attrib["title"][:-4]).strip()
    ScrapeCSVlink(title, request)






