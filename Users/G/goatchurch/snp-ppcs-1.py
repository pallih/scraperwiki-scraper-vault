## SNP PPCs ##
# (julian's version, so I can delete the datastore)

# no longer existing target webpage

import mechanize
import re
import urlparse, urllib2
import scraperwiki
from scraperwiki import datastore

def Main():
    url = "http://www.snp.org/people/candidates/Westminster"

    br = mechanize.Browser()
    br.set_handle_robots(False)
    base = br.open(url)
    page = base.read()
    #print page
    candidates = re.findall('(?si)<div class=\'view-content view-content-people-candidates\'><div class="item-list"><ul>(.*?)</ul></div></div>', page)
    links = re.findall('(?si)<li>(.*?)</li>', candidates[0])
    for i, link in enumerate(links):
        data = {}
        constituency = re.findall('(?si)<a href=".*?">(.*?):.*?</a>', link)
        data["constituency"] = RegularizeConstituency(constituency[0])
        name = re.findall('(?si)<a href=".*?">.*?:\s*(.*?)</a>', link)
        data["name"] = name[0]
        ppc_link = re.findall('(?si)<a href="(.*?)">.*?:\s*.*?</a>', link)
        llink = ppc_link[0]
        if llink == "//stewarthosie":
            llink = "/stewarthosie"
        data["url"] = urlparse.urljoin(url, llink)
        black_list = ["/people/midlothian-colin-beattie", "/people/moray-angus-robertson", 
                      "/people/motherwell-wishaw-marion-fellows", "/people/ochil-south-perthshire", 
                      "/people/orkney-shetland-john-mowat"]
        print i, data["url"]
        if ppc_link[0] not in black_list:
            #extra = br.follow_link(url_regex=ppc_link[0])
            try:
                extra = urllib2.urlopen(data["url"])
                Details(extra.read(), data)
            except urllib2.HTTPError as e:
                print e
                
            #br.back()
        #print "DATA: ", data
        datastore.save(unique_keys=['constituency'], data=data)
        
def Details(extra, data):
    photo = re.findall('(?si)<div.*?class="image-attach-body"><a href=".*?"><img src="(.*?)".*?class="image image-thumbnail ".*?/></a></div>', extra)
    if photo:
        data["photo"] = photo[0]
    bio = re.findall('(?si)<div class="content">.*<h2 class=\'section\'>Biography</h2>(.*?)</div>', extra)
    if bio:
        data["bio"] = SimplifyHTML(bio[0])
    #print "BIO: ", bio

    
def SimplifyHTML(html):
    t = re.sub("<p>", "NEWLINE", html)
    t = re.sub("<h2>(.*)</h2>", "NEWLINE==\\1==NEWLINE", t)
    t = re.sub("&amp;", "&", t)
    t = re.sub("&[\w#]*;?", " ", t)
    t = re.sub("–", "-", t)
    t = re.sub("’", "'", t)
    t = re.sub(u"[‘’\x9c\x9d]", "'", t)
    t = re.sub(u"(\w)'+s", "\\1's", t)
    t = re.sub(u"''+", "\"", t)
    t = re.sub("(?s)<style>.*?</style>|<!--.*?-->", " ", t)
    t = re.sub("(?:<[^>]*>|\s)+", " ", t)
    t = re.sub("(?:\s*NEWLINE\s*)+", "\n\n", t).strip()
    return t



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

corrections = {'Paisley &amp; South Renfrewshire':"Paisley &amp; Renfrewshire South", 
                   'Paisley &amp; North Renfrewshire':"Paisley &amp; Renfrewshire North", 
                   'Dumfriesshire, Clydesdale &amp; Tweedale':"Dumfriesshire, Clydesdale &amp; Tweeddale", 
                   'West Dunbartsonshire':"West Dunbartonshire", 
                   }
def RegularizeConstituency(lcon):
    lcon = re.sub(",", "", lcon)
    lcon = re.sub("-", " ", lcon)
    lcon = re.sub("  ", " ", lcon)
    lcon = corrections.get(lcon, lcon)
    lcon = re.sub(" &amp; ", " and ", lcon)
    lcon = re.sub(" & ", " and ", lcon)
    lcon = re.sub("(?i)\s+Clp$", "", lcon)
    return twfyconstituencies.get(lcon.lower())


Main()


