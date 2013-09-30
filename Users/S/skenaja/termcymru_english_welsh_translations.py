import scraperwiki
from scrapemark import scrape
from datetime import datetime
import time


#GLOBALS:
base_url = "http://www.termcymru.wales.gov.uk/fulldetailse.asp?ID="
fileid = "123"
debug_yn = "Y"

#range: 1 - 48970-ish

#============================================
def debug( txt ):
    if debug_yn == "Y":
        print txt

#============================================
def GetPage ( fileid ):

    try:
        terms = ( scrape("""
            {*
    <h2>Full Details</h2>  </div>  <div class='page_summary_3col'></div>  <div class='page_content_3col'><table width='60%'><tr><td colspan='2' class='line'><font size='2'><b>English</b></font></td></tr><tr><td class='line'><font size='2'>Term</font></td><td class='line'><font size='2'>{{ [y].en_term }}</font></td></tr><tr><td class='line'><font size='2'>Definition</font></td><td class='line'><font size='2'>{{ [y].en_definition }}</font></td></tr><tr><td class='line'><font size='2'>Context</font></td><td class='line'><font size='2'>{{ [y].en_context }}</font></td></tr></table><br><table width='60%'><tr><td colspan='2' class='line'><font size='2'><b>Welsh</b></font></td></tr><tr><td class='line'><font size='2'>Term</font></td><td class='line'><font size='2'>{{ [y].cy_term }}</font></td></tr><tr><td class='line'><font size='2'>Definition</font></td><td class='line'><font size='2'>{{ [y].cy_definition }}</font></td></tr><tr><td class='line'><font size='2'>Status</font></td><td class='line'><font size='2'>{{ [y].cy_status }}</font></td></tr><tr><td class='line'><font size='2'>Part of Speech</font></td><td class='line'><font size='2'>{{ [y].cy_part_of_speech }}</font></td></tr><tr><td class='line'><font size='2'>Gender</font></td><td class='line'><font size='2'>{{ [y].cy_gender }}</font></td></tr><tr><td class='line'><font size='2'>Number</font></td><td class='line'><font size='2'>{{ [y].cy_number }}</font></td></tr><tr><td class='line'><font size='2'>Context</font></td><td class='line'><font size='2'>{{ [y].cy_context }}</font></td></tr><tr><td class='line'><font size='2'>Subject :&nbsp;</font></td><td class='line'><font size='2'>{{ [y].cy_subject }}</font></td></tr></table></div></div></div>            
            *}
            """,url=base_url+fileid))
    
        debug ((len(terms['y']), "items found"))
        debug (terms['y'])
    
        for k in terms['y']:
            k['id'] = fileid
            scraperwiki.sqlite.execute("""
                INSERT OR REPLACE INTO swdata (id, en_term, en_definition, en_context, cy_term, cy_definition, cy_status, cy_part_of_Speech, cy_gender, cy_number, cy_context, cy_subject) values (:id, :en_term, :en_definition, :en_context, :cy_term, :cy_definition, :cy_status, :cy_part_of_speech, :cy_gender, :cy_number, :cy_context, :cy_subject)
            """, k,verbose=0)
            scraperwiki.sqlite.commit()
            #scraperwiki.sqlite.save(unique_keys=fileid, data=k, table_name="swdata")
    except Exception, e:
        print e
        return

#============================================

debug ("MakeTables: start")
#scraperwiki.sqlite.execute("drop table if exists swdata") 
#scraperwiki.sqlite.execute("create table swdata (id text primary key, en_term text, en_definition text, en_context text, cy_term text, cy_definition text, cy_status text, cy_part_of_speech text, cy_gender text, cy_number text, cy_context text, cy_subject text, scrapedate text, scrapestatus text)")

# set up the data for all known id ranges (somewhere between 46-47000)
#for l in range(1,47000):
#    scraperwiki.sqlite.execute("insert or ignore into swdata (id, scrapestatus) values ('" + str(l) + "', 'NOTSCRAPED')",verbose=0)
#    scraperwiki.sqlite.commit()

#retrieve 2000 random rows to scrape
runbook = scraperwiki.sqlite.select("id from swdata where scrapestatus = 'NOTSCRAPED' order by abs(1) limit 100")
for k in runbook:    
    debug (k['id'])
    GetPage ( k['id'] )
    #time.sleep(1) #lots of timeouts being seen, so this may avoid it.



import scraperwiki
from scrapemark import scrape
from datetime import datetime
import time


#GLOBALS:
base_url = "http://www.termcymru.wales.gov.uk/fulldetailse.asp?ID="
fileid = "123"
debug_yn = "Y"

#range: 1 - 48970-ish

#============================================
def debug( txt ):
    if debug_yn == "Y":
        print txt

#============================================
def GetPage ( fileid ):

    try:
        terms = ( scrape("""
            {*
    <h2>Full Details</h2>  </div>  <div class='page_summary_3col'></div>  <div class='page_content_3col'><table width='60%'><tr><td colspan='2' class='line'><font size='2'><b>English</b></font></td></tr><tr><td class='line'><font size='2'>Term</font></td><td class='line'><font size='2'>{{ [y].en_term }}</font></td></tr><tr><td class='line'><font size='2'>Definition</font></td><td class='line'><font size='2'>{{ [y].en_definition }}</font></td></tr><tr><td class='line'><font size='2'>Context</font></td><td class='line'><font size='2'>{{ [y].en_context }}</font></td></tr></table><br><table width='60%'><tr><td colspan='2' class='line'><font size='2'><b>Welsh</b></font></td></tr><tr><td class='line'><font size='2'>Term</font></td><td class='line'><font size='2'>{{ [y].cy_term }}</font></td></tr><tr><td class='line'><font size='2'>Definition</font></td><td class='line'><font size='2'>{{ [y].cy_definition }}</font></td></tr><tr><td class='line'><font size='2'>Status</font></td><td class='line'><font size='2'>{{ [y].cy_status }}</font></td></tr><tr><td class='line'><font size='2'>Part of Speech</font></td><td class='line'><font size='2'>{{ [y].cy_part_of_speech }}</font></td></tr><tr><td class='line'><font size='2'>Gender</font></td><td class='line'><font size='2'>{{ [y].cy_gender }}</font></td></tr><tr><td class='line'><font size='2'>Number</font></td><td class='line'><font size='2'>{{ [y].cy_number }}</font></td></tr><tr><td class='line'><font size='2'>Context</font></td><td class='line'><font size='2'>{{ [y].cy_context }}</font></td></tr><tr><td class='line'><font size='2'>Subject :&nbsp;</font></td><td class='line'><font size='2'>{{ [y].cy_subject }}</font></td></tr></table></div></div></div>            
            *}
            """,url=base_url+fileid))
    
        debug ((len(terms['y']), "items found"))
        debug (terms['y'])
    
        for k in terms['y']:
            k['id'] = fileid
            scraperwiki.sqlite.execute("""
                INSERT OR REPLACE INTO swdata (id, en_term, en_definition, en_context, cy_term, cy_definition, cy_status, cy_part_of_Speech, cy_gender, cy_number, cy_context, cy_subject) values (:id, :en_term, :en_definition, :en_context, :cy_term, :cy_definition, :cy_status, :cy_part_of_speech, :cy_gender, :cy_number, :cy_context, :cy_subject)
            """, k,verbose=0)
            scraperwiki.sqlite.commit()
            #scraperwiki.sqlite.save(unique_keys=fileid, data=k, table_name="swdata")
    except Exception, e:
        print e
        return

#============================================

debug ("MakeTables: start")
#scraperwiki.sqlite.execute("drop table if exists swdata") 
#scraperwiki.sqlite.execute("create table swdata (id text primary key, en_term text, en_definition text, en_context text, cy_term text, cy_definition text, cy_status text, cy_part_of_speech text, cy_gender text, cy_number text, cy_context text, cy_subject text, scrapedate text, scrapestatus text)")

# set up the data for all known id ranges (somewhere between 46-47000)
#for l in range(1,47000):
#    scraperwiki.sqlite.execute("insert or ignore into swdata (id, scrapestatus) values ('" + str(l) + "', 'NOTSCRAPED')",verbose=0)
#    scraperwiki.sqlite.commit()

#retrieve 2000 random rows to scrape
runbook = scraperwiki.sqlite.select("id from swdata where scrapestatus = 'NOTSCRAPED' order by abs(1) limit 100")
for k in runbook:    
    debug (k['id'])
    GetPage ( k['id'] )
    #time.sleep(1) #lots of timeouts being seen, so this may avoid it.



