#Python script
#scripted by Carl Martin Burch cburch@journalism.cuny.edu

import scraperwiki

import scrapemark

global fetchnumber
fetchnumber = 0
global sessionid
sessionid = ""

def fetchsession():
    global fetchnumber
    global sessionid
    if (fetchnumber > 50) or (sessionid == ""):
        sessionurl = 'http://www.meganslaw.ca.gov/cgi/prosoma.dll?searchby=curno'
        result = scrapemark.scrape("{{ page.text }}",url=sessionurl)
        sessionid = str(result['page']['text'])
    if fetchnumber <= 50:
        fetchnumber += 1
    else:
        fetchnumber = 0
    return sessionid

# sessionid = fetchsession()

def fetchresultpage(sessionid,pagenumber,county):
    try:
        result = scrapemark.scrape("""
        <tr nowrap="" align="left" valign="top"></tr>
        {*
                <tr align='left'>
                {*
                <td align='center'></td>
                <td align='center'></td>

                <td>
                    <a href="javascript: OpenDetail('{{ [offenders].uniqueid }}')">
                        {{ [offenders].name }}
                    </a>
                </td>
{#
                <td>
                    {{ [offenders].address }}
                </td>

                <td>{{ [offenders].city }}</td>

                <td align='center'>{{ [offenders].zip }}</td>

                <td>{{ [offenders].county }}</td>

#}                    
                *}
                </tr>
        *}
        """,
        url='http://www.meganslaw.ca.gov/cgi/prosoma.dll?w6='+sessionid+'&searchby=CountyList&SelectCounty='+county+'&SB=0&PageNo='+str(pagenumber))
    except:
        return "Error"
    return result

startingpage = 1

scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS `swdata` (`uniqueid` text, `name` text)")

counties = ['SAN%20JOAQUIN']
#ALAMEDA', 'ALPINE', 'AMADOR', 'BUTTE', 'CALAVERAS', 'COLUSA', 'CONTRA%20COSTA', 'DEL%20NORTE', 'EL%20DORADO', 'FRESNO', 'GLENN', 'HUMBOLDT', 'IMPERIAL', 'INYO', 'KERN', 'KINGS', 'LAKE', 'LASSEN', 'LOS%20ANGELES', 'MADERA', 'MARIN', 'MARIPOSA', 'MENDOCINO', 'MERCED', 'MODOC', 'MONO', 'MONTEREY', 'NAPA', 'NEVADA', 'ORANGE', 'PLACER', 'PLUMAS', 'RIVERSIDE', 'SACRAMENTO', 'SAN%20BENITO', 'SAN%20BERNARDINO', 'SAN%20DIEGO', 'SAN%20FRANCISCO', 'SAN%20JOAQUIN', 'SAN%20LUIS%20OBISPO', 'SAN%20MATEO', 'SANTA%20BARBARA', 'SANTA%20CLARA', 'SANTA%20CRUZ', 'SHASTA', 'SIERRA', 'SISKIYOU', 'SOLANO', 'SONOMA', 'STANISLAUS', 'SUTTER', 'TEHAMA', 'TRINITY', 'TULARE', 'TUOLUMNE', 'VENTURA', 'YOLO', 'YUBA'

def fetchcounty(page,county): 
    while True:
         sessionid = fetchsession()
         result = fetchresultpage(sessionid,page,county)
         while (result == "Error"):
             sleep(5)
             sessionid = fetchsession()
             result = fetchresultpage(sessionid,page,county)
         try:
             if result['offenders'] == []:
                 break
             else:
                 for offender in result['offenders']:
                     offender['lookupcounty'] = county
                     # offender['address'] = offender['address'].rstrip('Show On Map')
                     scraperwiki.sqlite.save(unique_keys=["uniqueid"], data=offender)   
         except TypeError:
             break
         page += 1

for county in counties:
    fetchcounty(startingpage,county)

#Python script
#scripted by Carl Martin Burch cburch@journalism.cuny.edu

import scraperwiki

import scrapemark

global fetchnumber
fetchnumber = 0
global sessionid
sessionid = ""

def fetchsession():
    global fetchnumber
    global sessionid
    if (fetchnumber > 50) or (sessionid == ""):
        sessionurl = 'http://www.meganslaw.ca.gov/cgi/prosoma.dll?searchby=curno'
        result = scrapemark.scrape("{{ page.text }}",url=sessionurl)
        sessionid = str(result['page']['text'])
    if fetchnumber <= 50:
        fetchnumber += 1
    else:
        fetchnumber = 0
    return sessionid

# sessionid = fetchsession()

def fetchresultpage(sessionid,pagenumber,county):
    try:
        result = scrapemark.scrape("""
        <tr nowrap="" align="left" valign="top"></tr>
        {*
                <tr align='left'>
                {*
                <td align='center'></td>
                <td align='center'></td>

                <td>
                    <a href="javascript: OpenDetail('{{ [offenders].uniqueid }}')">
                        {{ [offenders].name }}
                    </a>
                </td>
{#
                <td>
                    {{ [offenders].address }}
                </td>

                <td>{{ [offenders].city }}</td>

                <td align='center'>{{ [offenders].zip }}</td>

                <td>{{ [offenders].county }}</td>

#}                    
                *}
                </tr>
        *}
        """,
        url='http://www.meganslaw.ca.gov/cgi/prosoma.dll?w6='+sessionid+'&searchby=CountyList&SelectCounty='+county+'&SB=0&PageNo='+str(pagenumber))
    except:
        return "Error"
    return result

startingpage = 1

scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS `swdata` (`uniqueid` text, `name` text)")

counties = ['SAN%20JOAQUIN']
#ALAMEDA', 'ALPINE', 'AMADOR', 'BUTTE', 'CALAVERAS', 'COLUSA', 'CONTRA%20COSTA', 'DEL%20NORTE', 'EL%20DORADO', 'FRESNO', 'GLENN', 'HUMBOLDT', 'IMPERIAL', 'INYO', 'KERN', 'KINGS', 'LAKE', 'LASSEN', 'LOS%20ANGELES', 'MADERA', 'MARIN', 'MARIPOSA', 'MENDOCINO', 'MERCED', 'MODOC', 'MONO', 'MONTEREY', 'NAPA', 'NEVADA', 'ORANGE', 'PLACER', 'PLUMAS', 'RIVERSIDE', 'SACRAMENTO', 'SAN%20BENITO', 'SAN%20BERNARDINO', 'SAN%20DIEGO', 'SAN%20FRANCISCO', 'SAN%20JOAQUIN', 'SAN%20LUIS%20OBISPO', 'SAN%20MATEO', 'SANTA%20BARBARA', 'SANTA%20CLARA', 'SANTA%20CRUZ', 'SHASTA', 'SIERRA', 'SISKIYOU', 'SOLANO', 'SONOMA', 'STANISLAUS', 'SUTTER', 'TEHAMA', 'TRINITY', 'TULARE', 'TUOLUMNE', 'VENTURA', 'YOLO', 'YUBA'

def fetchcounty(page,county): 
    while True:
         sessionid = fetchsession()
         result = fetchresultpage(sessionid,page,county)
         while (result == "Error"):
             sleep(5)
             sessionid = fetchsession()
             result = fetchresultpage(sessionid,page,county)
         try:
             if result['offenders'] == []:
                 break
             else:
                 for offender in result['offenders']:
                     offender['lookupcounty'] = county
                     # offender['address'] = offender['address'].rstrip('Show On Map')
                     scraperwiki.sqlite.save(unique_keys=["uniqueid"], data=offender)   
         except TypeError:
             break
         page += 1

for county in counties:
    fetchcounty(startingpage,county)

