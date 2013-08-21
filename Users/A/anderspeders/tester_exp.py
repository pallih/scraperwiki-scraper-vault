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
    page = BeautifulSoup(scraperwiki.scrape("http://ec.europa.eu/transparency/regexpert/search_results_members.cfm" % (id)))
    img_tag = page.find("img", {"class":"photoframe"})
    if img_tag:
        img = "http://ec.europa.eu/transparency/regexpert/search_results_members.cfm"+img_tag["src"]

scraperwiki.sqlite.save(["id"], info)


