import scraperwiki
import mechanize
import re
import urlparse
from scraperwiki import datastore

def Main():
    br = mechanize.Browser()
    br.set_handle_robots(False)
    getPPCs(br)
    getMPs(br)   # currently Labour website down for MPs

def getPPCs(br):
    for i in range(1,19):
        url = "http://www.labour.org.uk/ppc?Page=%d" % i
        print "Page %d" % i, url
        page = br.open(url)
        html = page.read()
        main = re.findall('(?si)<ul class="swc_List">(.*?)</ul>', html)
        ppcs = re.findall('(?si)<li.*?>(.*?)</li>', main[0])
        for ppc in ppcs:
            data = {}
            name = re.findall('(?si)<a href=".*?".*>(.*?),.*?</a>', ppc)
            data["name"] = SimplifyHTML(name[0])
            link = re.findall('(?si)<a href="(.*?)".*>.*</a>', ppc)
            data["url"] = urlparse.urljoin(url, link[0])
            extra = br.follow_link(url_regex=link[0])
            details(extra.read(), data)
            br.back()

def getMPs(br):
    for i in range(1,19):
        url = "http://www.labour.org.uk/mp?Page=%d" % i
        print "Page %d" % i, url
        page = br.open(url)
        html = page.read()
        main = re.findall('(?si)<ul class="swc_List">(.*?)</ul>', html)
        mps = re.findall('(?si)<li.*?>(.*?)</li>', main[0])
        for mp in mps:
            data = {}
            name = re.findall('(?si)<a href=".*?".*>(.*?),.*?</a>', mp)
            data["name"] = SimplifyHTML(name[0])
            constituency_mp = re.findall('(?si)<a href=".*?".*>.*?, MP for (.*?)</a>', mp)
            if constituency_mp:
                data["constituency_mp"] = SimplifyHTML(constituency_mp[0])
            link = re.findall('(?si)<a href="(.*?)".*>.*?, MP for .*?</a>', mp)
            data["url"] = urlparse.urljoin(url, link[0])
            print mp, data["url"]
            extra = br.follow_link(url_regex=link[0])
            details(extra.read(), data)
            br.back()

            
def TWFYconstituencies():
    constituencylisturl = "http://www.theyworkforyou.com/boundaries/new-constituencies.tsv"
    constituencylist = scraperwiki.scrape(constituencylisturl)
    result = { }
    for con, r in re.findall("(.*?)\t(.*?)\n", constituencylist):
        lcon = re.sub(",", "", con)
        lcon = re.sub("-", " ", lcon).lower()
        result[lcon] = con
    return result

twfyconstituencies = TWFYconstituencies()

corrections = {'Shetland':"Orkney and Shetland", 'Orkney':"Orkney and Shetland"}  # both have same candidate
def RegularizeConstituency(lcon):
    lcon = re.sub(",", "", lcon)
    lcon = re.sub("-", " ", lcon)
    lcon = re.sub("  ", " ", lcon)
    lcon = re.sub(" &amp; ", " and ", lcon)
    lcon = re.sub(" & ", " and ", lcon)
    lcon = re.sub("(?i)\s+Clp$", "", lcon)
    lcon = corrections.get(lcon, lcon)
    return twfyconstituencies.get(lcon.lower())


def SimplifyHTML(html):
    t = html
    t = re.sub("<p><strong>(.*)</strong></p>", "==\\1==NEWLINE", t)
    t = re.sub("<p>", "NEWLINE", t)
    t = re.sub("<h2>(.*)</h2>", "NEWLINE==\\1==NEWLINE", t)
    t = re.sub("&amp;", "&", t)
    t = re.sub("&[\w#]*;?", " ", t)
    t = re.sub("(?s)<style>.*?</style>|<!--.*?-->", " ", t)
    t = re.sub("(?:<[^>]*>|\s)+", " ", t)
    t = re.sub("(?:\s*NEWLINE\s*)+", "\n\n", t).strip()
    return t

def details(extra, data):
    address = re.findall('(?si)<!-- BLOCK: PostalAddress -->\s*<strong>Write to me at:</strong><br />(.*?)<br /><br />\s*<!-- ENDBLOCK: PostalAddress -->', extra)
    if address:
        address = re.sub('\r|,', '', address[0])
        data["address"] = re.sub('\n', ' ', address)
    phone = re.findall('(?si)<!-- BLOCK: Telephone -->\s*<strong>Phone me on:</strong><br />(.*?)<br /><br />\s*<!-- ENDBLOCK: Telephone -->', extra)
    if phone:
        data["phone"] = phone[0]
    email = re.findall('(?si)<!-- BLOCK: EmailAddress -->\s*<strong>Email me at:</strong><br /><a href="mailto:(.*?)">.*?</a><br /><br />\s*<!-- ENDBLOCK: EmailAddress -->', extra)
    if email:
        data["email"] = email[0]
    website = re.findall('(?si)<!-- BLOCK: WebsiteAddress -->\s*<strong>Website address:</strong><br /><a href="(.*?)".*?>.*?</a><br /><br />\s*<!-- ENDBLOCK: WebsiteAddress -->', extra)
    if website:
        data["website"] = website[0]
    bio = re.findall('(?si)<!-- BLOCK: Biography -->\s*<div class="content_pod_content_title"><h1>.*?</h1></div>(.*?)<!-- ENDBLOCK: Biography -->', extra)
    if bio:
        data["bio"] = SimplifyHTML(bio[0])
        if re.search("Rory Palmer", data["bio"]):  # very bad formatting here
            data["bio"] = re.sub("(?s)^Rory Palmer.*?About Rory Palmer", "", data["bio"])
            data["bio"] = re.sub("==", "", data["bio"])
            data["bio"] = re.sub("\s*?\n\n\s*?", "\n\n", data["bio"]).strip()
        data["bio"] = re.sub("^Biographical Details\n\s*", "", data["bio"])
    photo = re.findall('(?si)<td valign="top" width="210"><img src="(.*?)" border="0" alt=".*?" width="200" class="" />', extra)
    if photo:
        data["photo"] = urlparse.urljoin(data["url"], photo[0])
    # for MPs 
    mconstituency = re.search('(?si)</h6>\s*(?:MP for (.*?)<br />)?\s*(?:PPC for (.*?)<br />)?', extra)  
    if not mconstituency:
        print "---", extra
        return
    if mconstituency.group(1):
        data["MP for"] = mconstituency.group(1)
    if mconstituency.group(2):
        data["constituency"] = RegularizeConstituency(mconstituency.group(2))
        datastore.save(unique_keys=['constituency'], data=data)
    else:
        print "MPonly  ", data
Main()

import scraperwiki
import mechanize
import re
import urlparse
from scraperwiki import datastore

def Main():
    br = mechanize.Browser()
    br.set_handle_robots(False)
    getPPCs(br)
    getMPs(br)   # currently Labour website down for MPs

def getPPCs(br):
    for i in range(1,19):
        url = "http://www.labour.org.uk/ppc?Page=%d" % i
        print "Page %d" % i, url
        page = br.open(url)
        html = page.read()
        main = re.findall('(?si)<ul class="swc_List">(.*?)</ul>', html)
        ppcs = re.findall('(?si)<li.*?>(.*?)</li>', main[0])
        for ppc in ppcs:
            data = {}
            name = re.findall('(?si)<a href=".*?".*>(.*?),.*?</a>', ppc)
            data["name"] = SimplifyHTML(name[0])
            link = re.findall('(?si)<a href="(.*?)".*>.*</a>', ppc)
            data["url"] = urlparse.urljoin(url, link[0])
            extra = br.follow_link(url_regex=link[0])
            details(extra.read(), data)
            br.back()

def getMPs(br):
    for i in range(1,19):
        url = "http://www.labour.org.uk/mp?Page=%d" % i
        print "Page %d" % i, url
        page = br.open(url)
        html = page.read()
        main = re.findall('(?si)<ul class="swc_List">(.*?)</ul>', html)
        mps = re.findall('(?si)<li.*?>(.*?)</li>', main[0])
        for mp in mps:
            data = {}
            name = re.findall('(?si)<a href=".*?".*>(.*?),.*?</a>', mp)
            data["name"] = SimplifyHTML(name[0])
            constituency_mp = re.findall('(?si)<a href=".*?".*>.*?, MP for (.*?)</a>', mp)
            if constituency_mp:
                data["constituency_mp"] = SimplifyHTML(constituency_mp[0])
            link = re.findall('(?si)<a href="(.*?)".*>.*?, MP for .*?</a>', mp)
            data["url"] = urlparse.urljoin(url, link[0])
            print mp, data["url"]
            extra = br.follow_link(url_regex=link[0])
            details(extra.read(), data)
            br.back()

            
def TWFYconstituencies():
    constituencylisturl = "http://www.theyworkforyou.com/boundaries/new-constituencies.tsv"
    constituencylist = scraperwiki.scrape(constituencylisturl)
    result = { }
    for con, r in re.findall("(.*?)\t(.*?)\n", constituencylist):
        lcon = re.sub(",", "", con)
        lcon = re.sub("-", " ", lcon).lower()
        result[lcon] = con
    return result

twfyconstituencies = TWFYconstituencies()

corrections = {'Shetland':"Orkney and Shetland", 'Orkney':"Orkney and Shetland"}  # both have same candidate
def RegularizeConstituency(lcon):
    lcon = re.sub(",", "", lcon)
    lcon = re.sub("-", " ", lcon)
    lcon = re.sub("  ", " ", lcon)
    lcon = re.sub(" &amp; ", " and ", lcon)
    lcon = re.sub(" & ", " and ", lcon)
    lcon = re.sub("(?i)\s+Clp$", "", lcon)
    lcon = corrections.get(lcon, lcon)
    return twfyconstituencies.get(lcon.lower())


def SimplifyHTML(html):
    t = html
    t = re.sub("<p><strong>(.*)</strong></p>", "==\\1==NEWLINE", t)
    t = re.sub("<p>", "NEWLINE", t)
    t = re.sub("<h2>(.*)</h2>", "NEWLINE==\\1==NEWLINE", t)
    t = re.sub("&amp;", "&", t)
    t = re.sub("&[\w#]*;?", " ", t)
    t = re.sub("(?s)<style>.*?</style>|<!--.*?-->", " ", t)
    t = re.sub("(?:<[^>]*>|\s)+", " ", t)
    t = re.sub("(?:\s*NEWLINE\s*)+", "\n\n", t).strip()
    return t

def details(extra, data):
    address = re.findall('(?si)<!-- BLOCK: PostalAddress -->\s*<strong>Write to me at:</strong><br />(.*?)<br /><br />\s*<!-- ENDBLOCK: PostalAddress -->', extra)
    if address:
        address = re.sub('\r|,', '', address[0])
        data["address"] = re.sub('\n', ' ', address)
    phone = re.findall('(?si)<!-- BLOCK: Telephone -->\s*<strong>Phone me on:</strong><br />(.*?)<br /><br />\s*<!-- ENDBLOCK: Telephone -->', extra)
    if phone:
        data["phone"] = phone[0]
    email = re.findall('(?si)<!-- BLOCK: EmailAddress -->\s*<strong>Email me at:</strong><br /><a href="mailto:(.*?)">.*?</a><br /><br />\s*<!-- ENDBLOCK: EmailAddress -->', extra)
    if email:
        data["email"] = email[0]
    website = re.findall('(?si)<!-- BLOCK: WebsiteAddress -->\s*<strong>Website address:</strong><br /><a href="(.*?)".*?>.*?</a><br /><br />\s*<!-- ENDBLOCK: WebsiteAddress -->', extra)
    if website:
        data["website"] = website[0]
    bio = re.findall('(?si)<!-- BLOCK: Biography -->\s*<div class="content_pod_content_title"><h1>.*?</h1></div>(.*?)<!-- ENDBLOCK: Biography -->', extra)
    if bio:
        data["bio"] = SimplifyHTML(bio[0])
        if re.search("Rory Palmer", data["bio"]):  # very bad formatting here
            data["bio"] = re.sub("(?s)^Rory Palmer.*?About Rory Palmer", "", data["bio"])
            data["bio"] = re.sub("==", "", data["bio"])
            data["bio"] = re.sub("\s*?\n\n\s*?", "\n\n", data["bio"]).strip()
        data["bio"] = re.sub("^Biographical Details\n\s*", "", data["bio"])
    photo = re.findall('(?si)<td valign="top" width="210"><img src="(.*?)" border="0" alt=".*?" width="200" class="" />', extra)
    if photo:
        data["photo"] = urlparse.urljoin(data["url"], photo[0])
    # for MPs 
    mconstituency = re.search('(?si)</h6>\s*(?:MP for (.*?)<br />)?\s*(?:PPC for (.*?)<br />)?', extra)  
    if not mconstituency:
        print "---", extra
        return
    if mconstituency.group(1):
        data["MP for"] = mconstituency.group(1)
    if mconstituency.group(2):
        data["constituency"] = RegularizeConstituency(mconstituency.group(2))
        datastore.save(unique_keys=['constituency'], data=data)
    else:
        print "MPonly  ", data
Main()

