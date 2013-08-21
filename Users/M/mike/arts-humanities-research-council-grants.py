import    re
import    datetime
import    scraperwiki
import    BeautifulSoup
import    mechanize
import    urllib
import    urllib2

rootURL  = "http://www.ahrc.ac.uk/FundedResearch/BrowseResearch.aspx"

reISO    = re.compile ("([0-9]{4})-([0-9]{2})-([0-9]{2})"   )
reDMY2   = re.compile ("([0-9]{2})[-/ ]([A-Za-z]{3})[-/ ]([0-9]{2})")
reDMY4   = re.compile ("([0-9]{2})[-/ ]([A-Za-z]{3})[-/ ]([0-9]{4})")
reDMYS2  = re.compile ("([0-9]{2})[-/ ]([0-9]{2})[-/ ]([0-9]{2})"   )
reDMYS4  = re.compile ("([0-9]{2})[-/ ]([0-9]{2})[-/ ]([0-9]{4})"   )

months = \
                [
                [       '',             '0'     ],
                [       'Jan',          '1'     ],
                [       'Feb',          '2'     ],
                [       'Mar',          '3'     ],
                [       'Apr',          '4'     ],
                [       'May',          '5'     ],
                [       'Jun',          '6'     ],
                [       'Jul',          '7'     ],
                [       'Aug',          '8'     ],
                [       'Sep',          '9'     ],
                [       'Oct',          '10'    ],
                [       'Nov',          '11'    ],
                [       'Dec',          '12'    ]
                ]

def monthNameToMonth (name) :

    import string
    for month in months[1:] :
        if string.upper(name) == string.upper(month[0]) :
            return int(month[1])                         

    return 1

def canonicalDateValue (value) :

    try :
        m = reDMY4.match (value)
        g = m.groups()          
        return '%04d-%02d-%02d' % (int(g[2]), monthNameToMonth(g[1]), int(g[0]))
    except :                                                                    
        pass                                                                    

    try :
        m = reDMY2.match (value)
        g = m.groups()          
        return '%04d-%02d-%02d' % (int(g[2]) + 2000, monthNameToMonth(g[1]), int(g[0]))
    except :                                                                           
        pass                                                                           

    try :
        m = reDMYS4.match (value)
        g = m.groups()           
        return '%04d-%02d-%02d' % (int(g[2]), int(g[1]), int(g[0]))
    except :                                                       
        pass                                                       

    try :
        m = reDMYS2.match (value)
        g = m.groups()           
        return '%04d-%02d-%02d' % (int(g[2]) + 2000, int(g[1]), int(g[0]))
    except :                                                              
        pass                                                              

    return value

def ISODateValue (value) :

    try :
        m = reDMY4.match (value)
        g = m.groups()          
        return (int(g[2]), monthNameToMonth(g[1]), int(g[0]))
    except :                                                                    
        pass                                                                    

    try :
        m = reDMY2.match (value)
        g = m.groups()          
        return (int(g[2]) + 2000, monthNameToMonth(g[1]), int(g[0]))
    except :                                                                           
        pass                                                                           

    try :
        m = reDMYS4.match (value)
        g = m.groups()           
        return (int(g[2]), int(g[1]), int(g[0]))
    except :                                                       
        pass                                                       

    try :
        m = reDMYS2.match (value)
        g = m.groups()           
        return (int(g[2]) + 2000, int(g[1]), int(g[0]))
    except :                                                              
        pass                                                              

    raise Exception ("Cannot convert to ISO date: %s" % value)

def linkPage (pagePage, pageno) :
    queryArgs = \
        [
            'ctl00$AHRCScriptManager',
            'MSO_PageHashCode',
            '__SPSCEditMenu',
            'MSOWebPartPage_PostbackSource',
            'MSOTlPn_SelectedWpId',
            'MSOTlPn_View',
            'MSOTlPn_ShowSettings',
            'MSOGallery_SelectedLibrary',
            'MSOGallery_FilterString',
            'MSOTlPn_Button',
            'MSOAuthoringConsole_FormContext',
            'MSOAC_EditDuringWorkflow',
            'MSOSPWebPartManager_DisplayModeName',
            '__EVENTTARGET',
            '__EVENTARGUMENT',
            'MSOWebPartPage_Shared',
            'MSOLayout_LayoutChanges',
            'MSOLayout_InDesignMode',
            'MSOSPWebPartManager_OldDisplayModeName',
            'MSOSPWebPartManager_StartWebPartEditingName',
            '__LASTFOCUS',
            '__VIEWSTATE',
            '__VIEWSTATEENCRYPTED',
            '__EVENTVALIDATION',
            'ctl00$ctl29$txtSearchTextbox',
            'ctl00$PlaceHolderMain$query',
            'ctl00$PlaceHolderMain$ddlSchemes',
            'ctl00$PlaceHolderMain$ddlSubjects',
            'ctl00$PlaceHolderMain$txtInstitute',
            'ctl00$PlaceHolderMain$txtAwardHolder',
            'ctl00$PlaceHolderMain$ddlYears',
            'ctl00$PlaceHolderMain$txtAwardTitle',
            'hiddenInputToUpdateATBuffer_CommonToolkitScripts'
        ]
    queryWith = {}
    for key in queryArgs :
        try    : queryWith[key] = pagePage.find('input', attrs = { 'name' : key })['value']
        except : pass
    queryWith['__EVENTARGUMENT'] = 'Page$%d' % pageno
    queryWith['__EVENTTARGET'  ] = 'ctl00$PlaceHolderMain$gResults'
    return scraperwiki.scrape (rootURL, queryWith)
    
def processPage (page) :
    fundingOps = page.find ('table', attrs = { 'class' : 'fundingops' })
    for funding in fundingOps.findAll ('tr') :
        if funding.find ('th') :
            continue
        columns = funding.findAll ('td')
        try    : href    = columns[0].find('a')['href']
        except : continue
        try    : id      = re.search('id=([0-9]*)', href).group(1)
        except : continue
        ISODate = ISODateValue(columns[6].text)
        data    = \
             {   'id'             : id,
                 'title'          : columns[0].text,
                 'holder'         : columns[1].text,
                 'amount'         : columns[2].text,
                 'organisation'   : columns[3].text,
                 'subject'        : columns[4].text,
                 'scheme'         : columns[5].text,
                 'awarded'        : canonicalDateValue(columns[6].text),
                 'url'            : "http://www.ahrc.ac.uk/FundedResearch/" + href
             }
        for key in data.keys() :
            if data[key].strip() == "&nbsp;" :
                data[key] = ''
        #
        # HACK: Silent option supresses browser output. This option may disappear at
        # any time.
        #
        scraperwiki.datastore.save (unique_keys = ['id'], data = data, date = datetime.date (*ISODate), silent = False)
                                                    
# Grab and scrape the first page ...
#
pageHTML = scraperwiki.scrape(rootURL)              
pagePage = BeautifulSoup.BeautifulSoup(pageHTML)
processPage (pagePage)
 
# ... and then subsequent pages. This should continue until we run out of pages.
#
for page in range (2,10000) :
    print "Page", page
    pageHTML = linkPage (pagePage, page)
    pagePage = BeautifulSoup.BeautifulSoup(pageHTML)
    processPage (pagePage)                   
