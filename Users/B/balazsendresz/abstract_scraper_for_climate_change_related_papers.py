import scraperwiki
import requests
import lxml.html
import simplejson
import re

selectors = {
    "sagepub.com": "#p-1",
    "onlinelibrary.wiley.com": "#abstract > div",
    "tandfonline.com": ".abstract .first.last",
    "sciencemag.org": "#abstract-2 p",
    "psycnet.apa.org": "#doiAbstract",
    "sciencedirect.com": ".abstract p",
    "nature.com": ".section.first.no-nav.no-title.first-no-nav .content #first-paragraph p",
    "journals.ametsoc.org": ".abstractSection > p.last",
    "plosone.org": ".abstract",
    "onlinelibrary.wiley.com": "#abstract > div.para",
    "springerlink.com": ".Abstract > div.normal",
}

def url_springerlink(url):
    url = url.replace("http://www.springerlink.com/content/", "")
    url = re.sub(r"/.+", "", url).upper()
    return "http://www.springerlink.com/content/%s/primary" % url

url_transform = {
    "springerlink.com": url_springerlink,
}

def get_link(source):
    source = source.strip()
    link = ""
    if source[:4] == "http":
        link = source
    if source[:3] == "doi":
        link = "http://dx.doi.org/" + source[4:]
    return link

def get_abstract(url):
    url = requests.get(get_link(url)).url  # handle redirects
    for site in url_transform.keys():
        if url.find(site) != -1:
            url = url_transform[site](url)
    content = requests.get(url).text
    root = lxml.html.fromstring(content)
    selector = None
    abstract = ""
    
    for site, _selector in selectors.items():
        if url.find(site) != -1:
            selector = _selector
    if not selector:
        print "- No rule defined for this site %s" % url
        return ""
        
    try:
        for e in root.cssselect(selector):
            abstract += e.text_content().strip()            
    except Exception, e:
        print "- There was an error finding the abstract on the page: %s\n" % e

    return abstract

talkingclimate_references = "http://talkingclimate.org/django/static/references.json"
talkingclimate_references = simplejson.loads(requests.get(talkingclimate_references).text)

for ref in talkingclimate_references:
    #ref["abstract"] = ""  # uncomment for testing
    scraperwiki.sqlite.save(unique_keys=["title"], data=ref, table_name="refs")

for ref in scraperwiki.sqlite.select("* from refs where url is not null and abstract = ''"):
    if ref["url"] and not ref["abstract"]:
        print "Getting abstract for: %s - %s" % (ref["title"], ref["url"])
        ref["abstract"] = get_abstract(ref["url"])
        print "- Abstract scraped: %s" % ref["abstract"]
        scraperwiki.sqlite.save(unique_keys=["title"], data=ref, table_name="refs")
