import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore


# get the index of all from 2010
urlindex = "http://www.oireachtas.ie/viewdoc.asp?DocID=-1&CatID=59&StartDate=1/01/2010"
htmlindex = scraperwiki.scrape(urlindex)
print htmlindex
#sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)

#02 July 2010<br /><a href="viewdoc.asp?DocID=15565&amp;&amp;CatID=59&amp;StartDate=01 January 2010&amp;OrderAscending=0" >Immigration, Residence and Protection Bill 2010 (Number 38 of 2010)</a><br>Bill entitled an Act to restate and modify certain aspects of the law relating to the entry into, presence in and removal from the State of certain foreign nationals and others, including foreign nationals in need of protection from the risk of serious harm or persecution elsewhere, while having regard also to the power of the Executive in relation to the above matters, to give effect to Council Directive 2001/40/EC of 28 May 2001 on the mutual recognition of decisions on the expulsion of third country nationals, to give effect to Council Directive 2001/55/EC of 20 July 2001 on minimum standards for giving temporary protection in the event of a mass influx of displaced persons and on measures promoting a balance of efforts between Member States in receiving such persons and bearing the consequences therof, to give effect to...<br/><a href="viewdoc.asp?DocID=15565&amp;&amp;CatID=59&amp;StartDate=01 January 2010&amp;OrderAscending=0" > [view more]</a><br />
#<hr>

#http://www.oireachtas.ie/viewdoc.asp?DocID=17196&&CatID=59&StartDate=01%20January%202010&OrderAscending=0
#sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)
sinos = re.findall('<a href="viewdoc.asp\?DocID\=(.*?)">', htmlindex)
for lk in sinos: #, no, title
    url = "http://www.oireachtas.ie/"+lk
    page = scraperwiki.scrape(url)
    print page 


    
    # http://www.irishstatutebook.ie/2010/en/si/0121.html
    #need to find act,ministry,minister|seal of courts etc
# title = re.findall('(?si)<p style="display:block;">Minister (?:for|of )(.*?)</p>', page) # working cept courts#
    title = re.findall('(?si)<SPAN class=bodytext>(?:<STRONG>|<strong>)(.*?)(?:</STRONG>|</strong>)', page) # working cept courts
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
                                 
    #sealbody  dept = re.search('(?si)<p style="display:block;">Minister  (?:for|of )(.*?)</p>|<p style="display:block;">GIVEN under  the seal of the (*.?),</p>', page)
    #dept  = re.search('(?si)<p style="display:block;">Minister (?:for|of  )(.*?)</p>|<p style="display:block;">GIVEN under the seal of  the (*.?),</p>', page)
    #if dept != []: #notnone
    #    return []
    #else:
    #    print "Not a Dept", url
    #    dept = "courts or other"
       
    # if european directive 
    
 #   mdate = re.search(' of</i> (\d+)<i>.. (\w+)</i>, (2010).</p>', page)
#    if mdate:
#        date = mdate.group(1)+" "+mdate.group(2)+" 2010"
#    else:
#        print "No date on", url
#        date = None
#    msdate = re.search('(?si)<p  style="display:block;">Given under (?:my Official Seal|my Hand|the  Official Seal of the Government|the Official Seal of,? the Minister for  Finance|the #Seal of the Courts Service),</p>.*?<p  style="display:block;">(\d+) (\w+) (2010)\.?</p>', page) 
#    if msdate:
#        sealdata = "%s %s %s" % msdate.groups()
 #   else:
  #      print "No seal date found", url, page
 #       sealdata = None  
    #mnstr = re.findall('<p style="display:block;">WHEREAS I,|I, (.*?), Minister', page)

    data = {'url': url, 'title': title }
 #   data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata, 'mnstr':mnstr, 'dept':dept }#   'act':cleaned} # , 'sealbody':sealbody} # deptdata } 
    scraperwiki.datastore.save(['url'], data)   
import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore


# get the index of all from 2010
urlindex = "http://www.oireachtas.ie/viewdoc.asp?DocID=-1&CatID=59&StartDate=1/01/2010"
htmlindex = scraperwiki.scrape(urlindex)
print htmlindex
#sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)

#02 July 2010<br /><a href="viewdoc.asp?DocID=15565&amp;&amp;CatID=59&amp;StartDate=01 January 2010&amp;OrderAscending=0" >Immigration, Residence and Protection Bill 2010 (Number 38 of 2010)</a><br>Bill entitled an Act to restate and modify certain aspects of the law relating to the entry into, presence in and removal from the State of certain foreign nationals and others, including foreign nationals in need of protection from the risk of serious harm or persecution elsewhere, while having regard also to the power of the Executive in relation to the above matters, to give effect to Council Directive 2001/40/EC of 28 May 2001 on the mutual recognition of decisions on the expulsion of third country nationals, to give effect to Council Directive 2001/55/EC of 20 July 2001 on minimum standards for giving temporary protection in the event of a mass influx of displaced persons and on measures promoting a balance of efforts between Member States in receiving such persons and bearing the consequences therof, to give effect to...<br/><a href="viewdoc.asp?DocID=15565&amp;&amp;CatID=59&amp;StartDate=01 January 2010&amp;OrderAscending=0" > [view more]</a><br />
#<hr>

#http://www.oireachtas.ie/viewdoc.asp?DocID=17196&&CatID=59&StartDate=01%20January%202010&OrderAscending=0
#sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)
sinos = re.findall('<a href="viewdoc.asp\?DocID\=(.*?)">', htmlindex)
for lk in sinos: #, no, title
    url = "http://www.oireachtas.ie/"+lk
    page = scraperwiki.scrape(url)
    print page 


    
    # http://www.irishstatutebook.ie/2010/en/si/0121.html
    #need to find act,ministry,minister|seal of courts etc
# title = re.findall('(?si)<p style="display:block;">Minister (?:for|of )(.*?)</p>', page) # working cept courts#
    title = re.findall('(?si)<SPAN class=bodytext>(?:<STRONG>|<strong>)(.*?)(?:</STRONG>|</strong>)', page) # working cept courts
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
                                 
    #sealbody  dept = re.search('(?si)<p style="display:block;">Minister  (?:for|of )(.*?)</p>|<p style="display:block;">GIVEN under  the seal of the (*.?),</p>', page)
    #dept  = re.search('(?si)<p style="display:block;">Minister (?:for|of  )(.*?)</p>|<p style="display:block;">GIVEN under the seal of  the (*.?),</p>', page)
    #if dept != []: #notnone
    #    return []
    #else:
    #    print "Not a Dept", url
    #    dept = "courts or other"
       
    # if european directive 
    
 #   mdate = re.search(' of</i> (\d+)<i>.. (\w+)</i>, (2010).</p>', page)
#    if mdate:
#        date = mdate.group(1)+" "+mdate.group(2)+" 2010"
#    else:
#        print "No date on", url
#        date = None
#    msdate = re.search('(?si)<p  style="display:block;">Given under (?:my Official Seal|my Hand|the  Official Seal of the Government|the Official Seal of,? the Minister for  Finance|the #Seal of the Courts Service),</p>.*?<p  style="display:block;">(\d+) (\w+) (2010)\.?</p>', page) 
#    if msdate:
#        sealdata = "%s %s %s" % msdate.groups()
 #   else:
  #      print "No seal date found", url, page
 #       sealdata = None  
    #mnstr = re.findall('<p style="display:block;">WHEREAS I,|I, (.*?), Minister', page)

    data = {'url': url, 'title': title }
 #   data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata, 'mnstr':mnstr, 'dept':dept }#   'act':cleaned} # , 'sealbody':sealbody} # deptdata } 
    scraperwiki.datastore.save(['url'], data)   
import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore


# get the index of all from 2010
urlindex = "http://www.oireachtas.ie/viewdoc.asp?DocID=-1&CatID=59&StartDate=1/01/2010"
htmlindex = scraperwiki.scrape(urlindex)
print htmlindex
#sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)

#02 July 2010<br /><a href="viewdoc.asp?DocID=15565&amp;&amp;CatID=59&amp;StartDate=01 January 2010&amp;OrderAscending=0" >Immigration, Residence and Protection Bill 2010 (Number 38 of 2010)</a><br>Bill entitled an Act to restate and modify certain aspects of the law relating to the entry into, presence in and removal from the State of certain foreign nationals and others, including foreign nationals in need of protection from the risk of serious harm or persecution elsewhere, while having regard also to the power of the Executive in relation to the above matters, to give effect to Council Directive 2001/40/EC of 28 May 2001 on the mutual recognition of decisions on the expulsion of third country nationals, to give effect to Council Directive 2001/55/EC of 20 July 2001 on minimum standards for giving temporary protection in the event of a mass influx of displaced persons and on measures promoting a balance of efforts between Member States in receiving such persons and bearing the consequences therof, to give effect to...<br/><a href="viewdoc.asp?DocID=15565&amp;&amp;CatID=59&amp;StartDate=01 January 2010&amp;OrderAscending=0" > [view more]</a><br />
#<hr>

#http://www.oireachtas.ie/viewdoc.asp?DocID=17196&&CatID=59&StartDate=01%20January%202010&OrderAscending=0
#sinos = re.findall('<a href="(/2010/en/si/\d+.html)">S.I. No. (\d+)/2010 — (.*?).</a>', htmlindex)
sinos = re.findall('<a href="viewdoc.asp\?DocID\=(.*?)">', htmlindex)
for lk in sinos: #, no, title
    url = "http://www.oireachtas.ie/"+lk
    page = scraperwiki.scrape(url)
    print page 


    
    # http://www.irishstatutebook.ie/2010/en/si/0121.html
    #need to find act,ministry,minister|seal of courts etc
# title = re.findall('(?si)<p style="display:block;">Minister (?:for|of )(.*?)</p>', page) # working cept courts#
    title = re.findall('(?si)<SPAN class=bodytext>(?:<STRONG>|<strong>)(.*?)(?:</STRONG>|</strong>)', page) # working cept courts
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
                                 
    #sealbody  dept = re.search('(?si)<p style="display:block;">Minister  (?:for|of )(.*?)</p>|<p style="display:block;">GIVEN under  the seal of the (*.?),</p>', page)
    #dept  = re.search('(?si)<p style="display:block;">Minister (?:for|of  )(.*?)</p>|<p style="display:block;">GIVEN under the seal of  the (*.?),</p>', page)
    #if dept != []: #notnone
    #    return []
    #else:
    #    print "Not a Dept", url
    #    dept = "courts or other"
       
    # if european directive 
    
 #   mdate = re.search(' of</i> (\d+)<i>.. (\w+)</i>, (2010).</p>', page)
#    if mdate:
#        date = mdate.group(1)+" "+mdate.group(2)+" 2010"
#    else:
#        print "No date on", url
#        date = None
#    msdate = re.search('(?si)<p  style="display:block;">Given under (?:my Official Seal|my Hand|the  Official Seal of the Government|the Official Seal of,? the Minister for  Finance|the #Seal of the Courts Service),</p>.*?<p  style="display:block;">(\d+) (\w+) (2010)\.?</p>', page) 
#    if msdate:
#        sealdata = "%s %s %s" % msdate.groups()
 #   else:
  #      print "No seal date found", url, page
 #       sealdata = None  
    #mnstr = re.findall('<p style="display:block;">WHEREAS I,|I, (.*?), Minister', page)

    data = {'url': url, 'title': title }
 #   data = {'url': url, 'title': title, 'number':no, 'date':date, 'sealdate':sealdata, 'mnstr':mnstr, 'dept':dept }#   'act':cleaned} # , 'sealbody':sealbody} # deptdata } 
    scraperwiki.datastore.save(['url'], data)   
