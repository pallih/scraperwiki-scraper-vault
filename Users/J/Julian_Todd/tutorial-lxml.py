## lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The parsed objects are slightly different between the two.  
# This tutorial walks through the xml features

import lxml.etree

# create an example case
samplexml = """<HTML><HEAD><meta http-equiv="Content-Language" content="en-us"><meta http-equiv="Content-Type" content="text/html; charset=windows-1252"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="Mon, 01 Jan 1990 12:00:00 GMT"><title>SHOUTcast Administrator</title><style type="text/css"><!--a:link {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:visited {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:hover {color: red; font-family:Arial, Helvetica; font-size:9pt; }.default {color: White; font-family:Arial, Helvetica; font-size:9pt; font-weight: normal}.ST {color: White; font-family:Arial, Helvetica; font-size:8pt; font-weight: normal}.logoText {color: red; font-family: Arial Black, Helvetica, sans-serif; font-size: 25pt; font-weight: normal; letter-spacing : -2.5px;}.flagText {color: blue; font-family: webdings; font-size: 36pt; font-weight: normal; }.ltv {color: blue; font-family: Arial, Helvetica, sans-serif; font-size: 9pt; font-weight: normal;}.tnl {color: black; font-family: Arial, Helvetica, sans-serif; font-size: 10pt; font-weight: bold; text-decoration: none;}--></style></HEAD><BODY topmargin=0 leftmargin=0 marginheight=0 marginwidth=0 bgcolor=#000000 text=#EEEEEE link=#001155 vlink=#001155 alink=#FF0000><font class=default><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td height=50><font class=flagText>U</font><font class=logoText>&nbsp;SHOUTcast D.N.A.S. Status</font></td></tr><tr><td height=14 align=right><font class=ltv><a id=ltv href="http://www.shoutcast.com/">SHOUTcast Server Version 1.9.8/Linux</a></font></td></tr><tr><td bgcolor=#DDDDDD height=20 align=center><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td align=center><font class=tnl><a id=tnl href="index.html">Status</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="played.html">Song History</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="listen.pls">Listen</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="home.html">Stream URL</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="admin.cgi">Admin Login</a></font></td></tr></table></td></tr></table><br><table cellpadding=5 cellspacing=0 border=0 width=100%><tr><td bgcolor=#000025 colspan=2 align=center><font class=ST>Current Stream Information</font></td></tr></table><table cellpadding=2 cellspacing=0 border=0 align=center><tr><td width=100 nowrap><font class=default>Server Status: </font></td><td><font class=default><b>Server is currently up and private.</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Status: </font></td><td><font class=default><b>Stream is up at 128 kbps with <B>0 of 50 listeners (0 unique)</b></b></td></tr><tr><td width=100 nowrap><font class=default>Listener Peak: </font></td><td><font class=default><b>0</b></td></tr><tr><td width=100 nowrap><font class=default>Average Listen Time: </font></td><td><font class=default><b>0m&nbsp;01s</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Title: </font></td><td><font class=default><b>TI-Radio AutoDj</b></td></tr><tr><td width=100 nowrap><font class=default>Content Type: </font></td><td><font class=default><b>audio/mpeg</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Genre: </font></td><td><font class=default><b>Various</b></td></tr><tr><td width=100 nowrap><font class=default>Stream URL: </font></td><td><font class=default><b><a href="http://www.torrent-invites.com/">http://www.torrent-invites.com/</a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream ICQ: </font></td><td><font class=default><b><a href="http://wwp.icq.com/scripts/contact.dll?msgto="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream AIM: </font></td><td><font class=default><b><a href="aim:goim?screenname="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream IRC: </font></td><td><font class=default><b><a href="http://www.shoutcast.com/chat.phtml?dc="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Current Song: </font></td><td><font class=default><b>K-Ci and Jo Jo - Crazy</b></td></tr></table><br><table cellpadding=0 cellspacing=0 border=0 width=100%>    <tr><td bgcolor=#DDDDDD  nowrap colspan=5 align=center><table cellspacing=0 cellpadding=0 border=0><tr><td><font class=ltv>Written by Stephen 'Tag Loomis, Tom Pepper and Justin Frankel</font></td></tr></table></td></tr><tr><td nowrap colspan=5 align=center><font class=ST><b><a href="http://www.shoutcast.com/disclaimer.phtml">Copyright Nullsoft Inc</a><a href="/llamacookie">.</a> 1998-2004</b></font></td></tr></table></font></body></html>"""

root = lxml.etree.fromstring(samplexml)  # an lxml.etree.Element object


# to load directly from a file, do
tree = lxml.etree.parse("http://ukparse.kforge.net/parldata/scrapedxml/debates/debates2010-03-29a.xml")
root = tree.getroot()  # tree is an ElementTree object.  findall works for the whole document

print root
print lxml.etree.tostring(root)

# uncomment each line to test it
print root.tag, len(root), list(root), root[0]  # the Element object can like a list

# element objects carry a dict for the attributes
# print root.get("v")   # returns qqqq
#print root.get("vvv") # returns None (doesn't exist)
#print root.keys()     # list of keys available

print root.findall("b")[0].text
#print root.findall("hh2")   # nothing
#print root.findall(".//hh2")   # anywhere in the list

# just the text within an element



## lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The parsed objects are slightly different between the two.  
# This tutorial walks through the xml features

import lxml.etree

# create an example case
samplexml = """<HTML><HEAD><meta http-equiv="Content-Language" content="en-us"><meta http-equiv="Content-Type" content="text/html; charset=windows-1252"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="Mon, 01 Jan 1990 12:00:00 GMT"><title>SHOUTcast Administrator</title><style type="text/css"><!--a:link {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:visited {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:hover {color: red; font-family:Arial, Helvetica; font-size:9pt; }.default {color: White; font-family:Arial, Helvetica; font-size:9pt; font-weight: normal}.ST {color: White; font-family:Arial, Helvetica; font-size:8pt; font-weight: normal}.logoText {color: red; font-family: Arial Black, Helvetica, sans-serif; font-size: 25pt; font-weight: normal; letter-spacing : -2.5px;}.flagText {color: blue; font-family: webdings; font-size: 36pt; font-weight: normal; }.ltv {color: blue; font-family: Arial, Helvetica, sans-serif; font-size: 9pt; font-weight: normal;}.tnl {color: black; font-family: Arial, Helvetica, sans-serif; font-size: 10pt; font-weight: bold; text-decoration: none;}--></style></HEAD><BODY topmargin=0 leftmargin=0 marginheight=0 marginwidth=0 bgcolor=#000000 text=#EEEEEE link=#001155 vlink=#001155 alink=#FF0000><font class=default><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td height=50><font class=flagText>U</font><font class=logoText>&nbsp;SHOUTcast D.N.A.S. Status</font></td></tr><tr><td height=14 align=right><font class=ltv><a id=ltv href="http://www.shoutcast.com/">SHOUTcast Server Version 1.9.8/Linux</a></font></td></tr><tr><td bgcolor=#DDDDDD height=20 align=center><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td align=center><font class=tnl><a id=tnl href="index.html">Status</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="played.html">Song History</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="listen.pls">Listen</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="home.html">Stream URL</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="admin.cgi">Admin Login</a></font></td></tr></table></td></tr></table><br><table cellpadding=5 cellspacing=0 border=0 width=100%><tr><td bgcolor=#000025 colspan=2 align=center><font class=ST>Current Stream Information</font></td></tr></table><table cellpadding=2 cellspacing=0 border=0 align=center><tr><td width=100 nowrap><font class=default>Server Status: </font></td><td><font class=default><b>Server is currently up and private.</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Status: </font></td><td><font class=default><b>Stream is up at 128 kbps with <B>0 of 50 listeners (0 unique)</b></b></td></tr><tr><td width=100 nowrap><font class=default>Listener Peak: </font></td><td><font class=default><b>0</b></td></tr><tr><td width=100 nowrap><font class=default>Average Listen Time: </font></td><td><font class=default><b>0m&nbsp;01s</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Title: </font></td><td><font class=default><b>TI-Radio AutoDj</b></td></tr><tr><td width=100 nowrap><font class=default>Content Type: </font></td><td><font class=default><b>audio/mpeg</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Genre: </font></td><td><font class=default><b>Various</b></td></tr><tr><td width=100 nowrap><font class=default>Stream URL: </font></td><td><font class=default><b><a href="http://www.torrent-invites.com/">http://www.torrent-invites.com/</a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream ICQ: </font></td><td><font class=default><b><a href="http://wwp.icq.com/scripts/contact.dll?msgto="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream AIM: </font></td><td><font class=default><b><a href="aim:goim?screenname="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream IRC: </font></td><td><font class=default><b><a href="http://www.shoutcast.com/chat.phtml?dc="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Current Song: </font></td><td><font class=default><b>K-Ci and Jo Jo - Crazy</b></td></tr></table><br><table cellpadding=0 cellspacing=0 border=0 width=100%>    <tr><td bgcolor=#DDDDDD  nowrap colspan=5 align=center><table cellspacing=0 cellpadding=0 border=0><tr><td><font class=ltv>Written by Stephen 'Tag Loomis, Tom Pepper and Justin Frankel</font></td></tr></table></td></tr><tr><td nowrap colspan=5 align=center><font class=ST><b><a href="http://www.shoutcast.com/disclaimer.phtml">Copyright Nullsoft Inc</a><a href="/llamacookie">.</a> 1998-2004</b></font></td></tr></table></font></body></html>"""

root = lxml.etree.fromstring(samplexml)  # an lxml.etree.Element object


# to load directly from a file, do
tree = lxml.etree.parse("http://ukparse.kforge.net/parldata/scrapedxml/debates/debates2010-03-29a.xml")
root = tree.getroot()  # tree is an ElementTree object.  findall works for the whole document

print root
print lxml.etree.tostring(root)

# uncomment each line to test it
print root.tag, len(root), list(root), root[0]  # the Element object can like a list

# element objects carry a dict for the attributes
# print root.get("v")   # returns qqqq
#print root.get("vvv") # returns None (doesn't exist)
#print root.keys()     # list of keys available

print root.findall("b")[0].text
#print root.findall("hh2")   # nothing
#print root.findall(".//hh2")   # anywhere in the list

# just the text within an element



## lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The parsed objects are slightly different between the two.  
# This tutorial walks through the xml features

import lxml.etree

# create an example case
samplexml = """<HTML><HEAD><meta http-equiv="Content-Language" content="en-us"><meta http-equiv="Content-Type" content="text/html; charset=windows-1252"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="Mon, 01 Jan 1990 12:00:00 GMT"><title>SHOUTcast Administrator</title><style type="text/css"><!--a:link {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:visited {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:hover {color: red; font-family:Arial, Helvetica; font-size:9pt; }.default {color: White; font-family:Arial, Helvetica; font-size:9pt; font-weight: normal}.ST {color: White; font-family:Arial, Helvetica; font-size:8pt; font-weight: normal}.logoText {color: red; font-family: Arial Black, Helvetica, sans-serif; font-size: 25pt; font-weight: normal; letter-spacing : -2.5px;}.flagText {color: blue; font-family: webdings; font-size: 36pt; font-weight: normal; }.ltv {color: blue; font-family: Arial, Helvetica, sans-serif; font-size: 9pt; font-weight: normal;}.tnl {color: black; font-family: Arial, Helvetica, sans-serif; font-size: 10pt; font-weight: bold; text-decoration: none;}--></style></HEAD><BODY topmargin=0 leftmargin=0 marginheight=0 marginwidth=0 bgcolor=#000000 text=#EEEEEE link=#001155 vlink=#001155 alink=#FF0000><font class=default><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td height=50><font class=flagText>U</font><font class=logoText>&nbsp;SHOUTcast D.N.A.S. Status</font></td></tr><tr><td height=14 align=right><font class=ltv><a id=ltv href="http://www.shoutcast.com/">SHOUTcast Server Version 1.9.8/Linux</a></font></td></tr><tr><td bgcolor=#DDDDDD height=20 align=center><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td align=center><font class=tnl><a id=tnl href="index.html">Status</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="played.html">Song History</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="listen.pls">Listen</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="home.html">Stream URL</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="admin.cgi">Admin Login</a></font></td></tr></table></td></tr></table><br><table cellpadding=5 cellspacing=0 border=0 width=100%><tr><td bgcolor=#000025 colspan=2 align=center><font class=ST>Current Stream Information</font></td></tr></table><table cellpadding=2 cellspacing=0 border=0 align=center><tr><td width=100 nowrap><font class=default>Server Status: </font></td><td><font class=default><b>Server is currently up and private.</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Status: </font></td><td><font class=default><b>Stream is up at 128 kbps with <B>0 of 50 listeners (0 unique)</b></b></td></tr><tr><td width=100 nowrap><font class=default>Listener Peak: </font></td><td><font class=default><b>0</b></td></tr><tr><td width=100 nowrap><font class=default>Average Listen Time: </font></td><td><font class=default><b>0m&nbsp;01s</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Title: </font></td><td><font class=default><b>TI-Radio AutoDj</b></td></tr><tr><td width=100 nowrap><font class=default>Content Type: </font></td><td><font class=default><b>audio/mpeg</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Genre: </font></td><td><font class=default><b>Various</b></td></tr><tr><td width=100 nowrap><font class=default>Stream URL: </font></td><td><font class=default><b><a href="http://www.torrent-invites.com/">http://www.torrent-invites.com/</a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream ICQ: </font></td><td><font class=default><b><a href="http://wwp.icq.com/scripts/contact.dll?msgto="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream AIM: </font></td><td><font class=default><b><a href="aim:goim?screenname="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream IRC: </font></td><td><font class=default><b><a href="http://www.shoutcast.com/chat.phtml?dc="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Current Song: </font></td><td><font class=default><b>K-Ci and Jo Jo - Crazy</b></td></tr></table><br><table cellpadding=0 cellspacing=0 border=0 width=100%>    <tr><td bgcolor=#DDDDDD  nowrap colspan=5 align=center><table cellspacing=0 cellpadding=0 border=0><tr><td><font class=ltv>Written by Stephen 'Tag Loomis, Tom Pepper and Justin Frankel</font></td></tr></table></td></tr><tr><td nowrap colspan=5 align=center><font class=ST><b><a href="http://www.shoutcast.com/disclaimer.phtml">Copyright Nullsoft Inc</a><a href="/llamacookie">.</a> 1998-2004</b></font></td></tr></table></font></body></html>"""

root = lxml.etree.fromstring(samplexml)  # an lxml.etree.Element object


# to load directly from a file, do
tree = lxml.etree.parse("http://ukparse.kforge.net/parldata/scrapedxml/debates/debates2010-03-29a.xml")
root = tree.getroot()  # tree is an ElementTree object.  findall works for the whole document

print root
print lxml.etree.tostring(root)

# uncomment each line to test it
print root.tag, len(root), list(root), root[0]  # the Element object can like a list

# element objects carry a dict for the attributes
# print root.get("v")   # returns qqqq
#print root.get("vvv") # returns None (doesn't exist)
#print root.keys()     # list of keys available

print root.findall("b")[0].text
#print root.findall("hh2")   # nothing
#print root.findall(".//hh2")   # anywhere in the list

# just the text within an element



## lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The parsed objects are slightly different between the two.  
# This tutorial walks through the xml features

import lxml.etree

# create an example case
samplexml = """<HTML><HEAD><meta http-equiv="Content-Language" content="en-us"><meta http-equiv="Content-Type" content="text/html; charset=windows-1252"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="Mon, 01 Jan 1990 12:00:00 GMT"><title>SHOUTcast Administrator</title><style type="text/css"><!--a:link {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:visited {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:hover {color: red; font-family:Arial, Helvetica; font-size:9pt; }.default {color: White; font-family:Arial, Helvetica; font-size:9pt; font-weight: normal}.ST {color: White; font-family:Arial, Helvetica; font-size:8pt; font-weight: normal}.logoText {color: red; font-family: Arial Black, Helvetica, sans-serif; font-size: 25pt; font-weight: normal; letter-spacing : -2.5px;}.flagText {color: blue; font-family: webdings; font-size: 36pt; font-weight: normal; }.ltv {color: blue; font-family: Arial, Helvetica, sans-serif; font-size: 9pt; font-weight: normal;}.tnl {color: black; font-family: Arial, Helvetica, sans-serif; font-size: 10pt; font-weight: bold; text-decoration: none;}--></style></HEAD><BODY topmargin=0 leftmargin=0 marginheight=0 marginwidth=0 bgcolor=#000000 text=#EEEEEE link=#001155 vlink=#001155 alink=#FF0000><font class=default><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td height=50><font class=flagText>U</font><font class=logoText>&nbsp;SHOUTcast D.N.A.S. Status</font></td></tr><tr><td height=14 align=right><font class=ltv><a id=ltv href="http://www.shoutcast.com/">SHOUTcast Server Version 1.9.8/Linux</a></font></td></tr><tr><td bgcolor=#DDDDDD height=20 align=center><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td align=center><font class=tnl><a id=tnl href="index.html">Status</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="played.html">Song History</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="listen.pls">Listen</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="home.html">Stream URL</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="admin.cgi">Admin Login</a></font></td></tr></table></td></tr></table><br><table cellpadding=5 cellspacing=0 border=0 width=100%><tr><td bgcolor=#000025 colspan=2 align=center><font class=ST>Current Stream Information</font></td></tr></table><table cellpadding=2 cellspacing=0 border=0 align=center><tr><td width=100 nowrap><font class=default>Server Status: </font></td><td><font class=default><b>Server is currently up and private.</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Status: </font></td><td><font class=default><b>Stream is up at 128 kbps with <B>0 of 50 listeners (0 unique)</b></b></td></tr><tr><td width=100 nowrap><font class=default>Listener Peak: </font></td><td><font class=default><b>0</b></td></tr><tr><td width=100 nowrap><font class=default>Average Listen Time: </font></td><td><font class=default><b>0m&nbsp;01s</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Title: </font></td><td><font class=default><b>TI-Radio AutoDj</b></td></tr><tr><td width=100 nowrap><font class=default>Content Type: </font></td><td><font class=default><b>audio/mpeg</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Genre: </font></td><td><font class=default><b>Various</b></td></tr><tr><td width=100 nowrap><font class=default>Stream URL: </font></td><td><font class=default><b><a href="http://www.torrent-invites.com/">http://www.torrent-invites.com/</a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream ICQ: </font></td><td><font class=default><b><a href="http://wwp.icq.com/scripts/contact.dll?msgto="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream AIM: </font></td><td><font class=default><b><a href="aim:goim?screenname="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream IRC: </font></td><td><font class=default><b><a href="http://www.shoutcast.com/chat.phtml?dc="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Current Song: </font></td><td><font class=default><b>K-Ci and Jo Jo - Crazy</b></td></tr></table><br><table cellpadding=0 cellspacing=0 border=0 width=100%>    <tr><td bgcolor=#DDDDDD  nowrap colspan=5 align=center><table cellspacing=0 cellpadding=0 border=0><tr><td><font class=ltv>Written by Stephen 'Tag Loomis, Tom Pepper and Justin Frankel</font></td></tr></table></td></tr><tr><td nowrap colspan=5 align=center><font class=ST><b><a href="http://www.shoutcast.com/disclaimer.phtml">Copyright Nullsoft Inc</a><a href="/llamacookie">.</a> 1998-2004</b></font></td></tr></table></font></body></html>"""

root = lxml.etree.fromstring(samplexml)  # an lxml.etree.Element object


# to load directly from a file, do
tree = lxml.etree.parse("http://ukparse.kforge.net/parldata/scrapedxml/debates/debates2010-03-29a.xml")
root = tree.getroot()  # tree is an ElementTree object.  findall works for the whole document

print root
print lxml.etree.tostring(root)

# uncomment each line to test it
print root.tag, len(root), list(root), root[0]  # the Element object can like a list

# element objects carry a dict for the attributes
# print root.get("v")   # returns qqqq
#print root.get("vvv") # returns None (doesn't exist)
#print root.keys()     # list of keys available

print root.findall("b")[0].text
#print root.findall("hh2")   # nothing
#print root.findall(".//hh2")   # anywhere in the list

# just the text within an element



## lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The parsed objects are slightly different between the two.  
# This tutorial walks through the xml features

import lxml.etree

# create an example case
samplexml = """<HTML><HEAD><meta http-equiv="Content-Language" content="en-us"><meta http-equiv="Content-Type" content="text/html; charset=windows-1252"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="Mon, 01 Jan 1990 12:00:00 GMT"><title>SHOUTcast Administrator</title><style type="text/css"><!--a:link {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:visited {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:hover {color: red; font-family:Arial, Helvetica; font-size:9pt; }.default {color: White; font-family:Arial, Helvetica; font-size:9pt; font-weight: normal}.ST {color: White; font-family:Arial, Helvetica; font-size:8pt; font-weight: normal}.logoText {color: red; font-family: Arial Black, Helvetica, sans-serif; font-size: 25pt; font-weight: normal; letter-spacing : -2.5px;}.flagText {color: blue; font-family: webdings; font-size: 36pt; font-weight: normal; }.ltv {color: blue; font-family: Arial, Helvetica, sans-serif; font-size: 9pt; font-weight: normal;}.tnl {color: black; font-family: Arial, Helvetica, sans-serif; font-size: 10pt; font-weight: bold; text-decoration: none;}--></style></HEAD><BODY topmargin=0 leftmargin=0 marginheight=0 marginwidth=0 bgcolor=#000000 text=#EEEEEE link=#001155 vlink=#001155 alink=#FF0000><font class=default><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td height=50><font class=flagText>U</font><font class=logoText>&nbsp;SHOUTcast D.N.A.S. Status</font></td></tr><tr><td height=14 align=right><font class=ltv><a id=ltv href="http://www.shoutcast.com/">SHOUTcast Server Version 1.9.8/Linux</a></font></td></tr><tr><td bgcolor=#DDDDDD height=20 align=center><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td align=center><font class=tnl><a id=tnl href="index.html">Status</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="played.html">Song History</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="listen.pls">Listen</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="home.html">Stream URL</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="admin.cgi">Admin Login</a></font></td></tr></table></td></tr></table><br><table cellpadding=5 cellspacing=0 border=0 width=100%><tr><td bgcolor=#000025 colspan=2 align=center><font class=ST>Current Stream Information</font></td></tr></table><table cellpadding=2 cellspacing=0 border=0 align=center><tr><td width=100 nowrap><font class=default>Server Status: </font></td><td><font class=default><b>Server is currently up and private.</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Status: </font></td><td><font class=default><b>Stream is up at 128 kbps with <B>0 of 50 listeners (0 unique)</b></b></td></tr><tr><td width=100 nowrap><font class=default>Listener Peak: </font></td><td><font class=default><b>0</b></td></tr><tr><td width=100 nowrap><font class=default>Average Listen Time: </font></td><td><font class=default><b>0m&nbsp;01s</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Title: </font></td><td><font class=default><b>TI-Radio AutoDj</b></td></tr><tr><td width=100 nowrap><font class=default>Content Type: </font></td><td><font class=default><b>audio/mpeg</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Genre: </font></td><td><font class=default><b>Various</b></td></tr><tr><td width=100 nowrap><font class=default>Stream URL: </font></td><td><font class=default><b><a href="http://www.torrent-invites.com/">http://www.torrent-invites.com/</a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream ICQ: </font></td><td><font class=default><b><a href="http://wwp.icq.com/scripts/contact.dll?msgto="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream AIM: </font></td><td><font class=default><b><a href="aim:goim?screenname="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream IRC: </font></td><td><font class=default><b><a href="http://www.shoutcast.com/chat.phtml?dc="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Current Song: </font></td><td><font class=default><b>K-Ci and Jo Jo - Crazy</b></td></tr></table><br><table cellpadding=0 cellspacing=0 border=0 width=100%>    <tr><td bgcolor=#DDDDDD  nowrap colspan=5 align=center><table cellspacing=0 cellpadding=0 border=0><tr><td><font class=ltv>Written by Stephen 'Tag Loomis, Tom Pepper and Justin Frankel</font></td></tr></table></td></tr><tr><td nowrap colspan=5 align=center><font class=ST><b><a href="http://www.shoutcast.com/disclaimer.phtml">Copyright Nullsoft Inc</a><a href="/llamacookie">.</a> 1998-2004</b></font></td></tr></table></font></body></html>"""

root = lxml.etree.fromstring(samplexml)  # an lxml.etree.Element object


# to load directly from a file, do
tree = lxml.etree.parse("http://ukparse.kforge.net/parldata/scrapedxml/debates/debates2010-03-29a.xml")
root = tree.getroot()  # tree is an ElementTree object.  findall works for the whole document

print root
print lxml.etree.tostring(root)

# uncomment each line to test it
print root.tag, len(root), list(root), root[0]  # the Element object can like a list

# element objects carry a dict for the attributes
# print root.get("v")   # returns qqqq
#print root.get("vvv") # returns None (doesn't exist)
#print root.keys()     # list of keys available

print root.findall("b")[0].text
#print root.findall("hh2")   # nothing
#print root.findall(".//hh2")   # anywhere in the list

# just the text within an element



## lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The parsed objects are slightly different between the two.  
# This tutorial walks through the xml features

import lxml.etree

# create an example case
samplexml = """<HTML><HEAD><meta http-equiv="Content-Language" content="en-us"><meta http-equiv="Content-Type" content="text/html; charset=windows-1252"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="Mon, 01 Jan 1990 12:00:00 GMT"><title>SHOUTcast Administrator</title><style type="text/css"><!--a:link {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:visited {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:hover {color: red; font-family:Arial, Helvetica; font-size:9pt; }.default {color: White; font-family:Arial, Helvetica; font-size:9pt; font-weight: normal}.ST {color: White; font-family:Arial, Helvetica; font-size:8pt; font-weight: normal}.logoText {color: red; font-family: Arial Black, Helvetica, sans-serif; font-size: 25pt; font-weight: normal; letter-spacing : -2.5px;}.flagText {color: blue; font-family: webdings; font-size: 36pt; font-weight: normal; }.ltv {color: blue; font-family: Arial, Helvetica, sans-serif; font-size: 9pt; font-weight: normal;}.tnl {color: black; font-family: Arial, Helvetica, sans-serif; font-size: 10pt; font-weight: bold; text-decoration: none;}--></style></HEAD><BODY topmargin=0 leftmargin=0 marginheight=0 marginwidth=0 bgcolor=#000000 text=#EEEEEE link=#001155 vlink=#001155 alink=#FF0000><font class=default><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td height=50><font class=flagText>U</font><font class=logoText>&nbsp;SHOUTcast D.N.A.S. Status</font></td></tr><tr><td height=14 align=right><font class=ltv><a id=ltv href="http://www.shoutcast.com/">SHOUTcast Server Version 1.9.8/Linux</a></font></td></tr><tr><td bgcolor=#DDDDDD height=20 align=center><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td align=center><font class=tnl><a id=tnl href="index.html">Status</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="played.html">Song History</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="listen.pls">Listen</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="home.html">Stream URL</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="admin.cgi">Admin Login</a></font></td></tr></table></td></tr></table><br><table cellpadding=5 cellspacing=0 border=0 width=100%><tr><td bgcolor=#000025 colspan=2 align=center><font class=ST>Current Stream Information</font></td></tr></table><table cellpadding=2 cellspacing=0 border=0 align=center><tr><td width=100 nowrap><font class=default>Server Status: </font></td><td><font class=default><b>Server is currently up and private.</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Status: </font></td><td><font class=default><b>Stream is up at 128 kbps with <B>0 of 50 listeners (0 unique)</b></b></td></tr><tr><td width=100 nowrap><font class=default>Listener Peak: </font></td><td><font class=default><b>0</b></td></tr><tr><td width=100 nowrap><font class=default>Average Listen Time: </font></td><td><font class=default><b>0m&nbsp;01s</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Title: </font></td><td><font class=default><b>TI-Radio AutoDj</b></td></tr><tr><td width=100 nowrap><font class=default>Content Type: </font></td><td><font class=default><b>audio/mpeg</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Genre: </font></td><td><font class=default><b>Various</b></td></tr><tr><td width=100 nowrap><font class=default>Stream URL: </font></td><td><font class=default><b><a href="http://www.torrent-invites.com/">http://www.torrent-invites.com/</a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream ICQ: </font></td><td><font class=default><b><a href="http://wwp.icq.com/scripts/contact.dll?msgto="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream AIM: </font></td><td><font class=default><b><a href="aim:goim?screenname="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream IRC: </font></td><td><font class=default><b><a href="http://www.shoutcast.com/chat.phtml?dc="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Current Song: </font></td><td><font class=default><b>K-Ci and Jo Jo - Crazy</b></td></tr></table><br><table cellpadding=0 cellspacing=0 border=0 width=100%>    <tr><td bgcolor=#DDDDDD  nowrap colspan=5 align=center><table cellspacing=0 cellpadding=0 border=0><tr><td><font class=ltv>Written by Stephen 'Tag Loomis, Tom Pepper and Justin Frankel</font></td></tr></table></td></tr><tr><td nowrap colspan=5 align=center><font class=ST><b><a href="http://www.shoutcast.com/disclaimer.phtml">Copyright Nullsoft Inc</a><a href="/llamacookie">.</a> 1998-2004</b></font></td></tr></table></font></body></html>"""

root = lxml.etree.fromstring(samplexml)  # an lxml.etree.Element object


# to load directly from a file, do
tree = lxml.etree.parse("http://ukparse.kforge.net/parldata/scrapedxml/debates/debates2010-03-29a.xml")
root = tree.getroot()  # tree is an ElementTree object.  findall works for the whole document

print root
print lxml.etree.tostring(root)

# uncomment each line to test it
print root.tag, len(root), list(root), root[0]  # the Element object can like a list

# element objects carry a dict for the attributes
# print root.get("v")   # returns qqqq
#print root.get("vvv") # returns None (doesn't exist)
#print root.keys()     # list of keys available

print root.findall("b")[0].text
#print root.findall("hh2")   # nothing
#print root.findall(".//hh2")   # anywhere in the list

# just the text within an element



## lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The parsed objects are slightly different between the two.  
# This tutorial walks through the xml features

import lxml.etree

# create an example case
samplexml = """<HTML><HEAD><meta http-equiv="Content-Language" content="en-us"><meta http-equiv="Content-Type" content="text/html; charset=windows-1252"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="Mon, 01 Jan 1990 12:00:00 GMT"><title>SHOUTcast Administrator</title><style type="text/css"><!--a:link {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:visited {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:hover {color: red; font-family:Arial, Helvetica; font-size:9pt; }.default {color: White; font-family:Arial, Helvetica; font-size:9pt; font-weight: normal}.ST {color: White; font-family:Arial, Helvetica; font-size:8pt; font-weight: normal}.logoText {color: red; font-family: Arial Black, Helvetica, sans-serif; font-size: 25pt; font-weight: normal; letter-spacing : -2.5px;}.flagText {color: blue; font-family: webdings; font-size: 36pt; font-weight: normal; }.ltv {color: blue; font-family: Arial, Helvetica, sans-serif; font-size: 9pt; font-weight: normal;}.tnl {color: black; font-family: Arial, Helvetica, sans-serif; font-size: 10pt; font-weight: bold; text-decoration: none;}--></style></HEAD><BODY topmargin=0 leftmargin=0 marginheight=0 marginwidth=0 bgcolor=#000000 text=#EEEEEE link=#001155 vlink=#001155 alink=#FF0000><font class=default><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td height=50><font class=flagText>U</font><font class=logoText>&nbsp;SHOUTcast D.N.A.S. Status</font></td></tr><tr><td height=14 align=right><font class=ltv><a id=ltv href="http://www.shoutcast.com/">SHOUTcast Server Version 1.9.8/Linux</a></font></td></tr><tr><td bgcolor=#DDDDDD height=20 align=center><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td align=center><font class=tnl><a id=tnl href="index.html">Status</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="played.html">Song History</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="listen.pls">Listen</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="home.html">Stream URL</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="admin.cgi">Admin Login</a></font></td></tr></table></td></tr></table><br><table cellpadding=5 cellspacing=0 border=0 width=100%><tr><td bgcolor=#000025 colspan=2 align=center><font class=ST>Current Stream Information</font></td></tr></table><table cellpadding=2 cellspacing=0 border=0 align=center><tr><td width=100 nowrap><font class=default>Server Status: </font></td><td><font class=default><b>Server is currently up and private.</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Status: </font></td><td><font class=default><b>Stream is up at 128 kbps with <B>0 of 50 listeners (0 unique)</b></b></td></tr><tr><td width=100 nowrap><font class=default>Listener Peak: </font></td><td><font class=default><b>0</b></td></tr><tr><td width=100 nowrap><font class=default>Average Listen Time: </font></td><td><font class=default><b>0m&nbsp;01s</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Title: </font></td><td><font class=default><b>TI-Radio AutoDj</b></td></tr><tr><td width=100 nowrap><font class=default>Content Type: </font></td><td><font class=default><b>audio/mpeg</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Genre: </font></td><td><font class=default><b>Various</b></td></tr><tr><td width=100 nowrap><font class=default>Stream URL: </font></td><td><font class=default><b><a href="http://www.torrent-invites.com/">http://www.torrent-invites.com/</a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream ICQ: </font></td><td><font class=default><b><a href="http://wwp.icq.com/scripts/contact.dll?msgto="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream AIM: </font></td><td><font class=default><b><a href="aim:goim?screenname="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream IRC: </font></td><td><font class=default><b><a href="http://www.shoutcast.com/chat.phtml?dc="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Current Song: </font></td><td><font class=default><b>K-Ci and Jo Jo - Crazy</b></td></tr></table><br><table cellpadding=0 cellspacing=0 border=0 width=100%>    <tr><td bgcolor=#DDDDDD  nowrap colspan=5 align=center><table cellspacing=0 cellpadding=0 border=0><tr><td><font class=ltv>Written by Stephen 'Tag Loomis, Tom Pepper and Justin Frankel</font></td></tr></table></td></tr><tr><td nowrap colspan=5 align=center><font class=ST><b><a href="http://www.shoutcast.com/disclaimer.phtml">Copyright Nullsoft Inc</a><a href="/llamacookie">.</a> 1998-2004</b></font></td></tr></table></font></body></html>"""

root = lxml.etree.fromstring(samplexml)  # an lxml.etree.Element object


# to load directly from a file, do
tree = lxml.etree.parse("http://ukparse.kforge.net/parldata/scrapedxml/debates/debates2010-03-29a.xml")
root = tree.getroot()  # tree is an ElementTree object.  findall works for the whole document

print root
print lxml.etree.tostring(root)

# uncomment each line to test it
print root.tag, len(root), list(root), root[0]  # the Element object can like a list

# element objects carry a dict for the attributes
# print root.get("v")   # returns qqqq
#print root.get("vvv") # returns None (doesn't exist)
#print root.keys()     # list of keys available

print root.findall("b")[0].text
#print root.findall("hh2")   # nothing
#print root.findall(".//hh2")   # anywhere in the list

# just the text within an element



## lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The parsed objects are slightly different between the two.  
# This tutorial walks through the xml features

import lxml.etree

# create an example case
samplexml = """<HTML><HEAD><meta http-equiv="Content-Language" content="en-us"><meta http-equiv="Content-Type" content="text/html; charset=windows-1252"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="Mon, 01 Jan 1990 12:00:00 GMT"><title>SHOUTcast Administrator</title><style type="text/css"><!--a:link {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:visited {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:hover {color: red; font-family:Arial, Helvetica; font-size:9pt; }.default {color: White; font-family:Arial, Helvetica; font-size:9pt; font-weight: normal}.ST {color: White; font-family:Arial, Helvetica; font-size:8pt; font-weight: normal}.logoText {color: red; font-family: Arial Black, Helvetica, sans-serif; font-size: 25pt; font-weight: normal; letter-spacing : -2.5px;}.flagText {color: blue; font-family: webdings; font-size: 36pt; font-weight: normal; }.ltv {color: blue; font-family: Arial, Helvetica, sans-serif; font-size: 9pt; font-weight: normal;}.tnl {color: black; font-family: Arial, Helvetica, sans-serif; font-size: 10pt; font-weight: bold; text-decoration: none;}--></style></HEAD><BODY topmargin=0 leftmargin=0 marginheight=0 marginwidth=0 bgcolor=#000000 text=#EEEEEE link=#001155 vlink=#001155 alink=#FF0000><font class=default><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td height=50><font class=flagText>U</font><font class=logoText>&nbsp;SHOUTcast D.N.A.S. Status</font></td></tr><tr><td height=14 align=right><font class=ltv><a id=ltv href="http://www.shoutcast.com/">SHOUTcast Server Version 1.9.8/Linux</a></font></td></tr><tr><td bgcolor=#DDDDDD height=20 align=center><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td align=center><font class=tnl><a id=tnl href="index.html">Status</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="played.html">Song History</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="listen.pls">Listen</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="home.html">Stream URL</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="admin.cgi">Admin Login</a></font></td></tr></table></td></tr></table><br><table cellpadding=5 cellspacing=0 border=0 width=100%><tr><td bgcolor=#000025 colspan=2 align=center><font class=ST>Current Stream Information</font></td></tr></table><table cellpadding=2 cellspacing=0 border=0 align=center><tr><td width=100 nowrap><font class=default>Server Status: </font></td><td><font class=default><b>Server is currently up and private.</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Status: </font></td><td><font class=default><b>Stream is up at 128 kbps with <B>0 of 50 listeners (0 unique)</b></b></td></tr><tr><td width=100 nowrap><font class=default>Listener Peak: </font></td><td><font class=default><b>0</b></td></tr><tr><td width=100 nowrap><font class=default>Average Listen Time: </font></td><td><font class=default><b>0m&nbsp;01s</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Title: </font></td><td><font class=default><b>TI-Radio AutoDj</b></td></tr><tr><td width=100 nowrap><font class=default>Content Type: </font></td><td><font class=default><b>audio/mpeg</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Genre: </font></td><td><font class=default><b>Various</b></td></tr><tr><td width=100 nowrap><font class=default>Stream URL: </font></td><td><font class=default><b><a href="http://www.torrent-invites.com/">http://www.torrent-invites.com/</a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream ICQ: </font></td><td><font class=default><b><a href="http://wwp.icq.com/scripts/contact.dll?msgto="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream AIM: </font></td><td><font class=default><b><a href="aim:goim?screenname="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream IRC: </font></td><td><font class=default><b><a href="http://www.shoutcast.com/chat.phtml?dc="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Current Song: </font></td><td><font class=default><b>K-Ci and Jo Jo - Crazy</b></td></tr></table><br><table cellpadding=0 cellspacing=0 border=0 width=100%>    <tr><td bgcolor=#DDDDDD  nowrap colspan=5 align=center><table cellspacing=0 cellpadding=0 border=0><tr><td><font class=ltv>Written by Stephen 'Tag Loomis, Tom Pepper and Justin Frankel</font></td></tr></table></td></tr><tr><td nowrap colspan=5 align=center><font class=ST><b><a href="http://www.shoutcast.com/disclaimer.phtml">Copyright Nullsoft Inc</a><a href="/llamacookie">.</a> 1998-2004</b></font></td></tr></table></font></body></html>"""

root = lxml.etree.fromstring(samplexml)  # an lxml.etree.Element object


# to load directly from a file, do
tree = lxml.etree.parse("http://ukparse.kforge.net/parldata/scrapedxml/debates/debates2010-03-29a.xml")
root = tree.getroot()  # tree is an ElementTree object.  findall works for the whole document

print root
print lxml.etree.tostring(root)

# uncomment each line to test it
print root.tag, len(root), list(root), root[0]  # the Element object can like a list

# element objects carry a dict for the attributes
# print root.get("v")   # returns qqqq
#print root.get("vvv") # returns None (doesn't exist)
#print root.keys()     # list of keys available

print root.findall("b")[0].text
#print root.findall("hh2")   # nothing
#print root.findall(".//hh2")   # anywhere in the list

# just the text within an element



## lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The parsed objects are slightly different between the two.  
# This tutorial walks through the xml features

import lxml.etree

# create an example case
samplexml = """<HTML><HEAD><meta http-equiv="Content-Language" content="en-us"><meta http-equiv="Content-Type" content="text/html; charset=windows-1252"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="Mon, 01 Jan 1990 12:00:00 GMT"><title>SHOUTcast Administrator</title><style type="text/css"><!--a:link {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:visited {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:hover {color: red; font-family:Arial, Helvetica; font-size:9pt; }.default {color: White; font-family:Arial, Helvetica; font-size:9pt; font-weight: normal}.ST {color: White; font-family:Arial, Helvetica; font-size:8pt; font-weight: normal}.logoText {color: red; font-family: Arial Black, Helvetica, sans-serif; font-size: 25pt; font-weight: normal; letter-spacing : -2.5px;}.flagText {color: blue; font-family: webdings; font-size: 36pt; font-weight: normal; }.ltv {color: blue; font-family: Arial, Helvetica, sans-serif; font-size: 9pt; font-weight: normal;}.tnl {color: black; font-family: Arial, Helvetica, sans-serif; font-size: 10pt; font-weight: bold; text-decoration: none;}--></style></HEAD><BODY topmargin=0 leftmargin=0 marginheight=0 marginwidth=0 bgcolor=#000000 text=#EEEEEE link=#001155 vlink=#001155 alink=#FF0000><font class=default><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td height=50><font class=flagText>U</font><font class=logoText>&nbsp;SHOUTcast D.N.A.S. Status</font></td></tr><tr><td height=14 align=right><font class=ltv><a id=ltv href="http://www.shoutcast.com/">SHOUTcast Server Version 1.9.8/Linux</a></font></td></tr><tr><td bgcolor=#DDDDDD height=20 align=center><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td align=center><font class=tnl><a id=tnl href="index.html">Status</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="played.html">Song History</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="listen.pls">Listen</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="home.html">Stream URL</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="admin.cgi">Admin Login</a></font></td></tr></table></td></tr></table><br><table cellpadding=5 cellspacing=0 border=0 width=100%><tr><td bgcolor=#000025 colspan=2 align=center><font class=ST>Current Stream Information</font></td></tr></table><table cellpadding=2 cellspacing=0 border=0 align=center><tr><td width=100 nowrap><font class=default>Server Status: </font></td><td><font class=default><b>Server is currently up and private.</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Status: </font></td><td><font class=default><b>Stream is up at 128 kbps with <B>0 of 50 listeners (0 unique)</b></b></td></tr><tr><td width=100 nowrap><font class=default>Listener Peak: </font></td><td><font class=default><b>0</b></td></tr><tr><td width=100 nowrap><font class=default>Average Listen Time: </font></td><td><font class=default><b>0m&nbsp;01s</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Title: </font></td><td><font class=default><b>TI-Radio AutoDj</b></td></tr><tr><td width=100 nowrap><font class=default>Content Type: </font></td><td><font class=default><b>audio/mpeg</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Genre: </font></td><td><font class=default><b>Various</b></td></tr><tr><td width=100 nowrap><font class=default>Stream URL: </font></td><td><font class=default><b><a href="http://www.torrent-invites.com/">http://www.torrent-invites.com/</a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream ICQ: </font></td><td><font class=default><b><a href="http://wwp.icq.com/scripts/contact.dll?msgto="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream AIM: </font></td><td><font class=default><b><a href="aim:goim?screenname="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream IRC: </font></td><td><font class=default><b><a href="http://www.shoutcast.com/chat.phtml?dc="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Current Song: </font></td><td><font class=default><b>K-Ci and Jo Jo - Crazy</b></td></tr></table><br><table cellpadding=0 cellspacing=0 border=0 width=100%>    <tr><td bgcolor=#DDDDDD  nowrap colspan=5 align=center><table cellspacing=0 cellpadding=0 border=0><tr><td><font class=ltv>Written by Stephen 'Tag Loomis, Tom Pepper and Justin Frankel</font></td></tr></table></td></tr><tr><td nowrap colspan=5 align=center><font class=ST><b><a href="http://www.shoutcast.com/disclaimer.phtml">Copyright Nullsoft Inc</a><a href="/llamacookie">.</a> 1998-2004</b></font></td></tr></table></font></body></html>"""

root = lxml.etree.fromstring(samplexml)  # an lxml.etree.Element object


# to load directly from a file, do
tree = lxml.etree.parse("http://ukparse.kforge.net/parldata/scrapedxml/debates/debates2010-03-29a.xml")
root = tree.getroot()  # tree is an ElementTree object.  findall works for the whole document

print root
print lxml.etree.tostring(root)

# uncomment each line to test it
print root.tag, len(root), list(root), root[0]  # the Element object can like a list

# element objects carry a dict for the attributes
# print root.get("v")   # returns qqqq
#print root.get("vvv") # returns None (doesn't exist)
#print root.keys()     # list of keys available

print root.findall("b")[0].text
#print root.findall("hh2")   # nothing
#print root.findall(".//hh2")   # anywhere in the list

# just the text within an element



## lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The parsed objects are slightly different between the two.  
# This tutorial walks through the xml features

import lxml.etree

# create an example case
samplexml = """<HTML><HEAD><meta http-equiv="Content-Language" content="en-us"><meta http-equiv="Content-Type" content="text/html; charset=windows-1252"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="Mon, 01 Jan 1990 12:00:00 GMT"><title>SHOUTcast Administrator</title><style type="text/css"><!--a:link {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:visited {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:hover {color: red; font-family:Arial, Helvetica; font-size:9pt; }.default {color: White; font-family:Arial, Helvetica; font-size:9pt; font-weight: normal}.ST {color: White; font-family:Arial, Helvetica; font-size:8pt; font-weight: normal}.logoText {color: red; font-family: Arial Black, Helvetica, sans-serif; font-size: 25pt; font-weight: normal; letter-spacing : -2.5px;}.flagText {color: blue; font-family: webdings; font-size: 36pt; font-weight: normal; }.ltv {color: blue; font-family: Arial, Helvetica, sans-serif; font-size: 9pt; font-weight: normal;}.tnl {color: black; font-family: Arial, Helvetica, sans-serif; font-size: 10pt; font-weight: bold; text-decoration: none;}--></style></HEAD><BODY topmargin=0 leftmargin=0 marginheight=0 marginwidth=0 bgcolor=#000000 text=#EEEEEE link=#001155 vlink=#001155 alink=#FF0000><font class=default><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td height=50><font class=flagText>U</font><font class=logoText>&nbsp;SHOUTcast D.N.A.S. Status</font></td></tr><tr><td height=14 align=right><font class=ltv><a id=ltv href="http://www.shoutcast.com/">SHOUTcast Server Version 1.9.8/Linux</a></font></td></tr><tr><td bgcolor=#DDDDDD height=20 align=center><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td align=center><font class=tnl><a id=tnl href="index.html">Status</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="played.html">Song History</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="listen.pls">Listen</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="home.html">Stream URL</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="admin.cgi">Admin Login</a></font></td></tr></table></td></tr></table><br><table cellpadding=5 cellspacing=0 border=0 width=100%><tr><td bgcolor=#000025 colspan=2 align=center><font class=ST>Current Stream Information</font></td></tr></table><table cellpadding=2 cellspacing=0 border=0 align=center><tr><td width=100 nowrap><font class=default>Server Status: </font></td><td><font class=default><b>Server is currently up and private.</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Status: </font></td><td><font class=default><b>Stream is up at 128 kbps with <B>0 of 50 listeners (0 unique)</b></b></td></tr><tr><td width=100 nowrap><font class=default>Listener Peak: </font></td><td><font class=default><b>0</b></td></tr><tr><td width=100 nowrap><font class=default>Average Listen Time: </font></td><td><font class=default><b>0m&nbsp;01s</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Title: </font></td><td><font class=default><b>TI-Radio AutoDj</b></td></tr><tr><td width=100 nowrap><font class=default>Content Type: </font></td><td><font class=default><b>audio/mpeg</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Genre: </font></td><td><font class=default><b>Various</b></td></tr><tr><td width=100 nowrap><font class=default>Stream URL: </font></td><td><font class=default><b><a href="http://www.torrent-invites.com/">http://www.torrent-invites.com/</a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream ICQ: </font></td><td><font class=default><b><a href="http://wwp.icq.com/scripts/contact.dll?msgto="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream AIM: </font></td><td><font class=default><b><a href="aim:goim?screenname="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream IRC: </font></td><td><font class=default><b><a href="http://www.shoutcast.com/chat.phtml?dc="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Current Song: </font></td><td><font class=default><b>K-Ci and Jo Jo - Crazy</b></td></tr></table><br><table cellpadding=0 cellspacing=0 border=0 width=100%>    <tr><td bgcolor=#DDDDDD  nowrap colspan=5 align=center><table cellspacing=0 cellpadding=0 border=0><tr><td><font class=ltv>Written by Stephen 'Tag Loomis, Tom Pepper and Justin Frankel</font></td></tr></table></td></tr><tr><td nowrap colspan=5 align=center><font class=ST><b><a href="http://www.shoutcast.com/disclaimer.phtml">Copyright Nullsoft Inc</a><a href="/llamacookie">.</a> 1998-2004</b></font></td></tr></table></font></body></html>"""

root = lxml.etree.fromstring(samplexml)  # an lxml.etree.Element object


# to load directly from a file, do
tree = lxml.etree.parse("http://ukparse.kforge.net/parldata/scrapedxml/debates/debates2010-03-29a.xml")
root = tree.getroot()  # tree is an ElementTree object.  findall works for the whole document

print root
print lxml.etree.tostring(root)

# uncomment each line to test it
print root.tag, len(root), list(root), root[0]  # the Element object can like a list

# element objects carry a dict for the attributes
# print root.get("v")   # returns qqqq
#print root.get("vvv") # returns None (doesn't exist)
#print root.keys()     # list of keys available

print root.findall("b")[0].text
#print root.findall("hh2")   # nothing
#print root.findall(".//hh2")   # anywhere in the list

# just the text within an element



## lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The parsed objects are slightly different between the two.  
# This tutorial walks through the xml features

import lxml.etree

# create an example case
samplexml = """<HTML><HEAD><meta http-equiv="Content-Language" content="en-us"><meta http-equiv="Content-Type" content="text/html; charset=windows-1252"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="Mon, 01 Jan 1990 12:00:00 GMT"><title>SHOUTcast Administrator</title><style type="text/css"><!--a:link {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:visited {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:hover {color: red; font-family:Arial, Helvetica; font-size:9pt; }.default {color: White; font-family:Arial, Helvetica; font-size:9pt; font-weight: normal}.ST {color: White; font-family:Arial, Helvetica; font-size:8pt; font-weight: normal}.logoText {color: red; font-family: Arial Black, Helvetica, sans-serif; font-size: 25pt; font-weight: normal; letter-spacing : -2.5px;}.flagText {color: blue; font-family: webdings; font-size: 36pt; font-weight: normal; }.ltv {color: blue; font-family: Arial, Helvetica, sans-serif; font-size: 9pt; font-weight: normal;}.tnl {color: black; font-family: Arial, Helvetica, sans-serif; font-size: 10pt; font-weight: bold; text-decoration: none;}--></style></HEAD><BODY topmargin=0 leftmargin=0 marginheight=0 marginwidth=0 bgcolor=#000000 text=#EEEEEE link=#001155 vlink=#001155 alink=#FF0000><font class=default><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td height=50><font class=flagText>U</font><font class=logoText>&nbsp;SHOUTcast D.N.A.S. Status</font></td></tr><tr><td height=14 align=right><font class=ltv><a id=ltv href="http://www.shoutcast.com/">SHOUTcast Server Version 1.9.8/Linux</a></font></td></tr><tr><td bgcolor=#DDDDDD height=20 align=center><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td align=center><font class=tnl><a id=tnl href="index.html">Status</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="played.html">Song History</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="listen.pls">Listen</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="home.html">Stream URL</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="admin.cgi">Admin Login</a></font></td></tr></table></td></tr></table><br><table cellpadding=5 cellspacing=0 border=0 width=100%><tr><td bgcolor=#000025 colspan=2 align=center><font class=ST>Current Stream Information</font></td></tr></table><table cellpadding=2 cellspacing=0 border=0 align=center><tr><td width=100 nowrap><font class=default>Server Status: </font></td><td><font class=default><b>Server is currently up and private.</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Status: </font></td><td><font class=default><b>Stream is up at 128 kbps with <B>0 of 50 listeners (0 unique)</b></b></td></tr><tr><td width=100 nowrap><font class=default>Listener Peak: </font></td><td><font class=default><b>0</b></td></tr><tr><td width=100 nowrap><font class=default>Average Listen Time: </font></td><td><font class=default><b>0m&nbsp;01s</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Title: </font></td><td><font class=default><b>TI-Radio AutoDj</b></td></tr><tr><td width=100 nowrap><font class=default>Content Type: </font></td><td><font class=default><b>audio/mpeg</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Genre: </font></td><td><font class=default><b>Various</b></td></tr><tr><td width=100 nowrap><font class=default>Stream URL: </font></td><td><font class=default><b><a href="http://www.torrent-invites.com/">http://www.torrent-invites.com/</a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream ICQ: </font></td><td><font class=default><b><a href="http://wwp.icq.com/scripts/contact.dll?msgto="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream AIM: </font></td><td><font class=default><b><a href="aim:goim?screenname="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream IRC: </font></td><td><font class=default><b><a href="http://www.shoutcast.com/chat.phtml?dc="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Current Song: </font></td><td><font class=default><b>K-Ci and Jo Jo - Crazy</b></td></tr></table><br><table cellpadding=0 cellspacing=0 border=0 width=100%>    <tr><td bgcolor=#DDDDDD  nowrap colspan=5 align=center><table cellspacing=0 cellpadding=0 border=0><tr><td><font class=ltv>Written by Stephen 'Tag Loomis, Tom Pepper and Justin Frankel</font></td></tr></table></td></tr><tr><td nowrap colspan=5 align=center><font class=ST><b><a href="http://www.shoutcast.com/disclaimer.phtml">Copyright Nullsoft Inc</a><a href="/llamacookie">.</a> 1998-2004</b></font></td></tr></table></font></body></html>"""

root = lxml.etree.fromstring(samplexml)  # an lxml.etree.Element object


# to load directly from a file, do
tree = lxml.etree.parse("http://ukparse.kforge.net/parldata/scrapedxml/debates/debates2010-03-29a.xml")
root = tree.getroot()  # tree is an ElementTree object.  findall works for the whole document

print root
print lxml.etree.tostring(root)

# uncomment each line to test it
print root.tag, len(root), list(root), root[0]  # the Element object can like a list

# element objects carry a dict for the attributes
# print root.get("v")   # returns qqqq
#print root.get("vvv") # returns None (doesn't exist)
#print root.keys()     # list of keys available

print root.findall("b")[0].text
#print root.findall("hh2")   # nothing
#print root.findall(".//hh2")   # anywhere in the list

# just the text within an element



## lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The parsed objects are slightly different between the two.  
# This tutorial walks through the xml features

import lxml.etree

# create an example case
samplexml = """<HTML><HEAD><meta http-equiv="Content-Language" content="en-us"><meta http-equiv="Content-Type" content="text/html; charset=windows-1252"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="Mon, 01 Jan 1990 12:00:00 GMT"><title>SHOUTcast Administrator</title><style type="text/css"><!--a:link {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:visited {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:hover {color: red; font-family:Arial, Helvetica; font-size:9pt; }.default {color: White; font-family:Arial, Helvetica; font-size:9pt; font-weight: normal}.ST {color: White; font-family:Arial, Helvetica; font-size:8pt; font-weight: normal}.logoText {color: red; font-family: Arial Black, Helvetica, sans-serif; font-size: 25pt; font-weight: normal; letter-spacing : -2.5px;}.flagText {color: blue; font-family: webdings; font-size: 36pt; font-weight: normal; }.ltv {color: blue; font-family: Arial, Helvetica, sans-serif; font-size: 9pt; font-weight: normal;}.tnl {color: black; font-family: Arial, Helvetica, sans-serif; font-size: 10pt; font-weight: bold; text-decoration: none;}--></style></HEAD><BODY topmargin=0 leftmargin=0 marginheight=0 marginwidth=0 bgcolor=#000000 text=#EEEEEE link=#001155 vlink=#001155 alink=#FF0000><font class=default><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td height=50><font class=flagText>U</font><font class=logoText>&nbsp;SHOUTcast D.N.A.S. Status</font></td></tr><tr><td height=14 align=right><font class=ltv><a id=ltv href="http://www.shoutcast.com/">SHOUTcast Server Version 1.9.8/Linux</a></font></td></tr><tr><td bgcolor=#DDDDDD height=20 align=center><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td align=center><font class=tnl><a id=tnl href="index.html">Status</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="played.html">Song History</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="listen.pls">Listen</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="home.html">Stream URL</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="admin.cgi">Admin Login</a></font></td></tr></table></td></tr></table><br><table cellpadding=5 cellspacing=0 border=0 width=100%><tr><td bgcolor=#000025 colspan=2 align=center><font class=ST>Current Stream Information</font></td></tr></table><table cellpadding=2 cellspacing=0 border=0 align=center><tr><td width=100 nowrap><font class=default>Server Status: </font></td><td><font class=default><b>Server is currently up and private.</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Status: </font></td><td><font class=default><b>Stream is up at 128 kbps with <B>0 of 50 listeners (0 unique)</b></b></td></tr><tr><td width=100 nowrap><font class=default>Listener Peak: </font></td><td><font class=default><b>0</b></td></tr><tr><td width=100 nowrap><font class=default>Average Listen Time: </font></td><td><font class=default><b>0m&nbsp;01s</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Title: </font></td><td><font class=default><b>TI-Radio AutoDj</b></td></tr><tr><td width=100 nowrap><font class=default>Content Type: </font></td><td><font class=default><b>audio/mpeg</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Genre: </font></td><td><font class=default><b>Various</b></td></tr><tr><td width=100 nowrap><font class=default>Stream URL: </font></td><td><font class=default><b><a href="http://www.torrent-invites.com/">http://www.torrent-invites.com/</a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream ICQ: </font></td><td><font class=default><b><a href="http://wwp.icq.com/scripts/contact.dll?msgto="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream AIM: </font></td><td><font class=default><b><a href="aim:goim?screenname="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream IRC: </font></td><td><font class=default><b><a href="http://www.shoutcast.com/chat.phtml?dc="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Current Song: </font></td><td><font class=default><b>K-Ci and Jo Jo - Crazy</b></td></tr></table><br><table cellpadding=0 cellspacing=0 border=0 width=100%>    <tr><td bgcolor=#DDDDDD  nowrap colspan=5 align=center><table cellspacing=0 cellpadding=0 border=0><tr><td><font class=ltv>Written by Stephen 'Tag Loomis, Tom Pepper and Justin Frankel</font></td></tr></table></td></tr><tr><td nowrap colspan=5 align=center><font class=ST><b><a href="http://www.shoutcast.com/disclaimer.phtml">Copyright Nullsoft Inc</a><a href="/llamacookie">.</a> 1998-2004</b></font></td></tr></table></font></body></html>"""

root = lxml.etree.fromstring(samplexml)  # an lxml.etree.Element object


# to load directly from a file, do
tree = lxml.etree.parse("http://ukparse.kforge.net/parldata/scrapedxml/debates/debates2010-03-29a.xml")
root = tree.getroot()  # tree is an ElementTree object.  findall works for the whole document

print root
print lxml.etree.tostring(root)

# uncomment each line to test it
print root.tag, len(root), list(root), root[0]  # the Element object can like a list

# element objects carry a dict for the attributes
# print root.get("v")   # returns qqqq
#print root.get("vvv") # returns None (doesn't exist)
#print root.keys()     # list of keys available

print root.findall("b")[0].text
#print root.findall("hh2")   # nothing
#print root.findall(".//hh2")   # anywhere in the list

# just the text within an element



## lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The parsed objects are slightly different between the two.  
# This tutorial walks through the xml features

import lxml.etree

# create an example case
samplexml = """<HTML><HEAD><meta http-equiv="Content-Language" content="en-us"><meta http-equiv="Content-Type" content="text/html; charset=windows-1252"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="Mon, 01 Jan 1990 12:00:00 GMT"><title>SHOUTcast Administrator</title><style type="text/css"><!--a:link {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:visited {color: blue; font-family:Arial, Helvetica; font-size:9pt;}a:hover {color: red; font-family:Arial, Helvetica; font-size:9pt; }.default {color: White; font-family:Arial, Helvetica; font-size:9pt; font-weight: normal}.ST {color: White; font-family:Arial, Helvetica; font-size:8pt; font-weight: normal}.logoText {color: red; font-family: Arial Black, Helvetica, sans-serif; font-size: 25pt; font-weight: normal; letter-spacing : -2.5px;}.flagText {color: blue; font-family: webdings; font-size: 36pt; font-weight: normal; }.ltv {color: blue; font-family: Arial, Helvetica, sans-serif; font-size: 9pt; font-weight: normal;}.tnl {color: black; font-family: Arial, Helvetica, sans-serif; font-size: 10pt; font-weight: bold; text-decoration: none;}--></style></HEAD><BODY topmargin=0 leftmargin=0 marginheight=0 marginwidth=0 bgcolor=#000000 text=#EEEEEE link=#001155 vlink=#001155 alink=#FF0000><font class=default><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td height=50><font class=flagText>U</font><font class=logoText>&nbsp;SHOUTcast D.N.A.S. Status</font></td></tr><tr><td height=14 align=right><font class=ltv><a id=ltv href="http://www.shoutcast.com/">SHOUTcast Server Version 1.9.8/Linux</a></font></td></tr><tr><td bgcolor=#DDDDDD height=20 align=center><table width=100% border=0 cellpadding=0 cellspacing=0><tr><td align=center><font class=tnl><a id=tnl href="index.html">Status</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="played.html">Song History</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="listen.pls">Listen</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="home.html">Stream URL</a></font></td><td align=center><font class=tnl>&nbsp;|&nbsp;</font></td><td align=center><font class=tnl><a id=tnl href="admin.cgi">Admin Login</a></font></td></tr></table></td></tr></table><br><table cellpadding=5 cellspacing=0 border=0 width=100%><tr><td bgcolor=#000025 colspan=2 align=center><font class=ST>Current Stream Information</font></td></tr></table><table cellpadding=2 cellspacing=0 border=0 align=center><tr><td width=100 nowrap><font class=default>Server Status: </font></td><td><font class=default><b>Server is currently up and private.</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Status: </font></td><td><font class=default><b>Stream is up at 128 kbps with <B>0 of 50 listeners (0 unique)</b></b></td></tr><tr><td width=100 nowrap><font class=default>Listener Peak: </font></td><td><font class=default><b>0</b></td></tr><tr><td width=100 nowrap><font class=default>Average Listen Time: </font></td><td><font class=default><b>0m&nbsp;01s</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Title: </font></td><td><font class=default><b>TI-Radio AutoDj</b></td></tr><tr><td width=100 nowrap><font class=default>Content Type: </font></td><td><font class=default><b>audio/mpeg</b></td></tr><tr><td width=100 nowrap><font class=default>Stream Genre: </font></td><td><font class=default><b>Various</b></td></tr><tr><td width=100 nowrap><font class=default>Stream URL: </font></td><td><font class=default><b><a href="http://www.torrent-invites.com/">http://www.torrent-invites.com/</a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream ICQ: </font></td><td><font class=default><b><a href="http://wwp.icq.com/scripts/contact.dll?msgto="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream AIM: </font></td><td><font class=default><b><a href="aim:goim?screenname="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Stream IRC: </font></td><td><font class=default><b><a href="http://www.shoutcast.com/chat.phtml?dc="></a></b></td></tr><tr><td width=100 nowrap><font class=default>Current Song: </font></td><td><font class=default><b>K-Ci and Jo Jo - Crazy</b></td></tr></table><br><table cellpadding=0 cellspacing=0 border=0 width=100%>    <tr><td bgcolor=#DDDDDD  nowrap colspan=5 align=center><table cellspacing=0 cellpadding=0 border=0><tr><td><font class=ltv>Written by Stephen 'Tag Loomis, Tom Pepper and Justin Frankel</font></td></tr></table></td></tr><tr><td nowrap colspan=5 align=center><font class=ST><b><a href="http://www.shoutcast.com/disclaimer.phtml">Copyright Nullsoft Inc</a><a href="/llamacookie">.</a> 1998-2004</b></font></td></tr></table></font></body></html>"""

root = lxml.etree.fromstring(samplexml)  # an lxml.etree.Element object


# to load directly from a file, do
tree = lxml.etree.parse("http://ukparse.kforge.net/parldata/scrapedxml/debates/debates2010-03-29a.xml")
root = tree.getroot()  # tree is an ElementTree object.  findall works for the whole document

print root
print lxml.etree.tostring(root)

# uncomment each line to test it
print root.tag, len(root), list(root), root[0]  # the Element object can like a list

# element objects carry a dict for the attributes
# print root.get("v")   # returns qqqq
#print root.get("vvv") # returns None (doesn't exist)
#print root.keys()     # list of keys available

print root.findall("b")[0].text
#print root.findall("hh2")   # nothing
#print root.findall(".//hh2")   # anywhere in the list

# just the text within an element



