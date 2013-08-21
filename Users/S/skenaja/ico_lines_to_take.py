import urllib2
import urllib
import cookielib
import re
import scraperwiki
from scrapemark import scrape
from pprint import pprint

#GLOBALS:
base_url = "http://www.ico.gov.uk/foikb/FOIPolicyReference.htm"
base_url2 = "http://www.ico.gov.uk/foikb/PolicyLines/FOIPolicyFailuretocitespecificexceptionsectionnumber.htm"
debug_yn = "Y"

#TODO:
# - save changed/previous versions if any
# - save date scraped

# ##################################
def GetLtt( p_url ):

    ltt = ( scrape("""
        <div id="content">
        {*
        <td class="templateblock">FOI/EIR</td><td> {{ [x].legislation|html }} </td>
        <td class="templateblock">Section/Regulation</td><td> {{ [x].section|html }} </td>
        <td class="templateblock">Issue</td><td> {{ [x].issue|html }} </td>
        <td class="templateblock">Line to take:</td><td> {{ [x].ltt_intro|html }} </td>
        <td class="templateblock">Further Information:</td><td> {{ [x].ltt_further_info|html }} </td>
        <td class="templateblock">Source</td><td class="templateblock">Details</td><td> {{ [x].ltt_source|html }} </td><td> {{ [x].ltt_details|html }} </td>
        <td class="templateblock">Related Lines to Take</td><td> {{ [x].related_ltt|html }} </td>
        <td class="templateblock">Related Documents</td><td> {{ [x].ltt_related_docs|html }} </td>
        <td class="templateblock">Contact</td><td> {{ [x].ltt_contact|html }} </td>
        <td class="templateblock">Date</td><td> {{ [x].ltt_date|html }} </td>
        <td class="templateblock">Policy Reference </td><td><h4> {{ [x].ltt_id }} </h4></td>
        *}
        </div>
    """,url=p_url))

    if ltt != None:
        #although webpage is iso-8859-1, some utf-8 strings in there...

        if 'x' in ltt:
            debug ((len(ltt['x']), "items found"))
            debug (ltt['x'])

            for k in ltt['x']:
                k['ltt_status'] = "ACTIVE"
                k['date_scraped'] = ''
                k['legislation'] = k['legislation'].decode('utf-8', 'ignore')
                k['section'] = k['section'].decode('utf-8', 'ignore')
                k['issue'] = k['issue'].decode('utf-8', 'ignore')
                k['ltt_intro'] = k['ltt_intro'].decode('utf-8', 'ignore')
                k['ltt_further_info'] = k['ltt_further_info'].decode('utf-8', 'ignore')
                k['ltt_source'] = k['ltt_source'].decode('utf-8', 'ignore')
                k['ltt_details'] = k['ltt_details'].decode('utf-8', 'ignore')
                k['related_ltt'] = k['related_ltt'].decode('utf-8', 'ignore')
                k['ltt_related_docs'] = k['ltt_related_docs'].decode('utf-8', 'ignore')
                k['ltt_contact'] = k['ltt_contact'].decode('utf-8', 'ignore')
                k['ltt_date'] = k['ltt_date'].decode('utf-8', 'ignore')
                k['ltt_id'] = k['ltt_id'].decode('utf-8', 'ignore')
                k['ltt_url'] = p_url
                
                debug (type(k['ltt_related_docs']))
                scraperwiki.sqlite.save(unique_keys=["ltt_id"], data=k, table_name="ltt_data")

# ##################################
def GetListOfLtt():


    ltt = ( scrape("""
        <table>
        {*
            <td>{{ [y].ltt_id }} withdrawn</td>
        *}
        </table>
        """,url=base_url))

    if ltt != None:
        if 'y' in ltt:
            debug ((len(ltt['y']), "items found"))
            debug (ltt['y'])
            for k in ltt['y']:
                k['ltt_status'] = "WITHDRAWN"
                k['date_scraped'] = ''
                scraperwiki.sqlite.save(unique_keys=["ltt_id"], data=k, table_name="ltt_data")

    ltt = ( scrape("""
        <table>
        {*
            <td><a href='{{ [y].ltt_url|abs }}'>{{ [y].ltt_id }}</a></td>
        *}
        </table>
        """,url=base_url))

    if ltt != None:
        if 'y' in ltt:
            debug ((len(ltt['y']), "items found"))
            debug (ltt['y'])
            for k in ltt['y']:
                k['ltt_status'] = "ACTIVE"
                k['date_scraped'] = ''
                GetLtt( k['ltt_url'] )


def convert(data):
    if isinstance(data, unicode):
        return data.encode('utf-8')
    elif isinstance(data, str):
        return data.encode('utf-8')
    elif isinstance(data, dict):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, (list, tuple, set, frozenset)):
        return type(data)(map(convert, data))
    else:
        return data 

def ltt_upsert(cols):
    #grr no MERGE/UPSERT function in sqlite
    debug(cols)

    scraperwiki.sqlite.execute("""

    INSERT OR IGNORE INTO ltt_data (ltt_id, ltt_name, legislation, section, issue, ltt_intro, ltt_further_info, ltt_source,ltt_details, ltt_related_ltt, ltt_related_docs, ltt_contact, ltt_date, ltt_status, date_added, date_scraped, ltt_url ) 
    VALUES (:ltt_id, :ltt_name, :legislation, :section, :issue, :ltt_intro, :ltt_further_info, :ltt_source, :ltt_details, :ltt_related_ltt, :ltt_related_docs, :ltt_contact, :ltt_date, :ltt_status, :date_added, :date_scraped, :ltt_url)
    """, cols)

    scraperwiki.sqlite.execute("""

    UPDATE ltt_data 
    SET ltt_id = :ltt_id, ltt_name = :ltt_name, legislation = :legislation, section = :section, issue = :issue, ltt_intro = :ltt_intro, ltt_further_info = :ltt_further_info, ltt_source = :ltt_source, ltt_details = :ltt_details, ltt_related_ltt = :ltt_related_ltt, ltt_related_docs = :ltt_related_docs, ltt_contact = :ltt_contact, ltt_date = :ltt_date, ltt_status = :ltt_status, date_added = :date_added, date_scraped = :date_scraped, ltt_url = :ltt_url 
    WHERE ltt_id = :ltt_id 
    AND (ltt_name <> :ltt_name OR legislation <> :legislation OR section <> :section OR issue <> :issue OR ltt_intro <> :ltt_intro OR ltt_further_info <> :ltt_further_info OR ltt_source <> :ltt_source OR ltt_details <> :ltt_details OR ltt_related_ltt <> :ltt_related_ltt OR ltt_related_docs <> :ltt_related_docs OR ltt_contact <> :ltt_contact OR ltt_date <> :ltt_date OR ltt_status <> :ltt_status OR date_added <> :date_added OR date_scraped <> :date_scraped OR ltt_url <> :ltt_url)
    """, cols) 


    scraperwiki.sqlite.commit()


def MakeTables():
    debug ("MakeTables: start")

    scraperwiki.sqlite.execute("drop table if exists ltt_data")
    scraperwiki.sqlite.execute("create table ltt_data (ltt_id text primary key, ltt_name blob, legislation blob, section blob, issue blob, ltt_intro blob, ltt_further_info blob, ltt_source blob, ltt_details blob, related_ltt blob, ltt_related_docs blob, ltt_contact blob, ltt_date blob, ltt_status text, date_added blob, date_scraped blob, ltt_url blob)")

def debug( txt ):
    if debug_yn == "Y":
        print txt



# ##################################
#  MAIN:

print "hello"
#MakeTables()
GetListOfLtt()

#for testing:
#GetLtt( 'http://www.ico.gov.uk/foikb/PolicyLines/FOIPolicyPrejudicetocontractualrelations.htm' )



