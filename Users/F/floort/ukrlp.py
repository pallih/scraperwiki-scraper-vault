import scraperwiki
from BeautifulSoup import BeautifulSoup

RANGE = 1000000

def strip_tags(s):
    start = s.find("<")
    if start == -1:
        return s # No tags
    end = s.find(">", start)+1
    return s[:start]+strip_tags(s[end:])

for i in xrange(RANGE):
    url = "http://www.ukrlp.co.uk/ukrlp/ukrlp_provider.page_pls_provDetails?x=&pn_p_id=1%07d&pv_status=VERIFIED" % (i)
    html = scraperwiki.scrape(url)
    bs = BeautifulSoup(html)
    data = {}
    content = bs.find("div", {"class": "pod_main_body"})
    title = content.findAll("div", {"class":"provhead"})
    data["ukprn"] = int(title[0].string.split()[1])
    data["name"] = strip_tags(str(title[1])).strip()
    raw = str(content)
    start = raw.find('<div class="assoc">Legal address</div>')
    end = raw.find('<div class="assoc">Primary contact address</div>')
    address = ""
    for line in  raw[start:end].split("<br />")[1:]:
        l = line.strip()
        if l.startswith("<strong>"):
            s = l.find(">") + 1
            e = l.find("</strong>")
            data["legal_"+l[s:e].strip()[:-1]] = l[e+9:].strip()
        else:
            if l == "<": continue
            if not l: continue
            address += l.strip() + "; "
    data["legal_address"] = address[:-2]

    start = raw.find('<div class="assoc">Primary contact address</div>')
    end = raw.find('<b>More Information about this provider:</b>')
    more_info = True
    if end == -1:
        end = raw.find('<div class="searchleft">')
        more_info = False
    address = ""
    for line in  raw[start:end].split("<br />")[1:]:
        l = line.strip()
        if l.startswith("<strong>"):
            s = l.find(">") + 1
            e = l.find("</strong>")
            data["contact_"+l[s:e].strip()[:-1]] = strip_tags(l[e+9:]).strip()
        else:
            if l == "<": continue
            if not l: continue
            address += l.strip() + "; "
    data["contact_address"] = address[:-2]
    data["url"] = url

    scraperwiki.datastore.save(["ukprn"], data)import scraperwiki
from BeautifulSoup import BeautifulSoup

RANGE = 1000000

def strip_tags(s):
    start = s.find("<")
    if start == -1:
        return s # No tags
    end = s.find(">", start)+1
    return s[:start]+strip_tags(s[end:])

for i in xrange(RANGE):
    url = "http://www.ukrlp.co.uk/ukrlp/ukrlp_provider.page_pls_provDetails?x=&pn_p_id=1%07d&pv_status=VERIFIED&pv_vis_code=L" % (i)
    html = scraperwiki.scrape(url)
    bs = BeautifulSoup(html)
    data = {}
    content = bs.find("div", {"class": "pod_main_body"})
    title = content.findAll("div", {"class":"provhead"})
    data["ukprn"] = int(title[0].string.split()[1])
    data["name"] = strip_tags(str(title[1])).strip()
    raw = str(content)
    start = raw.find('<div class="assoc">Legal address</div>')
    end = raw.find('<div class="assoc">Primary contact address</div>')
    address = ""
    for line in  raw[start:end].split("<br />")[1:]:
        l = line.strip()
        if l.startswith("<strong>"):
            s = l.find(">") + 1
            e = l.find("</strong>")
            data["legal_"+l[s:e].strip()[:-1]] = l[e+9:].strip()
        else:
            if l == "<": continue
            if not l: continue
            address += l.strip() + "; "
    data["legal_address"] = address[:-2]

    start = raw.find('<div class="assoc">Primary contact address</div>')
    end = raw.find('<b>More Information about this provider:</b>')
    more_info = True
    if end == -1:
        end = raw.find('<div class="searchleft">')
        more_info = False
    address = ""
    for line in  raw[start:end].split("<br />")[1:]:
        l = line.strip()
        if l.startswith("<strong>"):
            s = l.find(">") + 1
            e = l.find("</strong>")
            data["contact_"+l[s:e].strip()[:-1]] = strip_tags(l[e+9:]).strip()
        else:
            if l == "<": continue
            if not l: continue
            address += l.strip() + "; "
    data["contact_address"] = address[:-2]
    data["url"] = url

    scraperwiki.sqlite.save(["ukprn"], data)