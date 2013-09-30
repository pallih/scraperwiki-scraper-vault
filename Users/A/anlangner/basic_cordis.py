import scraperwiki
import feedparser
import scrapemark
import lxml.html


def register_project(url):
    project_site = scraperwiki.scrape(url)
    root = lxml.html.fromstring(project_site)
    print root



    #print root.cssselect("div#projttl h1")[0]
    #print root.cssselect("div#projttl h1")[0].tail

    tmp = root.xpath("//*[@id="coord"]/div[1]/div[1]")[0]

    print tmp

    print "douh!"


applicants = ["rexroth"]

# project URL template: u'http://cordis.europa.eu/projects/rcn/105842_en.html

URL_1 = "http://cordis.europa.eu/newsearch/download.cfm?action=query&collection=EN_PROJ&text=%28"
URL_2 = "%29&sort=all&querySummary=quick&fieldText=%28MATCH%7BCORDIS%2CWEBPAGESEUROPA%7D%3ASOURCE%29&ENGINE_ID=CORDIS_ENGINE_ID&SEARCH_TYPE_ID=CORDIS_SEARCH_ID&descr="
URL_3 = ";%20Projects"


print "Number of searches: " + str(len(applicants))

#while iterator << len(applicant):

for applicant in applicants:

    print applicant
    
    list_url = URL_1 + applicant + URL_2 + applicant + URL_3
    
    atom_feed = feedparser.parse(list_url)
    
    for entry in atom_feed.entries:
        print entry.title
        print entry.link
        
        register_project (entry.link)

        print "++++"

    print "end " + applicant    



import scraperwiki
import feedparser
import scrapemark
import lxml.html


def register_project(url):
    project_site = scraperwiki.scrape(url)
    root = lxml.html.fromstring(project_site)
    print root



    #print root.cssselect("div#projttl h1")[0]
    #print root.cssselect("div#projttl h1")[0].tail

    tmp = root.xpath("//*[@id="coord"]/div[1]/div[1]")[0]

    print tmp

    print "douh!"


applicants = ["rexroth"]

# project URL template: u'http://cordis.europa.eu/projects/rcn/105842_en.html

URL_1 = "http://cordis.europa.eu/newsearch/download.cfm?action=query&collection=EN_PROJ&text=%28"
URL_2 = "%29&sort=all&querySummary=quick&fieldText=%28MATCH%7BCORDIS%2CWEBPAGESEUROPA%7D%3ASOURCE%29&ENGINE_ID=CORDIS_ENGINE_ID&SEARCH_TYPE_ID=CORDIS_SEARCH_ID&descr="
URL_3 = ";%20Projects"


print "Number of searches: " + str(len(applicants))

#while iterator << len(applicant):

for applicant in applicants:

    print applicant
    
    list_url = URL_1 + applicant + URL_2 + applicant + URL_3
    
    atom_feed = feedparser.parse(list_url)
    
    for entry in atom_feed.entries:
        print entry.title
        print entry.link
        
        register_project (entry.link)

        print "++++"

    print "end " + applicant    



