""""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore


# get the index of all from 2010
urlindex = "http://www.oireachtas.ie/members-hist/default.asp?housetype=0"
htmlindex = scraperwiki.scrape(urlindex)
print htmlindex
#http://www.oireachtas.ie/members-hist/default.asp?housetype=0&HouseNum=28&disp=mem
#<tr>
#<td><strong>10th  </strong></td>
#<td>30/06/1938 &ndash; 31/05/1943&nbsp;</td>
#<td align="center"><a href="default.asp?housetype=0&amp;HouseNum=10&amp;disp=mem"><img src="/images/members.gif" width="16" height="16" alt="Display by Members" /></a></td>
#<td align="center"><a href="default.asp?housetype=0&amp;HouseNum=10&amp;disp=const"><img src="/images/members-details.gif" width="16" height="16" alt="Display by Constituencies" /></a></td>
#</tr>
#<br>
#<img src="/images/member-party.gif" width="12" height="12" border="0" alt="" /> <strong>Party:</strong> Fianna Fáil <em>(<a #href="http://www.fiannafail.ie/" target="party">Website</a> / <a href="default.asp?housetype=0&amp;HouseNum=30&amp;PartyId=41" class="Memberlink" #title="List by party">Fianna Fáil members of the 30th  Dáil</a>)</em></li><li><img src="/images/member.gif" width="12" height="12" alt="" border="0" /> <a #href="default.asp?housetype=0&amp;HouseNum=30&amp;MemberID=6&amp;ConstID=139"><b>Mr. Dermot Ahern</b></a></br>
#sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)

dails = re.findall('<a href="(&HouseNum=\d+&disp=mem)">', htmlindex) #

for lk in dails: # no, title
    url = "http://www.oireachtas.ie/members-hist/default.asp?housetype=0"+lk
    page = scraperwiki.scrape(url)
    #print page 
    
    # http://www.irishstatutebook.ie/2010/en/si/0121.html
    #need to find act,ministry,minister|seal of courts etc
    #name = re.search('(?si)<b>(?:Mrs.|Mr.|Dr.) (.*?)</b>', page) # 
    #act powers conferred on me by
    #act = re.findall('(?si)powers conferred on (?:me by|them by) (.*?)\(No.', page) # working but with urls
    #def gettext(act):
    #  """Return the text within html, removing any HTML tags it contained."""
    #    cleaned = re.sub('<.*?>', '', act)  # remove tags
    #    cleaned = ' '.join(cleaned.split())  # collapse whitespace
    #    return cleaned
    
    #def dealWithLinks(actlinks):
    #    for link in act:
    #        href = link.get('href')
    #        name = link.text.replace("&nbsp;", "")
    
#def dealWithStructureLinks(structureLinks):
    #if href is not None:
    #        key = href.replace("/structures/data/index.cfm?id=", "")
    #        record = { "key" : key, "name" : name, "link" : base_url + href }
                                 
    #sealbody dept = re.search('(?si)<p style="display:block;">Minister (?:for|of )(.*?)</p>|<p style="display:block;">GIVEN under the seal of the (*.?),</p>', page)
    #dept = re.search('(?si)<p style="display:block;">Minister (?:for|of )(.*?)</p>|<p style="display:block;">GIVEN under the seal of the (*.?),</p>', page)
    #if dept != []: #notnone
    #    return []
    #else:
    #    print "Not a Dept", url
    #    dept = "courts or other"
       
    # if european directive 
    
    #mdate = re.search(' of</i> (\d+)<i>.. (\w+)</i>, (2010).</p>', page)
    #if mdate:
    #    date = mdate.group(1)+" "+mdate.group(2)+" 2010"
    #else:
    #    print "No date on", url
    #    date = None
    ##msdate = re.search('(?si)<p style="display:block;">Given under (?:my Official Seal|my Hand|the Official Seal of the Government|the Official Seal of,? the Minister for Finance|the Seal of the Courts Service),</p>.*?<p style="display:block;">(\d+) (\w+) (2010)\.?</p>', page) 
    #if msdate:
    #    sealdata = "%s %s %s" % msdate.groups()
    #else:
    #    print "No seal date found", url, page
    #    sealdata = None  
    #mnstr = re.findall('<p style="display:block;">WHEREAS I,|I, (.*?), Minister', page)

    data = {'url': url, 'name' :name }# 
       # data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata, 'mnstr':mnstr, 'dept':dept }#   'act':cleaned} # , 'sealbody':sealbody} # deptdata } 
    scraperwiki.datastore.save(['url'], data)   
