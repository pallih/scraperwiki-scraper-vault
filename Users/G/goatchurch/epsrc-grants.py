import scraperwiki
import urllib
import re
import time
import datetime

#from scraperwiki import log

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# backup when page_cache exists
def Scrape(tag, name, url):
#    text = scraperwiki.page_cache.getpagebyname(name)
#    if text != None:
#        return text
    
    fin = urllib.urlopen(url)
    text = fin.read()
    fin.close()

#    scraperwiki.page_cache.savepage(tag, name, text)

    return text


# get the list of recent grants from latest page
def RecentGrantRefs():
    grantrefs = [ ]

    text = Scrape("tag", "latest", "http://gow.epsrc.ac.uk/ListGrants.aspx?mode=Latest")

    mtab = re.search('(?s)<tr class="GridHeader">.*?</tr>(.*?)</table>', text)
    rows = re.findall("(?s)<tr.*?>(.*?)</tr>", mtab.group(1))
    for row in rows:
        # [id/title, researcher, university, amount, date]
        cols = [ col.strip()  for col in re.findall("(?s)<td.*?>(.*?)</td>", row) ]
        mgrantid = re.match('<a title="((?:EP|DT).*?)" href="(ViewGrant.aspx.*?)>(.*?)</a>', cols[0])
        grantref, grantlink, granttitle = mgrantid.groups()
                        
        grantrefs.append(grantref)
    return grantrefs


# single scrape of a page from a reference
def ScrapeGrantFromRef(grantref):
    text = Scrape("grantref", grantref, "http://gow.epsrc.ac.uk/ViewGrant.aspx?GrantRef=%s" % grantref)
          
    # Fields are ['GrantReference', 'Title', 'PrincipalInvestigator', 'Department', 'Organisation', 'AwardType', 'Starts', 'Ends', 'Value', 'Abstract', 'FinalReportSummary' ]
    data = { }
           
    # put in the attributes that are available in spans
    spanitems = re.findall('(?s)<span id="lbl(.*?)" (?:title="(.*?)" )?class="(.*?)">(?:<a href=\'(.*?)\'>)?(.*?)(?:</a>)?</span>', text)
    #<span id="lblStarts" class="DetailValue">01 January 2010</span>
    for (spanlbl, spantitle, spanclass, spanhref, spancontents) in spanitems:
        #log((spanlbl, spantitle, spanclass, spanhref, spancontents))   
        if spanlbl == "Title":
            spancontents = re.sub("</?strong>", "", spancontents)
        if spanlbl == "Abstract":
            spancontents = re.sub("(?:<br.*?>)+", "\n\n", spancontents).strip()
        if spanlbl == "PrincipalInvestigator":
            data["PrincipalInvestigatorPersonId"] = re.match("ViewPerson.aspx\?PersonId=([\-\d]+)$", spanhref).group(1)
        if spanlbl == "Value":
            spancontents = float(re.sub(",", "", spancontents))
        if spanlbl == "Starts" or spanlbl == "Ends":
            sday, smonth, syear = re.match("(\d\d)\s(\w+)\s(\d\d\d\d)$", spancontents).groups()
            simonth = months.index(smonth) + 1
            sdate = datetime.date(int(syear), simonth, int(sday))
            spancontents = sdate.strftime("%Y-%m-%d") # normal form

        data[spanlbl] = spancontents
    
    # attributes in other tables
    sectors = [ ]
    msector = re.search('(?s)<table[^>]*?summary="sector classifications">(.*?)</table>', text)
    for ssector in re.findall('<td.*?>\s*(.*?)\s*</td>', msector.group(1)):
        if ssector and not re.match("No relevance to Underpinning Sectors$", ssector):
            sectors.append(ssector.strip())
        
    if sectors:
        data["Sectors"] = sectors
    
    return data


# main loop that just looks at recent grants.  
# should do a larger loop through them all later
grantrefs = RecentGrantRefs()
for grantref in grantrefs[:15]:
    data = ScrapeGrantFromRef(grantref)
    scraperwiki.datastore.save(["GrantReference"], data)
    #log(data)
    

import scraperwiki
import urllib
import re
import time
import datetime

#from scraperwiki import log

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# backup when page_cache exists
def Scrape(tag, name, url):
#    text = scraperwiki.page_cache.getpagebyname(name)
#    if text != None:
#        return text
    
    fin = urllib.urlopen(url)
    text = fin.read()
    fin.close()

#    scraperwiki.page_cache.savepage(tag, name, text)

    return text


# get the list of recent grants from latest page
def RecentGrantRefs():
    grantrefs = [ ]

    text = Scrape("tag", "latest", "http://gow.epsrc.ac.uk/ListGrants.aspx?mode=Latest")

    mtab = re.search('(?s)<tr class="GridHeader">.*?</tr>(.*?)</table>', text)
    rows = re.findall("(?s)<tr.*?>(.*?)</tr>", mtab.group(1))
    for row in rows:
        # [id/title, researcher, university, amount, date]
        cols = [ col.strip()  for col in re.findall("(?s)<td.*?>(.*?)</td>", row) ]
        mgrantid = re.match('<a title="((?:EP|DT).*?)" href="(ViewGrant.aspx.*?)>(.*?)</a>', cols[0])
        grantref, grantlink, granttitle = mgrantid.groups()
                        
        grantrefs.append(grantref)
    return grantrefs


# single scrape of a page from a reference
def ScrapeGrantFromRef(grantref):
    text = Scrape("grantref", grantref, "http://gow.epsrc.ac.uk/ViewGrant.aspx?GrantRef=%s" % grantref)
          
    # Fields are ['GrantReference', 'Title', 'PrincipalInvestigator', 'Department', 'Organisation', 'AwardType', 'Starts', 'Ends', 'Value', 'Abstract', 'FinalReportSummary' ]
    data = { }
           
    # put in the attributes that are available in spans
    spanitems = re.findall('(?s)<span id="lbl(.*?)" (?:title="(.*?)" )?class="(.*?)">(?:<a href=\'(.*?)\'>)?(.*?)(?:</a>)?</span>', text)
    #<span id="lblStarts" class="DetailValue">01 January 2010</span>
    for (spanlbl, spantitle, spanclass, spanhref, spancontents) in spanitems:
        #log((spanlbl, spantitle, spanclass, spanhref, spancontents))   
        if spanlbl == "Title":
            spancontents = re.sub("</?strong>", "", spancontents)
        if spanlbl == "Abstract":
            spancontents = re.sub("(?:<br.*?>)+", "\n\n", spancontents).strip()
        if spanlbl == "PrincipalInvestigator":
            data["PrincipalInvestigatorPersonId"] = re.match("ViewPerson.aspx\?PersonId=([\-\d]+)$", spanhref).group(1)
        if spanlbl == "Value":
            spancontents = float(re.sub(",", "", spancontents))
        if spanlbl == "Starts" or spanlbl == "Ends":
            sday, smonth, syear = re.match("(\d\d)\s(\w+)\s(\d\d\d\d)$", spancontents).groups()
            simonth = months.index(smonth) + 1
            sdate = datetime.date(int(syear), simonth, int(sday))
            spancontents = sdate.strftime("%Y-%m-%d") # normal form

        data[spanlbl] = spancontents
    
    # attributes in other tables
    sectors = [ ]
    msector = re.search('(?s)<table[^>]*?summary="sector classifications">(.*?)</table>', text)
    for ssector in re.findall('<td.*?>\s*(.*?)\s*</td>', msector.group(1)):
        if ssector and not re.match("No relevance to Underpinning Sectors$", ssector):
            sectors.append(ssector.strip())
        
    if sectors:
        data["Sectors"] = sectors
    
    return data


# main loop that just looks at recent grants.  
# should do a larger loop through them all later
grantrefs = RecentGrantRefs()
for grantref in grantrefs[:15]:
    data = ScrapeGrantFromRef(grantref)
    scraperwiki.datastore.save(["GrantReference"], data)
    #log(data)
    

