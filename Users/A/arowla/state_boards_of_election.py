import scraperwiki
from lxml import html
import re
import os.path
import csv
import StringIO

try:
    swutils = scraperwiki.utils
except AttributeError:
    import gasp_helper
else:
    swutils.swimport("gasp_helper")

state_boards_csv = """AK,http://www.elections.alaska.gov/
AL,http://www.sos.state.al.us/elections/
AR,http://www.sosweb.state.ar.us/elections.html
AZ,http://www.azsos.gov/election/
CA,http://www.sos.ca.gov/elections/elections.htm
CO,http://www.elections.colorado.gov/
CT,http://www.ct.gov/sots/
DC,http://www.dcboee.org/
DE,http://elections.delaware.gov/
FL,http://election.dos.state.fl.us/
GA,http://sos.georgia.gov/elections/
HI,http://hawaii.gov/elections/
IA,http://www.sos.state.ia.us/elections/
ID,http://www.idahovotes.gov/
IL,http://www.elections.il.gov/
IN,http://www.indianavoters.com/
KS,http://www.kssos.org/elections/elections.html
KY,http://www.elect.ky.gov/
LA,http://www.sos.louisiana.gov/
MA,http://www.sec.state.ma.us/ele/
MD,http://www.elections.state.md.us/
ME,http://www.state.me.us/sos/cec/elec/
MI,http://www.michigan.gov/sos/0g1607,7-127-1633---,00.html
MN,http://www.sos.state.mn.us/home/index.asp?page=134
MO,http://www.sos.mo.gov/elections/
MS,http://www.sos.state.ms.us/elections/elections.asp
MT,http://www.montanavotes.net/
NC,http://www.sboe.state.nc.us/
NE,http://www.sos.ne.gov/elec/
NJ,http://www.njelections.org/
NM,http://www.sos.state.nm.us/sos-elections.html
NV,http://sos.state.nv.us/elections/
NY,http://www.elections.state.ny.us/
OH,http://www.sos.state.oh.us/SOS/elections.aspx
OK,http://www.ok.gov/~elections/
OR,http://www.sos.state.or.us/elections/voterresources.html
PA,http://www.votespa.com/
RI,http://www.elections.state.ri.us/
SC,http://www.scvotes.org/
SD,http://www.sdsos.gov/
TN,http://www.tn.gov/sos/election/
TX,http://www.sos.state.tx.us/elections/
UT,http://elections.utah.gov/
VA,http://www.sbe.virginia.gov/
VT,http://vermont-elections.org/
WA,http://www.secstate.wa.gov/elections/
WI,http://elections.state.wi.us/
WV,http://www.wvsos.com/elections/
ND,http://www.nd.gov/sos/electvote/
NH,http://www.sos.nh.gov/electionsnew.html
WY,http://soswy.state.wy.us/Elections/Elections.aspx
"""


state_boards = csv.reader(StringIO.StringIO(state_boards_csv))

for (state, url) in state_boards:
    state_str = scraperwiki.scrape(url)
    state_doc = html.fromstring(state_str)

    print 'link labels'
    found_link = False

    possible_links = {}

    # look through all the links on the page and save the URLs that look like election results pages
    for a in state_doc.cssselect('a'):
        
        if a.text_content().lower() in ('elections', 'election results'):
            if a.attrib['href'] and a.attrib['href'] != '#':
                full_url = os.path.join(url, a.attrib['href']
                scraperwiki.sqlite.save(unique_keys=['state','label'], data={'state': state, 'possible_elections_url': full_url, 'label': a.text_content()})

            found_link = True

    if not found_link:
        scraperwiki.sqlite.save(unique_keys=['state'], data={'missing_elections_url':True, 'parent_url': url})
  
import scraperwiki
from lxml import html
import re
import os.path
import csv
import StringIO

try:
    swutils = scraperwiki.utils
except AttributeError:
    import gasp_helper
else:
    swutils.swimport("gasp_helper")

state_boards_csv = """AK,http://www.elections.alaska.gov/
AL,http://www.sos.state.al.us/elections/
AR,http://www.sosweb.state.ar.us/elections.html
AZ,http://www.azsos.gov/election/
CA,http://www.sos.ca.gov/elections/elections.htm
CO,http://www.elections.colorado.gov/
CT,http://www.ct.gov/sots/
DC,http://www.dcboee.org/
DE,http://elections.delaware.gov/
FL,http://election.dos.state.fl.us/
GA,http://sos.georgia.gov/elections/
HI,http://hawaii.gov/elections/
IA,http://www.sos.state.ia.us/elections/
ID,http://www.idahovotes.gov/
IL,http://www.elections.il.gov/
IN,http://www.indianavoters.com/
KS,http://www.kssos.org/elections/elections.html
KY,http://www.elect.ky.gov/
LA,http://www.sos.louisiana.gov/
MA,http://www.sec.state.ma.us/ele/
MD,http://www.elections.state.md.us/
ME,http://www.state.me.us/sos/cec/elec/
MI,http://www.michigan.gov/sos/0g1607,7-127-1633---,00.html
MN,http://www.sos.state.mn.us/home/index.asp?page=134
MO,http://www.sos.mo.gov/elections/
MS,http://www.sos.state.ms.us/elections/elections.asp
MT,http://www.montanavotes.net/
NC,http://www.sboe.state.nc.us/
NE,http://www.sos.ne.gov/elec/
NJ,http://www.njelections.org/
NM,http://www.sos.state.nm.us/sos-elections.html
NV,http://sos.state.nv.us/elections/
NY,http://www.elections.state.ny.us/
OH,http://www.sos.state.oh.us/SOS/elections.aspx
OK,http://www.ok.gov/~elections/
OR,http://www.sos.state.or.us/elections/voterresources.html
PA,http://www.votespa.com/
RI,http://www.elections.state.ri.us/
SC,http://www.scvotes.org/
SD,http://www.sdsos.gov/
TN,http://www.tn.gov/sos/election/
TX,http://www.sos.state.tx.us/elections/
UT,http://elections.utah.gov/
VA,http://www.sbe.virginia.gov/
VT,http://vermont-elections.org/
WA,http://www.secstate.wa.gov/elections/
WI,http://elections.state.wi.us/
WV,http://www.wvsos.com/elections/
ND,http://www.nd.gov/sos/electvote/
NH,http://www.sos.nh.gov/electionsnew.html
WY,http://soswy.state.wy.us/Elections/Elections.aspx
"""


state_boards = csv.reader(StringIO.StringIO(state_boards_csv))

for (state, url) in state_boards:
    state_str = scraperwiki.scrape(url)
    state_doc = html.fromstring(state_str)

    print 'link labels'
    found_link = False

    possible_links = {}

    # look through all the links on the page and save the URLs that look like election results pages
    for a in state_doc.cssselect('a'):
        
        if a.text_content().lower() in ('elections', 'election results'):
            if a.attrib['href'] and a.attrib['href'] != '#':
                full_url = os.path.join(url, a.attrib['href']
                scraperwiki.sqlite.save(unique_keys=['state','label'], data={'state': state, 'possible_elections_url': full_url, 'label': a.text_content()})

            found_link = True

    if not found_link:
        scraperwiki.sqlite.save(unique_keys=['state'], data={'missing_elections_url':True, 'parent_url': url})
  
