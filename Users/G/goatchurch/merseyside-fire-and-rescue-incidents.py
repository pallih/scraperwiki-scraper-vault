"""Merseyside fire incidents"""
import scraperwiki
import re

def GetTopRecord():
    frontindex = scraperwiki.scrape("http://www.merseyfire.gov.uk/aspx/pages/Incidents/IncidentDetailsList.aspx")
    mtoprecord = re.search('<a href="IncidentDetail\.aspx\?id=(\d+)">Details</a>', frontindex)
    return int(mtoprecord.group(1))

months = {"January":1, "February":2, "March":3, "April":4, "May":5, "June":6, "July":7, "August":8, "September":9, "October":10, "November":11, "December":12}
def ConvertDate(ldate):
    mdate = re.match("\w+, (\d+) (\w+) (\d\d\d\d)", ldate)
    assert mdate, ldate
    month = mdate.group(2)
    assert month in months, ldate
    return "%s-%02d-%02d" % (mdate.group(3), months[month], int(mdate.group(1)))
    
def ScrapeRecord(r):
    print "Scraping page %d" % r, 
    url = "http://www.merseyfire.gov.uk/aspx/pages/Incidents/IncidentDetail.aspx?id=%d" % r
    text = scraperwiki.scrape(url)
    marticle = re.search('(?s)<table[^>]*?id="ctl00_ContentPlaceHolderMain_FormView1"[^>]*>(.*?)</table>', text)
    if not marticle:
        print "skipped"
        return
    mcontents = re.match("(?s)\s*<tr>\s*<td.*?>\s*(.*?)\s*</td>\s*</tr>\s*$", marticle.group(1))
    assert mcontents, marticle.group(1)
    contents = mcontents.group(1)
    paras = re.split("<br\s*/?>", contents)
    #print "ppp", paras
    
    data = { "id":r, "url":url }
    story = [ ]
    for para in paras:
        tpara = re.sub("^(?:\s|<[^>]*>)+|(?:\s|<[^>]*>)+$", "", para)
        if not tpara:
            continue
        mspanid = re.search('<span id="(.*?)">', para)
        spanid = mspanid and mspanid.group(1)
        
        if spanid == "ctl00_ContentPlaceHolderMain_FormView1_IncTitleLabel":
            data["title"] = tpara
        elif spanid == "ctl00_ContentPlaceHolderMain_FormView1_IncDateLabel":
            data["date"] = ConvertDate(tpara)
        elif spanid == "ctl00_ContentPlaceHolderMain_FormView1_IncLocationLabel":
            data["location"] = tpara
        else:
            assert not spanid or spanid == "ctl00_ContentPlaceHolderMain_FormView1_IncTextLabel", para
            story.append(tpara)
    data["story"] = "\n\n".join(tpara)
    
    scraperwiki.sqlite.save(unique_keys=["id"], data=data)
    
    
# go through the pages by their id.  too difficult to use the proper index page because the links are javascript 
# and mechanize doesn't work because the page is missing a </form> in it
toprecord = GetTopRecord()
for i in range(0, 50):
    ScrapeRecord(toprecord - i)
    

"""Merseyside fire incidents"""
import scraperwiki
import re

def GetTopRecord():
    frontindex = scraperwiki.scrape("http://www.merseyfire.gov.uk/aspx/pages/Incidents/IncidentDetailsList.aspx")
    mtoprecord = re.search('<a href="IncidentDetail\.aspx\?id=(\d+)">Details</a>', frontindex)
    return int(mtoprecord.group(1))

months = {"January":1, "February":2, "March":3, "April":4, "May":5, "June":6, "July":7, "August":8, "September":9, "October":10, "November":11, "December":12}
def ConvertDate(ldate):
    mdate = re.match("\w+, (\d+) (\w+) (\d\d\d\d)", ldate)
    assert mdate, ldate
    month = mdate.group(2)
    assert month in months, ldate
    return "%s-%02d-%02d" % (mdate.group(3), months[month], int(mdate.group(1)))
    
def ScrapeRecord(r):
    print "Scraping page %d" % r, 
    url = "http://www.merseyfire.gov.uk/aspx/pages/Incidents/IncidentDetail.aspx?id=%d" % r
    text = scraperwiki.scrape(url)
    marticle = re.search('(?s)<table[^>]*?id="ctl00_ContentPlaceHolderMain_FormView1"[^>]*>(.*?)</table>', text)
    if not marticle:
        print "skipped"
        return
    mcontents = re.match("(?s)\s*<tr>\s*<td.*?>\s*(.*?)\s*</td>\s*</tr>\s*$", marticle.group(1))
    assert mcontents, marticle.group(1)
    contents = mcontents.group(1)
    paras = re.split("<br\s*/?>", contents)
    #print "ppp", paras
    
    data = { "id":r, "url":url }
    story = [ ]
    for para in paras:
        tpara = re.sub("^(?:\s|<[^>]*>)+|(?:\s|<[^>]*>)+$", "", para)
        if not tpara:
            continue
        mspanid = re.search('<span id="(.*?)">', para)
        spanid = mspanid and mspanid.group(1)
        
        if spanid == "ctl00_ContentPlaceHolderMain_FormView1_IncTitleLabel":
            data["title"] = tpara
        elif spanid == "ctl00_ContentPlaceHolderMain_FormView1_IncDateLabel":
            data["date"] = ConvertDate(tpara)
        elif spanid == "ctl00_ContentPlaceHolderMain_FormView1_IncLocationLabel":
            data["location"] = tpara
        else:
            assert not spanid or spanid == "ctl00_ContentPlaceHolderMain_FormView1_IncTextLabel", para
            story.append(tpara)
    data["story"] = "\n\n".join(tpara)
    
    scraperwiki.sqlite.save(unique_keys=["id"], data=data)
    
    
# go through the pages by their id.  too difficult to use the proper index page because the links are javascript 
# and mechanize doesn't work because the page is missing a </form> in it
toprecord = GetTopRecord()
for i in range(0, 50):
    ScrapeRecord(toprecord - i)
    

