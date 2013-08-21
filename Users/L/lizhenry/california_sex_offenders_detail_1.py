#Python script

import scraperwiki

import scrapemark

from time import sleep

scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS `detail` (`uniqueid` text, `status` text, `violationdate` text, `weight` text, `dob` text, `height` text, `eyecolor` text, `laterconvictions` text, `haircolor` text, `sex` text, `ethnicity` text)")

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

def fetchdetailpage(uniqueid):
    sessionid = fetchsession()
    try:
        result = scrapemark.scrape("""
                    <body>
<div class='photoBox'>

    <p class='redtextbold' style='text-align:center'>{{ [offender].status }}</p>

  </div>

    <div class='dataBox'>
            <p class='redtextbold' style='text-align:center'>
            {{ [offender].violationdate }}
            </p>

                    <ul id='ALI' class='ulLayout'>
        {*
                <li>{{ [aliases].alias }}</li>
        *}
                   </ul>

                    <table id='DES'>
                    <tbody>
                    
                    <tr><td headers='dobColHdr'>{{ [offender].dob }}</td></tr>
                    <tr><td headers='genderColHdr'>{{ [offender].sex }}</td></tr>

                    <tr><td headers='heigthColHdr'>{{ [offender].height }}</td></tr>
                    <tr><td headers='weigthColHdr'>{{ [offender].weight }}</td></tr>

                    <tr><td headers='eyecolorColHdr'>{{ [offender].eyecolor }}</td></tr>
                    <tr><td headers='haircolorColHdr'>{{ [offender].haircolor }}</td></tr>

                    <tr><td headers='ethnicityColHdr'>{{ [offender].ethnicity }}</td></tr>
                    
                    </tbody>
                    </table>

                    <table id='OFF'>
                    {*
                        <tr>
                            <td headers='offenseCodeColHdr'>
                    {{ [offense].code }}
                            </td>
                        </tr>  
                  
                        <tr>
                            <td headers='descriptionColHdr'>
                    {{ [offense].description }}
                            </td>
                        </tr>

                        <tr>
                            <td headers='lastConvictionColHdr'>
                    {{ [offense].lastconviction }}
                            </td>
                        </tr>

                        <tr>
                            <td headers='lastReleaseColHdr'>
                    {{ [offense].lastrelease }}
                            </td>
                        </tr>
                    
                    *}
                    </table>

                    
                    <center>{{ [offender].laterconvictions }}</center>

                    {*
                    <td headers="lastKnwnAddrColHdr" class="uline">{{ [addresses].address }}<br>
                    </td>
                    *}


                    <ul id='SMT' class='ulLayout'>
        {*
                <li>{{ [marks].mark }}</li>
        *}
                   </ul>
        </div>

        </body>
        """,
        url='http://www.meganslaw.ca.gov/cgi/prosoma.dll?w6='+sessionid+'&searchby=offender&id='+uniqueid)
    except urllib2.URLError:
        return "Error"
    return result

def savedetail(uniqueid,result):
    result['offender'][0]['uniqueid'] = uniqueid
    scraperwiki.sqlite.save(unique_keys=["uniqueid"],data=result['offender'],table_name="detail")
    for alias in result['aliases']:
        scraperwiki.sqlite.save(unique_keys=[],data={"uniqueid":uniqueid, "alias":alias['alias']},table_name="aliases")
    for mark in result['marks']:
        scraperwiki.sqlite.save(unique_keys=[],data={"uniqueid":uniqueid, "marks":mark['mark']},table_name="marks")
    for address in result['addresses']:
        scraperwiki.sqlite.save(unique_keys=[],data={"uniqueid":uniqueid, "addresses":address['address']},table_name="addresses")

    for offense in result['offense']:
        offense['uniqueid'] = uniqueid
        scraperwiki.sqlite.save(unique_keys=[],data=offense,table_name="offenses")

def incrementstartingvalue():
    global startingvalue
    startingvalue = startingvalue + 1
    print "Now incrementing startingvalue to:"
    print startingvalue
    scraperwiki.sqlite.save_var('startingvalue', startingvalue)

# only on first run, to reset. Then comment out.
scraperwiki.sqlite.save_var('startingvalue', 0)
scraperwiki.sqlite.attach("california_sex_offenders") 

records = scraperwiki.sqlite.select("count(*) as count from california_sex_offenders.swdata")

recordscount = records[0]['count']

global startingvalue
startingvalue = scraperwiki.sqlite.get_var('startingvalue')

print startingvalue


while startingvalue <= recordscount:
    startingvalue = scraperwiki.sqlite.get_var('startingvalue')
    uniqueidsql = scraperwiki.sqlite.select("uniqueid from california_sex_offenders.swdata order by uniqueid asc limit "+str(startingvalue)+" , 1")
    #did we get back a uniqueid or an empty result?
    if uniqueidsql == []:
        break
    # check to see if there's already data
    existingrecords = scraperwiki.sqlite.select("* from addresses where uniqueid = '"+uniqueidsql[0]['uniqueid']+"'")

    # if not, get some and write it into the database
    if existingrecords == []:
        for idrecord in uniqueidsql:
            result = fetchdetailpage(idrecord['uniqueid'])
            while (result == "Error"):
                sleep(5)
                result = fetchdetailpage(idrecord['uniqueid'])
            uniqueid = idrecord['uniqueid']
            try:
                savedetail(uniqueid,result)
                incrementstartingvalue()
            except TypeError:
                # The record's been removed
                print "No detail could be extracted from fetched page"
                incrementstartingvalue()
                continue
            except:
                sleep(5)
                savedetail(result)
    else:
        print "We've already fetched that record"
        incrementstartingvalue()
