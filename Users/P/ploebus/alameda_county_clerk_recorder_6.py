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

field_names=['Entity','Name','Title','Base','Other','Gross','MDV','Er Psn','EPEPsn','DC','Misc.','TCOE']


def getJudgments(root):
    #parentStart = root.cssselect('input[name=CPIPage]')
    #print len(parentStart)
    tables= root.cssselect('table')
    x=0
    #myTables = root.xpath('//input/../../div/table')
    print len(tables)
    
    trs = tables[24].cssselect('tr')
    #print len(trs)
    for tr in trs:
        tds=tr.cssselect("td")
        fields = [td.text_content() for td in tds]
        data = dict(zip(field_names, fields))
        scraperwiki.sqlite.save(unique_keys=['Name'], data=data)
    
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
        

          


pagenoMax = 80
pageNo = 1
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

#base_url = "http://www.mercurynews.com/salaries/bay-area/2010?appSession=9284875334625&RecordID=&PageID=2&PrevPageID=&cpipage=" + pageNo + "&CPISortType=&CPIorderBy="
while pageNo< 600:
   base_url = "http://www.mercurynews.com/salaries/bay-area/2010?appSession=9284875334625&RecordID=&PageID=2&PrevPageID=&cpipage=" + str(pageNo) + "&CPISortType=&CPIorderBy="
   root, params, new_url = getPage(base_url)
   getJudgments(root)
   pageNo = pageNo + 1


