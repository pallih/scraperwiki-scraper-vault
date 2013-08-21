# Scraper for the UK Employment Appeal Tribunal

# FIXME: remove excess tabs/newlines from fields, particularly dates and appeal nos.

import urllib, urllib2
import cookielib
import lxml.html
import datetime
import urlparse
import scraperwiki

def initParams(root):
    """Get the default values of form parameters.

    initParams takes as input an lxml tree - typically the conversion of an
    HTML page.  However initParams can only cope with one form, so if the page
    has multiple forms, the caller should select only the part they want. The 
    return value is a dict containing the default values of all the form fields
    that have a default value.  

    It's particularly useful for sites that use hidden form fields to manage
    user state (ASP.NET is an example).

    The intended use is:
     - use initParams to get default form contents
     - modify any fields as desired
     - urlencode the dict and pass it to your favourite HTTP library to submit the form.
    """
    fields = root.cssselect("input")
    params = {}
    for field in fields:
        v = field.get("value")
        if v is not None:
            params[field.get("name")] = v
    #print params
    return params


def getPage(base_url, params=None):
    """Fetch a page (optionally with POST data) and gently parse it.

    This is for use in an environment where navigating through search
    results is done by form submission.  Essentially it submits a form
    and gets everything ready for you to submit again.

    This is kind of like scraperwiki.scrape, except:

     - the page is converted to lxml
     - default form fields are extracted
     - the URL of the returned page is obtained.  This is the URL to which
     the next request should be sent.
    """
    if params is None:
        r=urllib2.Request(url=base_url)
    else:
        r=urllib2.Request(url=base_url,data=params)
    fin  = opener.open(r)
    page = fin.read()

    print page
    root = lxml.html.fromstring(page)
    params = initParams(root)
    return root, params, fin.geturl()

field_names=['Instrument Number','Date Filed','Document Type','Name','Associated Name','Legal Description','Book-Page','Index Status']


def getJudgments(root):
    
    myTables=root.cssselect("table")
    print len(myTables)
    trs=myTables[8].cssselect("tr")
    print len(trs)
    for tr in trs:
        tds=tr.cssselect("td")
        fields = [td.text_content() for td in tds]
        data = dict(zip(field_names, fields))
        scraperwiki.sqlite.save(unique_keys=['Instrument Number'], data=data)

    #for td in tds:
     #   print td.text_content()   
        
    # for tr in root.cssselect("table tbody tr")[0]:
      #  tds = tr.cssselect("td")
       


       # for td in tds:
        #    print td.text_content()
        
        #Skip bogus row with no elements
        #if len(tds) == 0:
         #   continue

        
        
        

        # Harvest the document url
        #try:
         #   link = tds[0].cssselect("a")
          #  link_rel = link[0].get("href")
           # link_abs = urlparse.urljoin(base_url, link_rel)
        #except IndexError:
         #   print data
          #  link_abs = ""
        #data["judgment_url"] = link_abs
        
       

def fetch(base_url, params):

    # Submit the form params to search all judgments from a given year.
    # This will just get the first page of results.
    
    #CHANGE TO CHANGE FORM LOOKUP

    #params["txtName"] = ""
    params["selDocType"]="A03"   
    params["txtDateFiledFr"]="01/01/2012"
    params["txtDateFiledTo"]="01/09/2013"
       
    
# params["cmdSearch"] = "Search"

    p=urllib.urlencode(params)
    base_url='http://rechart1.acgov.org/results.asp'
    root, params, base_url = getPage(base_url, p)
    #getJudgments(root)
   

    #Now parse the judgments, and if necessary fetch another page
    pageno=2

    while True:

        getJudgments(root)

        # This bit of code searches for a "Next" link and assumes that
        # when there's no such link, we've reached the last page
        # Note that requesting an artificially high page number just
        # returns the last page, which is a harder thing to spot.
        #quit = True
        #nextlinks = root.cssselect("a[id='pager1']")
        #for l in nextlinks:
            #if "Next" in l.text_content():
                #quit = False

        #if quit:
            #break

        #params["__EVENTARGUMENT"] = str(pageno)
        #params["__EVENTTARGET"] = "pager1"   
        new_url=base_url+'?pg='+str(pageno)
        print new_url
        p=urllib.urlencode(params)

        root, params, new_url = getPage(new_url, p)
        print "Fetched %d" % (pageno)
        pageno = pageno + 1


    print "done"

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
base_url = "http://rechart1.acgov.org"


#for year in range(1989, datetime.date.today().year):
    # Fetch the URL once to set the cookie
root, params, base_url = getPage(base_url)
base_url = "http://rechart1.acgov.org/search.asp?cabinet=opr"
root, params, base_url = getPage(base_url)
print cj
fetch(base_url, params)

