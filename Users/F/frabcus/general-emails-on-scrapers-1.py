import os
import sys
import scraperwiki
import datetime


def EmailMessage(style="onlyexceptions"):
    subjectline, headerlines, bodylines, footerlines = EmailMessageParts(style)
    if bodylines:
        return "\n".join([subjectline] + headerlines + bodylines + footerlines)
    return ""


def EmailMessageParts(style="onlyexceptions"):

    # will need a wider selection of styles
    bonlyexceptions = (style == "onlyexceptions")

    escraper = os.getenv('SCRAPER_NAME')
    if not escraper:
        return "SCRAPER_NAME environment variable not set", [], [], []

    subjectline = "EMAILSUBJECT: Your Scraperwiki email - "+escraper

    watchinfo = GetWatchingInfo(escraper)

    profileid = watchinfo["profileid"]
    lastrundate = watchinfo["lastrundate"]
    if not lastrundate:
        lastrundate = str(datetime.date.today()-datetime.timedelta(1))

    bodylines = [ ]
    for scrapername in list(watchinfo["scrapersowned"]): 
        bodylines.extend(GetSummary(profileid, scrapername, lastrundate, bonlyexceptions))
    for scrapername in list(watchinfo["scrapersedited"]): 
        bodylines.extend(GetSummary(profileid, scrapername, lastrundate, bonlyexceptions))

    headerlines = [ ]
    headerlines.append("Dear %s," % watchinfo["profilename"])
    headerlines.append("")
    headerlines.append("Welcome to your personal ScraperWiki email update.")
    headerlines.append("")

    headerlines.append("Of the %d scrapers you own, and %d scrapers you have edited, we\nhave the following news since %s:" % \
                 (len(watchinfo["scrapersowned"]), len(watchinfo["scrapersedited"]), lastrundate))
    headerlines.append("")

    footerlines = [ ]
    footerlines.append("This concludes your the ScraperWiki email update till next time.")
    footerlines.append("")
    footerlines.append("Please follow this link to change how often you get these emails,")
    footerlines.append("or to unsubscribe: http://scraperwiki.com/profiles/edit/#alerts")
    return subjectline, headerlines, bodylines, footerlines



# find what scraper we are, who the user is, and what scrapers they are watching
def GetWatchingInfo(escraper):
    escraperinfo = scraperwiki.datastore.getInfo(escraper, quietfields="code")  # to get watched scrapers list
    lastrundate = None
    for rea in escraperinfo[0].get('runevents'):
        if not rea.get('still_running'):
            lastrundate = rea.get('run_started')
            break
        # could skip past blank email runobjects, 
        # definitely should skip previous email runobjects that ended in an error
        # or just use a metadata variable to report an extended range

    emailowner = escraperinfo[0]["userroles"]["owner"][0]
    userinfo = scraperwiki.datastore.getUserInfo(emailowner)
    scrapersowned = set(userinfo[0]['coderoles'].get('owner', []))
    scrapersedited = set(userinfo[0]['coderoles'].get('editor', []))
    scrapersedited.difference_update(scrapersowned)


    #scrapersowned, scrapersedited = ["python-api-functions"], []


    return {"profilename":userinfo[0]["profilename"], "profileid":emailowner, "scrapersowned":scrapersowned, "scrapersedited":scrapersedited, "lastrundate":lastrundate}


# build the summary paragraph for each chosen scraper
def GetSummary(profileid, scrapername, lastrundatetime, bonlyexceptions):
    try:
        info = scraperwiki.datastore.getInfo(scrapername, history_start_date=lastrundatetime[:10], quietfields="code|userroles")[0]
                              # we subsequently filter by >lastrundatetime after this get
    except IOError:
        return [ ]

    result = [ ]
    result.append("%s - http://scraperwiki.com/%ss/%s :" % (info.get('title'), info.get('wiki_type'), scrapername))

    # get history of edits, but don't include if you yourself edited it
    history = [ h  for h in info.get('history')  if h.get('date') >= lastrundatetime and h.get('user') != profileid ]
    
    # get history of runs of scraper, so can test broken
    runevents = [ runevent  for runevent in info.get('runevents', [])  if (runevent.get('last_update') > lastrundatetime) ]

    if history:
        users = list(set([h.get('user')  for h in history]))
        users.sort()
        result.append('   * edited %d times by %s' % (len(history), ', '.join(users)))

    if runevents and (not bonlyexceptions or runevents[0].get('exception_message')):
        records = sum([runevent.get("records_produced", 0)  for runevent in runevents])
        pages = sum([runevent.get("pages_scraped", 0)  for runevent in runevents])
        result.append('   * ran %d times producing %d records from %d pages' % (len(runevents), records, pages))
        exruns = [ runevent  for runevent in runevents  if runevent.get('exception_message') ]
        if exruns:
            result.append("   * with %d exceptions, (%s)" % (len(exruns), exruns[0].get('exception_message')))

    if len(result) == 1:
        return [ ]

    result.append("")
    return result

#EmailMessage()import os
import sys
import scraperwiki
import datetime


def EmailMessage(style="onlyexceptions"):
    subjectline, headerlines, bodylines, footerlines = EmailMessageParts(style)
    if bodylines:
        return "\n".join([subjectline] + headerlines + bodylines + footerlines)
    return ""


def EmailMessageParts(style="onlyexceptions"):

    # will need a wider selection of styles
    bonlyexceptions = (style == "onlyexceptions")

    escraper = os.getenv('SCRAPER_NAME')
    if not escraper:
        return "SCRAPER_NAME environment variable not set", [], [], []

    subjectline = "EMAILSUBJECT: Your Scraperwiki email - "+escraper

    watchinfo = GetWatchingInfo(escraper)

    profileid = watchinfo["profileid"]
    lastrundate = watchinfo["lastrundate"]
    if not lastrundate:
        lastrundate = str(datetime.date.today()-datetime.timedelta(1))

    bodylines = [ ]
    for scrapername in list(watchinfo["scrapersowned"]): 
        bodylines.extend(GetSummary(profileid, scrapername, lastrundate, bonlyexceptions))
    for scrapername in list(watchinfo["scrapersedited"]): 
        bodylines.extend(GetSummary(profileid, scrapername, lastrundate, bonlyexceptions))

    headerlines = [ ]
    headerlines.append("Dear %s," % watchinfo["profilename"])
    headerlines.append("")
    headerlines.append("Welcome to your personal ScraperWiki email update.")
    headerlines.append("")

    headerlines.append("Of the %d scrapers you own, and %d scrapers you have edited, we\nhave the following news since %s:" % \
                 (len(watchinfo["scrapersowned"]), len(watchinfo["scrapersedited"]), lastrundate))
    headerlines.append("")

    footerlines = [ ]
    footerlines.append("This concludes your the ScraperWiki email update till next time.")
    footerlines.append("")
    footerlines.append("Please follow this link to change how often you get these emails,")
    footerlines.append("or to unsubscribe: http://scraperwiki.com/profiles/edit/#alerts")
    return subjectline, headerlines, bodylines, footerlines



# find what scraper we are, who the user is, and what scrapers they are watching
def GetWatchingInfo(escraper):
    escraperinfo = scraperwiki.datastore.getInfo(escraper, quietfields="code")  # to get watched scrapers list
    lastrundate = None
    for rea in escraperinfo[0].get('runevents'):
        if not rea.get('still_running'):
            lastrundate = rea.get('run_started')
            break
        # could skip past blank email runobjects, 
        # definitely should skip previous email runobjects that ended in an error
        # or just use a metadata variable to report an extended range

    emailowner = escraperinfo[0]["userroles"]["owner"][0]
    userinfo = scraperwiki.datastore.getUserInfo(emailowner)
    scrapersowned = set(userinfo[0]['coderoles'].get('owner', []))
    scrapersedited = set(userinfo[0]['coderoles'].get('editor', []))
    scrapersedited.difference_update(scrapersowned)


    #scrapersowned, scrapersedited = ["python-api-functions"], []


    return {"profilename":userinfo[0]["profilename"], "profileid":emailowner, "scrapersowned":scrapersowned, "scrapersedited":scrapersedited, "lastrundate":lastrundate}


# build the summary paragraph for each chosen scraper
def GetSummary(profileid, scrapername, lastrundatetime, bonlyexceptions):
    try:
        info = scraperwiki.datastore.getInfo(scrapername, history_start_date=lastrundatetime[:10], quietfields="code|userroles")[0]
                              # we subsequently filter by >lastrundatetime after this get
    except IOError:
        return [ ]

    result = [ ]
    result.append("%s - http://scraperwiki.com/%ss/%s :" % (info.get('title'), info.get('wiki_type'), scrapername))

    # get history of edits, but don't include if you yourself edited it
    history = [ h  for h in info.get('history')  if h.get('date') >= lastrundatetime and h.get('user') != profileid ]
    
    # get history of runs of scraper, so can test broken
    runevents = [ runevent  for runevent in info.get('runevents', [])  if (runevent.get('last_update') > lastrundatetime) ]

    if history:
        users = list(set([h.get('user')  for h in history]))
        users.sort()
        result.append('   * edited %d times by %s' % (len(history), ', '.join(users)))

    if runevents and (not bonlyexceptions or runevents[0].get('exception_message')):
        records = sum([runevent.get("records_produced", 0)  for runevent in runevents])
        pages = sum([runevent.get("pages_scraped", 0)  for runevent in runevents])
        result.append('   * ran %d times producing %d records from %d pages' % (len(runevents), records, pages))
        exruns = [ runevent  for runevent in runevents  if runevent.get('exception_message') ]
        if exruns:
            result.append("   * with %d exceptions, (%s)" % (len(exruns), exruns[0].get('exception_message')))

    if len(result) == 1:
        return [ ]

    result.append("")
    return result

#EmailMessage()