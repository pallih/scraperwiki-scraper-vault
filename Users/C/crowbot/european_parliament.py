import scraperwiki
from BeautifulSoup import BeautifulSoup

def strip_comments(s):
    start = s.find("<!--")
    if start == -1:
        return s # No comments
    end = s.find("-->", start)+3
    return s[:start]+strip_comments(s[end:])
def strip_tags(s):
    start = s.find("<")
    if start == -1:
        return s # No tags
    end = s.find(">", start)+1
    return s[:start]+strip_tags(s[end:])
def repl_html_entities(s):
    start = s.find("&#")
    if start == -1:
        return s # No entities
    end = s.find(";", start)
    return s[:start]+unichr(int(s[start+2:end]))+repl_html_entities(s[end+1:])
def get_email(s):
    return repl_html_entities(strip_tags(strip_comments(str(s))))

def get_memberships(table):
    table_rows = table.findAll("tr", {"class":"mep_CVtext"})
    memberships = []
    for row in table_rows:
        if len(row.findAll("td")) == 2:
            print "adding %s" % row.findAll("td")[1].contents[0]
            memberships.append(row.findAll("td")[1].contents[0].strip())
    return memberships

def scrape_member(id):
    page = BeautifulSoup(scraperwiki.scrape("http://www.europarl.europa.eu/members/expert/alphaOrder/view.do?language=EN&id=%d" % (id)))
    img_tag = page.find("img", {"class":"photoframe"})
    if img_tag:
        img = "http://www.europarl.europa.eu"+img_tag["src"]
    else:
        img = None
    name = page.find("td", {"class":"mepname"}).string.strip()
    fraction = page.find("span", {"class":"titlemep"}).string
    country = page.find("table", {"class":"titlemep"}).findAll("td")[1].string
    details_tables = page.findAll("table", {"width":"80%"})
    print "got details tables" 
    headers = []
    for details_table in details_tables:
        headers.append(details_table.find("td", {"class":"mepcountry"}))
    committee_memberships = []
    committee_substitute_memberships = []
    for header in headers:
        #print header.contents
        #print header.string
        
        if header and header.string.strip() == 'Member':
            print "ctte member table"
            committee_table = header.parent.parent.parent
            committee_memberships = get_memberships(committee_table)
        if header and header.string.strip() == 'Substitute':        
            print "ctte subs table"
            committee_sub_table = header.parent.parent.parent
            committee_substitute_memberships = get_memberships(committee_sub_table)

    
    mail = get_email(page.find("td", {"class":"mepmail"}).find("a"))
    info = {
        "id":id,
        "img":img,
        "name":name,
        "fraction":fraction,
        "country":country,
        "mail":mail,
        "committee_memberships": committee_memberships,
        "committee_substitute_memberships": committee_substitute_memberships,
    }
    scraperwiki.sqlite.save(["id"], info)


index_page = BeautifulSoup(scraperwiki.scrape("http://www.europarl.europa.eu/members/expert/alphaOrder.do?language=EN"))
members = []
for m in index_page.find("td", {"class":"box_content_mep"}).findAll("td", {"class":"listcontentlight_left"})+index_page.find("td", {"class":"box_content_mep"}).findAll("td", {"class":"listcontentdark_left"}):
    s = m.find("a")["href"]
    name = m.find("a").string
    print name
    start = s.find("&id=")+4
    id = int(s[start:])
    existing = scraperwiki.sqlite.select("id from swdata where id = %s" % id)
    if len(existing) == 0:
        scrape_member(id)

for letter in index_page.findAll("a", {"class":"selector_lnk"}):
    
    index_page = BeautifulSoup(scraperwiki.scrape("http://www.europarl.europa.eu/members/expert/alphaOrder.do?letter=%s&language=EN" % (letter.string)))
    for m in index_page.find("td", {"class":"box_content_mep"}).findAll("td", {"class":"listcontentlight_left"})+index_page.find("td", {"class":"box_content_mep"}).findAll("td", {"class":"listcontentdark_left"}):
        s = m.find("a")["href"]
        start = s.find("&id=")+4
        id = int(s[start:])
        existing = scraperwiki.sqlite.select("id from swdata where id = %s" % id)
        if len(existing) == 0:
            scrape_member(id)
import scraperwiki
from BeautifulSoup import BeautifulSoup

def strip_comments(s):
    start = s.find("<!--")
    if start == -1:
        return s # No comments
    end = s.find("-->", start)+3
    return s[:start]+strip_comments(s[end:])
def strip_tags(s):
    start = s.find("<")
    if start == -1:
        return s # No tags
    end = s.find(">", start)+1
    return s[:start]+strip_tags(s[end:])
def repl_html_entities(s):
    start = s.find("&#")
    if start == -1:
        return s # No entities
    end = s.find(";", start)
    return s[:start]+unichr(int(s[start+2:end]))+repl_html_entities(s[end+1:])
def get_email(s):
    return repl_html_entities(strip_tags(strip_comments(str(s))))

def get_memberships(table):
    table_rows = table.findAll("tr", {"class":"mep_CVtext"})
    memberships = []
    for row in table_rows:
        if len(row.findAll("td")) == 2:
            print "adding %s" % row.findAll("td")[1].contents[0]
            memberships.append(row.findAll("td")[1].contents[0].strip())
    return memberships

def scrape_member(id):
    page = BeautifulSoup(scraperwiki.scrape("http://www.europarl.europa.eu/members/expert/alphaOrder/view.do?language=EN&id=%d" % (id)))
    img_tag = page.find("img", {"class":"photoframe"})
    if img_tag:
        img = "http://www.europarl.europa.eu"+img_tag["src"]
    else:
        img = None
    name = page.find("td", {"class":"mepname"}).string.strip()
    fraction = page.find("span", {"class":"titlemep"}).string
    country = page.find("table", {"class":"titlemep"}).findAll("td")[1].string
    details_tables = page.findAll("table", {"width":"80%"})
    print "got details tables" 
    headers = []
    for details_table in details_tables:
        headers.append(details_table.find("td", {"class":"mepcountry"}))
    committee_memberships = []
    committee_substitute_memberships = []
    for header in headers:
        #print header.contents
        #print header.string
        
        if header and header.string.strip() == 'Member':
            print "ctte member table"
            committee_table = header.parent.parent.parent
            committee_memberships = get_memberships(committee_table)
        if header and header.string.strip() == 'Substitute':        
            print "ctte subs table"
            committee_sub_table = header.parent.parent.parent
            committee_substitute_memberships = get_memberships(committee_sub_table)

    
    mail = get_email(page.find("td", {"class":"mepmail"}).find("a"))
    info = {
        "id":id,
        "img":img,
        "name":name,
        "fraction":fraction,
        "country":country,
        "mail":mail,
        "committee_memberships": committee_memberships,
        "committee_substitute_memberships": committee_substitute_memberships,
    }
    scraperwiki.sqlite.save(["id"], info)


index_page = BeautifulSoup(scraperwiki.scrape("http://www.europarl.europa.eu/members/expert/alphaOrder.do?language=EN"))
members = []
for m in index_page.find("td", {"class":"box_content_mep"}).findAll("td", {"class":"listcontentlight_left"})+index_page.find("td", {"class":"box_content_mep"}).findAll("td", {"class":"listcontentdark_left"}):
    s = m.find("a")["href"]
    name = m.find("a").string
    print name
    start = s.find("&id=")+4
    id = int(s[start:])
    existing = scraperwiki.sqlite.select("id from swdata where id = %s" % id)
    if len(existing) == 0:
        scrape_member(id)

for letter in index_page.findAll("a", {"class":"selector_lnk"}):
    
    index_page = BeautifulSoup(scraperwiki.scrape("http://www.europarl.europa.eu/members/expert/alphaOrder.do?letter=%s&language=EN" % (letter.string)))
    for m in index_page.find("td", {"class":"box_content_mep"}).findAll("td", {"class":"listcontentlight_left"})+index_page.find("td", {"class":"box_content_mep"}).findAll("td", {"class":"listcontentdark_left"}):
        s = m.find("a")["href"]
        start = s.find("&id=")+4
        id = int(s[start:])
        existing = scraperwiki.sqlite.select("id from swdata where id = %s" % id)
        if len(existing) == 0:
            scrape_member(id)
