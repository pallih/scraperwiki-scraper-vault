"""Finds the Annual Average Daily Traffic Flows for sets of roads, scraping by council area"""
import mechanize
import scraperwiki
import csv
import datetime
import traceback
import os

from scraperwiki import log

#### This scraper is now out of date.  
#### The new place to get the data is http://www.dft.gov.uk/matrix/Search.aspx
#### and it requires f***ing javascript and is very irritating, as well as being broken!!!

# data is in bottom part of CSV file.  
# the following are type int, though the sums don't seem to add up
intparams = [ 'PC', '2WMV', 'CAR', 'BUS', 'LGV', 'HGVR2', 'HGVR3', 'HGVR4', 'HGVA3', 'HGVA5', 'HGVA6', 'HGV' ]


# Fields defined at: http://www.dft.gov.uk/matrix/Forms/Definitions.aspx
#  'RName', 'LACode', 'LName',
#  'CP'                              Count point,
#  'Road',
#  'RdSeq', 'Street', 'RCatName',
#  'LenNet',
#  'dOpened'                         Date road link opened,
#  'dClosed'                         Date road link closed,
#  'SRefE', 'SRefN'                  OS Grid references,
#  'Year',
#  'PC'                              Pedal cycles,
#  '2WMV', 'CAR', 'BUS', 'LGV', 'HGVR2',
#  'HGVR3', 'HGVR4', 'HGVA3', 'HGVA5', 'HGVA6',
#  'HGV',
#  'All_MV'
def FixParamsSave(params):
    easting = int(params['SRefE'])
    northing = int(params['SRefN'])
    params["location"] = "OSEastingNorthing(%d, %d)" % (easting, northing)
    params["latlng"] = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
    del params['SRefE']
    del params['SRefN']
    
    scraperwiki.datastore.save(unique_keys=["CP", "Year"], data=params)


# goes into the save CSV link, pulls out all the rows, and goes back to the select council page
def FetchData(br):
    br.select_form(name="Form1")
    fin = br.submit("saveToCSV")
    cc = list(csv.reader(fin.readlines()))
    ih = 23
    assert len(cc[ih]) == 27 and cc[ih][0] == "RName", cc[ih]
    for n, c in enumerate(cc[ih+1:]):   # make this :50 to execute faster by looking at the first few records
        assert len(c) == len(cc[ih]), c
        params = dict(zip(cc[ih], c))
        FixParamsSave(params)
    br.back()
    br.back()
    return n
    
    
# prepare mechanize to look up by local authority
def SetupBrowserSearch():
    br = mechanize.Browser()
    br.addheaders = [ [ 'x-runid', os.environ['RUNID'] ] ]
    br.open("http://www.dft.gov.uk/matrix/forms/search.aspx")
    br.set_handle_robots(False)
    
    br.select_form(name="Form1")
    br["ddlSearchType"] = ["LA"]
    br.submit("btnUpdateSearch")   # one of several submit buttons.  This reloads the page, but with the ability to select by local authority
    return br

# finds the next unscraped council and selects it   
def SelectCouncilArea(br, iLA):
    br.select_form(name="Form1")
    ddlLA = br.find_control("ddlLA")

    print "number of LAs", len(ddlLA.items)

    #br["ddlSearchYear"] = ["ALL"]   # to download all, not just last year
    
    ddlLAchosen = ddlLA.items[iLA]
    
    log("Roads for iLA=%d %s in position " % (iLA, ddlLAchosen.attrs["contents"]))
    ddlLA.value = [ ddlLAchosen.name ]
    br.submit("doLASearch")


# the main loop (this could go on to do the whole set, or just do once and do the next council next time
def ScrapeAADTFdata():
    log("start")
    
    br = SetupBrowserSearch()
    for iLA in xrange(100, 105):  # there are 204 LAs -- edit this to spread the load
        SelectCouncilArea(br, iLA)
        n = FetchData(br)
        log("  saved %d records" % n)
    log("bye")
    


# main function
ScrapeAADTFdata()
"""Finds the Annual Average Daily Traffic Flows for sets of roads, scraping by council area"""
import mechanize
import scraperwiki
import csv
import datetime
import traceback
import os

from scraperwiki import log

#### This scraper is now out of date.  
#### The new place to get the data is http://www.dft.gov.uk/matrix/Search.aspx
#### and it requires f***ing javascript and is very irritating, as well as being broken!!!

# data is in bottom part of CSV file.  
# the following are type int, though the sums don't seem to add up
intparams = [ 'PC', '2WMV', 'CAR', 'BUS', 'LGV', 'HGVR2', 'HGVR3', 'HGVR4', 'HGVA3', 'HGVA5', 'HGVA6', 'HGV' ]


# Fields defined at: http://www.dft.gov.uk/matrix/Forms/Definitions.aspx
#  'RName', 'LACode', 'LName',
#  'CP'                              Count point,
#  'Road',
#  'RdSeq', 'Street', 'RCatName',
#  'LenNet',
#  'dOpened'                         Date road link opened,
#  'dClosed'                         Date road link closed,
#  'SRefE', 'SRefN'                  OS Grid references,
#  'Year',
#  'PC'                              Pedal cycles,
#  '2WMV', 'CAR', 'BUS', 'LGV', 'HGVR2',
#  'HGVR3', 'HGVR4', 'HGVA3', 'HGVA5', 'HGVA6',
#  'HGV',
#  'All_MV'
def FixParamsSave(params):
    easting = int(params['SRefE'])
    northing = int(params['SRefN'])
    params["location"] = "OSEastingNorthing(%d, %d)" % (easting, northing)
    params["latlng"] = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
    del params['SRefE']
    del params['SRefN']
    
    scraperwiki.datastore.save(unique_keys=["CP", "Year"], data=params)


# goes into the save CSV link, pulls out all the rows, and goes back to the select council page
def FetchData(br):
    br.select_form(name="Form1")
    fin = br.submit("saveToCSV")
    cc = list(csv.reader(fin.readlines()))
    ih = 23
    assert len(cc[ih]) == 27 and cc[ih][0] == "RName", cc[ih]
    for n, c in enumerate(cc[ih+1:]):   # make this :50 to execute faster by looking at the first few records
        assert len(c) == len(cc[ih]), c
        params = dict(zip(cc[ih], c))
        FixParamsSave(params)
    br.back()
    br.back()
    return n
    
    
# prepare mechanize to look up by local authority
def SetupBrowserSearch():
    br = mechanize.Browser()
    br.addheaders = [ [ 'x-runid', os.environ['RUNID'] ] ]
    br.open("http://www.dft.gov.uk/matrix/forms/search.aspx")
    br.set_handle_robots(False)
    
    br.select_form(name="Form1")
    br["ddlSearchType"] = ["LA"]
    br.submit("btnUpdateSearch")   # one of several submit buttons.  This reloads the page, but with the ability to select by local authority
    return br

# finds the next unscraped council and selects it   
def SelectCouncilArea(br, iLA):
    br.select_form(name="Form1")
    ddlLA = br.find_control("ddlLA")

    print "number of LAs", len(ddlLA.items)

    #br["ddlSearchYear"] = ["ALL"]   # to download all, not just last year
    
    ddlLAchosen = ddlLA.items[iLA]
    
    log("Roads for iLA=%d %s in position " % (iLA, ddlLAchosen.attrs["contents"]))
    ddlLA.value = [ ddlLAchosen.name ]
    br.submit("doLASearch")


# the main loop (this could go on to do the whole set, or just do once and do the next council next time
def ScrapeAADTFdata():
    log("start")
    
    br = SetupBrowserSearch()
    for iLA in xrange(100, 105):  # there are 204 LAs -- edit this to spread the load
        SelectCouncilArea(br, iLA)
        n = FetchData(br)
        log("  saved %d records" % n)
    log("bye")
    


# main function
ScrapeAADTFdata()
"""Finds the Annual Average Daily Traffic Flows for sets of roads, scraping by council area"""
import mechanize
import scraperwiki
import csv
import datetime
import traceback
import os

from scraperwiki import log

#### This scraper is now out of date.  
#### The new place to get the data is http://www.dft.gov.uk/matrix/Search.aspx
#### and it requires f***ing javascript and is very irritating, as well as being broken!!!

# data is in bottom part of CSV file.  
# the following are type int, though the sums don't seem to add up
intparams = [ 'PC', '2WMV', 'CAR', 'BUS', 'LGV', 'HGVR2', 'HGVR3', 'HGVR4', 'HGVA3', 'HGVA5', 'HGVA6', 'HGV' ]


# Fields defined at: http://www.dft.gov.uk/matrix/Forms/Definitions.aspx
#  'RName', 'LACode', 'LName',
#  'CP'                              Count point,
#  'Road',
#  'RdSeq', 'Street', 'RCatName',
#  'LenNet',
#  'dOpened'                         Date road link opened,
#  'dClosed'                         Date road link closed,
#  'SRefE', 'SRefN'                  OS Grid references,
#  'Year',
#  'PC'                              Pedal cycles,
#  '2WMV', 'CAR', 'BUS', 'LGV', 'HGVR2',
#  'HGVR3', 'HGVR4', 'HGVA3', 'HGVA5', 'HGVA6',
#  'HGV',
#  'All_MV'
def FixParamsSave(params):
    easting = int(params['SRefE'])
    northing = int(params['SRefN'])
    params["location"] = "OSEastingNorthing(%d, %d)" % (easting, northing)
    params["latlng"] = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
    del params['SRefE']
    del params['SRefN']
    
    scraperwiki.datastore.save(unique_keys=["CP", "Year"], data=params)


# goes into the save CSV link, pulls out all the rows, and goes back to the select council page
def FetchData(br):
    br.select_form(name="Form1")
    fin = br.submit("saveToCSV")
    cc = list(csv.reader(fin.readlines()))
    ih = 23
    assert len(cc[ih]) == 27 and cc[ih][0] == "RName", cc[ih]
    for n, c in enumerate(cc[ih+1:]):   # make this :50 to execute faster by looking at the first few records
        assert len(c) == len(cc[ih]), c
        params = dict(zip(cc[ih], c))
        FixParamsSave(params)
    br.back()
    br.back()
    return n
    
    
# prepare mechanize to look up by local authority
def SetupBrowserSearch():
    br = mechanize.Browser()
    br.addheaders = [ [ 'x-runid', os.environ['RUNID'] ] ]
    br.open("http://www.dft.gov.uk/matrix/forms/search.aspx")
    br.set_handle_robots(False)
    
    br.select_form(name="Form1")
    br["ddlSearchType"] = ["LA"]
    br.submit("btnUpdateSearch")   # one of several submit buttons.  This reloads the page, but with the ability to select by local authority
    return br

# finds the next unscraped council and selects it   
def SelectCouncilArea(br, iLA):
    br.select_form(name="Form1")
    ddlLA = br.find_control("ddlLA")

    print "number of LAs", len(ddlLA.items)

    #br["ddlSearchYear"] = ["ALL"]   # to download all, not just last year
    
    ddlLAchosen = ddlLA.items[iLA]
    
    log("Roads for iLA=%d %s in position " % (iLA, ddlLAchosen.attrs["contents"]))
    ddlLA.value = [ ddlLAchosen.name ]
    br.submit("doLASearch")


# the main loop (this could go on to do the whole set, or just do once and do the next council next time
def ScrapeAADTFdata():
    log("start")
    
    br = SetupBrowserSearch()
    for iLA in xrange(100, 105):  # there are 204 LAs -- edit this to spread the load
        SelectCouncilArea(br, iLA)
        n = FetchData(br)
        log("  saved %d records" % n)
    log("bye")
    


# main function
ScrapeAADTFdata()
"""Finds the Annual Average Daily Traffic Flows for sets of roads, scraping by council area"""
import mechanize
import scraperwiki
import csv
import datetime
import traceback
import os

from scraperwiki import log

#### This scraper is now out of date.  
#### The new place to get the data is http://www.dft.gov.uk/matrix/Search.aspx
#### and it requires f***ing javascript and is very irritating, as well as being broken!!!

# data is in bottom part of CSV file.  
# the following are type int, though the sums don't seem to add up
intparams = [ 'PC', '2WMV', 'CAR', 'BUS', 'LGV', 'HGVR2', 'HGVR3', 'HGVR4', 'HGVA3', 'HGVA5', 'HGVA6', 'HGV' ]


# Fields defined at: http://www.dft.gov.uk/matrix/Forms/Definitions.aspx
#  'RName', 'LACode', 'LName',
#  'CP'                              Count point,
#  'Road',
#  'RdSeq', 'Street', 'RCatName',
#  'LenNet',
#  'dOpened'                         Date road link opened,
#  'dClosed'                         Date road link closed,
#  'SRefE', 'SRefN'                  OS Grid references,
#  'Year',
#  'PC'                              Pedal cycles,
#  '2WMV', 'CAR', 'BUS', 'LGV', 'HGVR2',
#  'HGVR3', 'HGVR4', 'HGVA3', 'HGVA5', 'HGVA6',
#  'HGV',
#  'All_MV'
def FixParamsSave(params):
    easting = int(params['SRefE'])
    northing = int(params['SRefN'])
    params["location"] = "OSEastingNorthing(%d, %d)" % (easting, northing)
    params["latlng"] = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
    del params['SRefE']
    del params['SRefN']
    
    scraperwiki.datastore.save(unique_keys=["CP", "Year"], data=params)


# goes into the save CSV link, pulls out all the rows, and goes back to the select council page
def FetchData(br):
    br.select_form(name="Form1")
    fin = br.submit("saveToCSV")
    cc = list(csv.reader(fin.readlines()))
    ih = 23
    assert len(cc[ih]) == 27 and cc[ih][0] == "RName", cc[ih]
    for n, c in enumerate(cc[ih+1:]):   # make this :50 to execute faster by looking at the first few records
        assert len(c) == len(cc[ih]), c
        params = dict(zip(cc[ih], c))
        FixParamsSave(params)
    br.back()
    br.back()
    return n
    
    
# prepare mechanize to look up by local authority
def SetupBrowserSearch():
    br = mechanize.Browser()
    br.addheaders = [ [ 'x-runid', os.environ['RUNID'] ] ]
    br.open("http://www.dft.gov.uk/matrix/forms/search.aspx")
    br.set_handle_robots(False)
    
    br.select_form(name="Form1")
    br["ddlSearchType"] = ["LA"]
    br.submit("btnUpdateSearch")   # one of several submit buttons.  This reloads the page, but with the ability to select by local authority
    return br

# finds the next unscraped council and selects it   
def SelectCouncilArea(br, iLA):
    br.select_form(name="Form1")
    ddlLA = br.find_control("ddlLA")

    print "number of LAs", len(ddlLA.items)

    #br["ddlSearchYear"] = ["ALL"]   # to download all, not just last year
    
    ddlLAchosen = ddlLA.items[iLA]
    
    log("Roads for iLA=%d %s in position " % (iLA, ddlLAchosen.attrs["contents"]))
    ddlLA.value = [ ddlLAchosen.name ]
    br.submit("doLASearch")


# the main loop (this could go on to do the whole set, or just do once and do the next council next time
def ScrapeAADTFdata():
    log("start")
    
    br = SetupBrowserSearch()
    for iLA in xrange(100, 105):  # there are 204 LAs -- edit this to spread the load
        SelectCouncilArea(br, iLA)
        n = FetchData(br)
        log("  saved %d records" % n)
    log("bye")
    


# main function
ScrapeAADTFdata()
