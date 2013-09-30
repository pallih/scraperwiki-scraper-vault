import scraperwiki
import lxml.html
import re
import itertools

memberurl=re.compile("index.php/members/mpcvs/([0-9]+)/2010-2015") # This finds the ID of a MP

" URL Setup - These are the URLs Accessed by the Scraper "
base="http://www.parliament.go.tz/"
baseurl="http://www.parliament.go.tz/index.php/members/memberslist/all/all/2010-2015/"
detailurl=base+"index.php/members/mpcvs/%s/2010-2015"
questionurl="http://www.parliament.go.tz/index.php/sessions/questions/%s/2010-2015"
suppquestionurl="http://www.parliament.go.tz/index.php/sessions/suppquestion/%s/2010-2015"
contriburl="http://www.parliament.go.tz/index.php/sessions/contribution/%s/2010-2015"

pages=range(00,341,10)


def get_number_of_pages(url):
    """ Returns the number of pages on question and contribution urls """
    pg=scraperwiki.scrape(url)
    root=lxml.html.fromstring(pg)
    pagination=root.cssselect("#pagination")
    if not len(pagination):
        return 0
    pn=pagination[0].cssselect("a")[-1]
    pn=re.search("/([0-9]+)$",pn.get("href")).group(1)
    return int(pn)+1
    
def get_member_ids_from_page(number):
    """ gets member ids from overview lists """
    pg=scraperwiki.scrape("%s%02d"%(baseurl,number))
    return memberurl.findall(pg) # return all ids in the current page

def get_member_info(id):
    """ gets the member info """
    pg=scraperwiki.scrape(detailurl%id)
    root=lxml.html.fromstring(pg)
    table=root.cssselect("table")[1]
    minfo=dict(itertools.ifilter(lambda x: x,[extract_table_row(tr) for tr in table.cssselect("tr")]))
    """ Info from the page is done - now start further info """
    minfo["url"]=detailurl%id
    minfo["id"]=id
    minfo["questions"]=get_number_of_pages(questionurl%id)
    minfo["supplementary_questions"]=get_number_of_pages(suppquestionurl%id)
    minfo["contributions"]=get_number_of_pages(contriburl%id)
    return minfo
    
def extract_table_row(tr):
    tds=tr.cssselect("td")
    if len(tds)>1:
        return (tds[0].text_content().strip().replace(":","").replace(".",""),tds[1].text_content().strip())
    else:
        return None

""" get member ids """
members=set(reduce(lambda x,y: x+y,[get_member_ids_from_page(n) for n in pages])) # Only have each member once!

""" get member info and store it """
for id in members:
    scraperwiki.sqlite.save(unique_keys=['url','id'],data=get_member_info(id))




import scraperwiki
import lxml.html
import re
import itertools

memberurl=re.compile("index.php/members/mpcvs/([0-9]+)/2010-2015") # This finds the ID of a MP

" URL Setup - These are the URLs Accessed by the Scraper "
base="http://www.parliament.go.tz/"
baseurl="http://www.parliament.go.tz/index.php/members/memberslist/all/all/2010-2015/"
detailurl=base+"index.php/members/mpcvs/%s/2010-2015"
questionurl="http://www.parliament.go.tz/index.php/sessions/questions/%s/2010-2015"
suppquestionurl="http://www.parliament.go.tz/index.php/sessions/suppquestion/%s/2010-2015"
contriburl="http://www.parliament.go.tz/index.php/sessions/contribution/%s/2010-2015"

pages=range(00,341,10)


def get_number_of_pages(url):
    """ Returns the number of pages on question and contribution urls """
    pg=scraperwiki.scrape(url)
    root=lxml.html.fromstring(pg)
    pagination=root.cssselect("#pagination")
    if not len(pagination):
        return 0
    pn=pagination[0].cssselect("a")[-1]
    pn=re.search("/([0-9]+)$",pn.get("href")).group(1)
    return int(pn)+1
    
def get_member_ids_from_page(number):
    """ gets member ids from overview lists """
    pg=scraperwiki.scrape("%s%02d"%(baseurl,number))
    return memberurl.findall(pg) # return all ids in the current page

def get_member_info(id):
    """ gets the member info """
    pg=scraperwiki.scrape(detailurl%id)
    root=lxml.html.fromstring(pg)
    table=root.cssselect("table")[1]
    minfo=dict(itertools.ifilter(lambda x: x,[extract_table_row(tr) for tr in table.cssselect("tr")]))
    """ Info from the page is done - now start further info """
    minfo["url"]=detailurl%id
    minfo["id"]=id
    minfo["questions"]=get_number_of_pages(questionurl%id)
    minfo["supplementary_questions"]=get_number_of_pages(suppquestionurl%id)
    minfo["contributions"]=get_number_of_pages(contriburl%id)
    return minfo
    
def extract_table_row(tr):
    tds=tr.cssselect("td")
    if len(tds)>1:
        return (tds[0].text_content().strip().replace(":","").replace(".",""),tds[1].text_content().strip())
    else:
        return None

""" get member ids """
members=set(reduce(lambda x,y: x+y,[get_member_ids_from_page(n) for n in pages])) # Only have each member once!

""" get member info and store it """
for id in members:
    scraperwiki.sqlite.save(unique_keys=['url','id'],data=get_member_info(id))




