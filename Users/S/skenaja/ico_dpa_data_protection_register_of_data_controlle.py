import urllib2
import scraperwiki
from scrapemark import scrape
from datetime import datetime
import time
from pprint import pprint


#GLOBALS:
base_url = "http://www.ico.gov.uk/ESDWebPages/DoSearch.asp?reg="
fileid = "123"
debug_yn = "Y"

#4722968 doesn't exist
#4790967 exists
#4881763 foi body

#range: 4500000 - 5200000-ish!


#============================================
def debug( txt ):
    if debug_yn == "Y":
        print txt

#============================================
def GetPage ( fileid ):

    try:
        fin = urllib2.urlopen(base_url + fileid)
        text= fin.read()
        fin.close()
    
        pprint(text)

        #test for no match    
        no_match = ( scrape("""
<hr>There are {{ }} that match your search criteria.<br>
            """,html=text))
        print no_match
        #TODO: Save no match
        #if no_match == "no entries":

        #basic details:
        basic_details = ( scrape("""
<span class=detailstext>Registration Number: {{ [y].reg_no }}</span><P><span class=detailstext>Date Registered:&nbsp;</span>{{ [y].reg_date }}&nbsp;&nbsp;&nbsp;&nbsp;<span class=detailstext>Registration Expires:&nbsp;</span>{{ [y].reg_expiry }}<br><br><span class=detailstext>Data Controller:&nbsp;</span>{{ [y].data_controller }}<P><div class=detailstext>Address:</div><Blockquote>{{ [y].reg_address|html }}</BlockQuote><hr>
            """,html=text))
        print basic_details

        debug ((len(basic_details ['y']), "items found"))
        debug (basic_details ['y'])
    
        #foi:
        foi = ( scrape("""
<P ALIGN=center class=detailstext>{{ }} or a Scottish public authority
            """,html=text))
        print foi
        #if foi == "Freedom of Information Act 2000": 

#<P class=detailstext>Other Names:</P><BlockQuote>FIRST MONEY DIRECT<br>FIRSTMONEYDIRECT.CO.UK<br></BlockQuote></BlockQuote><hr>

        
    except Exception, e:
        print e
        return



#============================================

#MAIN PROGRAM:

#TODO: build tables:

#TODO: set up seed data for querystring IDs:

#TODO: retrieve x rows to scrape:

##TEST:
#4722968 doesn't exist
#4790967 exists
#4881763 foi body
GetPage ( str(4722968) )
GetPage ( str(4790967) )
GetPage ( str(4881763) )



#============================================
# example html for info:

x=""" no match:
<hr>
There are no entries that match your search criteria.<br>
"""

x=""" with FOI:
<span class=detailstext>Registration Number: Z8583439</span><P><span class=detailstext>Date Registered:&nbsp;</span>27 October 2004 &nbsp;&nbsp;&nbsp;&nbsp;<span class=detailstext>Registration Expires:&nbsp;</span>26 October 2011<br><br><span class=detailstext>Data Controller:&nbsp;</span>CAMDEN & ISLINGTON NHS FOUNDATION TRUST<br><P><div class=detailstext>Address:</div><Blockquote>ST. PANCRAS HOSPITAL<br>4 ST. PANCRAS WAY<br>LONDON<br>NW1 0PE<br></BlockQuote></BlockQuote><hr><P ALIGN=center class=detailstext>This data controller states that it is a public authority under the<br><P ALIGN=center class=detailstext>Freedom of Information Act 2000 or a Scottish public authority under the<br><P ALIGN=center class=detailstext>Freedom of Information (Scotland) Act 2002</P><hr><P class=detailstext>This register entry describes, in very general terms, the personal data being processed by:</P>CAMDEN & ISLINGTON NHS FOUNDATION TRUST<br><P class=detailstext>
"""

x=""" without:
<P><span class=detailstext>Registration Number: Z8841249</span><P><span class=detailstext>Date Registered:&nbsp;</span>20 November 2004 &nbsp;&nbsp;&nbsp;&nbsp;<span class=detailstext>Registration Expires:&nbsp;</span>19 November 2011<br><br><span class=detailstext>Data Controller:&nbsp;</span>COVERSURE INSURANCE SERVICES (ISLINGTON)<br><P><div class=detailstext>Address:</div><Blockquote>3 DRAYTON PARK<br>LONDON<br>N5 1NU<br></BlockQuote></BlockQuote><hr><P class=detailstext>This register entry describes, in very general terms, the personal data being processed by:</P>COVERSURE INSURANCE SERVICES (ISLINGTON)<br><P class=detailstext>
"""

x=""" more than 1 name: separated by<br>
<P><span class=detailstext>Registration Number: Z2317432</span><P><span class=detailstext>Date Registered:&nbsp;</span>27 July 2010 &nbsp;&nbsp;&nbsp;&nbsp;<span class=detailstext>Registration Expires:&nbsp;</span>26 July 2011<br><br><span class=detailstext>Data Controller:&nbsp;</span>FIRST MONEY DIRECT LTD<br><P><div class=detailstext>Address:</div><Blockquote>274 CHORLEY OLD ROAD<br>BOLTON<br>BL1 4JE<br></BlockQuote><P class=detailstext>Other Names:</P><BlockQuote>FIRST MONEY DIRECT<br>FIRSTMONEYDIRECT.CO.UK<br></BlockQuote></BlockQuote><hr><P class=detailstext>This register entry describes, in very general terms, the personal data being processed by:</P>FIRST MONEY DIRECT LTD<br><P class=detailstext>
"""

