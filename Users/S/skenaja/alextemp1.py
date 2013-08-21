import scraperwiki
from scrapemark import scrape
from time import clock, time
import cookielib
from httplib import BadStatusLine 
import re

#globals
base_url = "https://delecorp.delaware.gov/tin/controller"
ua = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; rv:9.0) Gecko/20100101 Firefox/9.0", "Connection" : "keep-alive", "Host" : "delecorp.delaware.gov", "Referer" : "https://delecorp.delaware.gov/tin/GINameSearch.jsp"}
myjar = cookielib.CookieJar()
debug_yn = "Y"
batch_size = 10

#============================================
def StartUp():

    #go to homepage in order to set session cookie
    start_url = "https://delecorp.delaware.gov/tin/GINameSearch.jsp"
    p = ""
    g={"x": str(time())}
    html=""
    uastart = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; rv:9.0) Gecko/20100101 Firefox/9.0"}
    try:
        html = scrape('''
<html>
{{ [y].html }}
</html>
''', url=start_url,get=g,headers=uastart, cookie_jar=myjar )

    except BadStatusLine:
        #hmmm... will skip this check for now..
        return 0
    except Exception, e:
        debug(repr(e))
        debug("scrape problem")
        return 1

    #debug:
    debug (html)

    #Check for site down:
    sitedown = re.search("Website Closed", str(html))
    
    debug ("sitedown:" + str(sitedown))

    if sitedown:
        return 1         #exit
    else:
        return 0         #OK to continue 

#============================================
def GetPage ( fileid ):

    debug("GetPage:fileid: " + str(fileid))

    #search for a known company:
    params = {"JSPName" : "GINAMESEARCH", "action" : "Search", "frmFileNumber" : fileid, "frmEntityName" : "" }
    html=""
    try:
        html = scrape('''
<html>
{{ [y].html }}
</html>
''', url=base_url, post=params, headers=ua, cookie_jar=myjar)

    except Exception, e:
        debug(repr(e))
        debug("scrape problem")
        return 1

    #debug:
    debug(str(html))

    #test for not found
    badpage = re.search("No matches found", str(html))
    if badpage:
        debug("badpage: " + fileid)
        SaveCompanyUpsert( fileid, "", "", "", "", "", "", "BAD" )
        return 0

    #then try directly open company details page:
    params = {"JSPName" : "GINAMESEARCH", "action" : "Get Entity Details", "frmFileNumber" : fileid }

    try:
        html = scrape('''
THIS IS NOT A STATEMENT OF GOOD STANDING
{*
<TD>{{ [y] }}</TD>
*}
<B>REGISTERED AGENT INFORMATION</B>
''', url=base_url, post=params, headers=ua, cookie_jar=myjar)

    except Exception, e:
        debug(repr(e))
        debug("scrape problem")
        return 1

    #debug:
    debug(html)

    i = html['y']    
    # u'File Number:', u'2337422', 
    # u'Incorporation Date / Formation Date:', u'05/24/1993(mm/dd/yyyy)', 
    # u'Entity Name:', u'CBS OUTDOOR INC.', 
    # u'Entity Kind:', u'CORPORATION', 
    # u'Entity Type:', u'GENERAL', 
    # u'Residency:', u'DOMESTIC', 
    # u'State:', u'DE',
    #  some other stuff - can skip
    #save: i[1], i[3][:10], i[5], i[7], i[9], i[11], i[13], 
    debug ("1: " +i[1])
    debug ("1: " +i[3][:10])
    debug ("1: " +i[5])
    debug ("1: " +i[7])
    debug ("1: " +i[9])
    debug ("1: " +i[11])
    debug ("1: " +i[13])
    SaveCompanyUpsert( fileid, i[3][:10], i[5], i[7], i[9], i[11], i[13], "OK" )
    
    #back to search results:
    params = {"JSPName" : "ENTITYDETAILS", "action" : "Back to Entity Search", "frmFileNumber" : fileid}
    html = scrape('''
<html>
{{ [y].html }}
</html>
''', url=base_url, post=params, headers=ua, cookie_jar=myjar)

    #debug:
    debug(html)


#============================================
def MakeTables():

    print "MakeTables: start"
    companyfields = ["companyid text", "incorpdate text", "entityname text",  "entitykind text", "entitytype text", "residency text", "usstate text", "scrapedate text", "scrapestatus text"]
    scraperwiki.sqlite.execute("drop table if exists company")
    scraperwiki.sqlite.execute("create table company (%s, unique(companyid))" % ",".join(companyfields))
    scraperwiki.sqlite.commit()
    print "MakeTables: end"
#============================================

def PopulateCompanyTableWithIds():
    print "MakeIDTable: start"
    scraperwiki.sqlite.execute("BEGIN TRANSACTION")
    scraperwiki.sqlite.execute("pragma journal_mode = memory") #save to disk at the end
    scraperwiki.sqlite.execute("pragma synchronous = 0") 
    scraperwiki.sqlite.execute("pragma cache_size=500000")

    i_start = 1
    i_end = 1
    for largest in scraperwiki.sqlite.execute("select CASE WHEN max(cast(companyid as integer)) IS NULL THEN 0 else max(cast(companyid as integer)) end  as largest FROM company").get("data"):
        debug ("PopulateCompanyTableWithIds:largest: " + str(largest[0]))

    if largest[0] == 0:
        i_start = 1
    elif largest[0] >= 9999999:
        debug("done setting up")
        return 0
    else:
        i_start = largest[0] +1

    i_end = i_start + batch_size
    debug("i_start: " + str(i_start) + ". i_end: " + str(i_end))

    for xx in xrange(i_start, i_end):
        scraperwiki.sqlite.execute("insert into company (companyid,scrapestatus) values (?,?)", ["%07d" % xx, "NOTYET" ], verbose=0)
    #commit:
    scraperwiki.sqlite.commit()
    
    print "MakeIDTable: end"

#============================================
def SaveCompanyUpsert( p_companyid, p_incorpdate, p_entityname, p_entitykind, p_entitytype, p_residency, p_usstate, p_scrapestatus ):
    scraperwiki.sqlite.execute("UPDATE company set incorpdate = ?, entityname= ?, entitykind= ?, entitytype= ?, residency= ?, usstate= ?, scrapedate= datetime(), scrapestatus= ? WHERE companyid = ?", [p_incorpdate, p_entityname, p_entitykind, p_entitytype, p_residency, p_usstate, p_scrapestatus, p_companyid ], verbose=0)

#============================================
def GetRunInitData ():

    #begin:
    for companyid in scraperwiki.sqlite.execute("select companyid FROM company where scrapestatus = 'NOTYET' ORDER BY RANDOM() limit " + str(batch_size)).get("data"):
        debug ("GetRunInitData:companyid: " + str(companyid[0]))
        GetPage (companyid[0])
        #commit:
        scraperwiki.sqlite.commit()


#============================================
def debug( txt ):
    if debug_yn == "Y":
        print txt


#============================================
#MAIN:
debug ("Starting")
#- comment out the relevant sections depending on what's required:
#MakeTables()  ## Comment out after first run.
PopulateCompanyTableWithIds()

if (StartUp() == 1):
    pass
else:
    GetRunInitData()




#============================================
# Notes:
#"No matches found"
