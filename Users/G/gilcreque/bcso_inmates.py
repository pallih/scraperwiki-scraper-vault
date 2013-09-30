sourcescraper = 'brevard_county_sheriff_inmate_photos'

import scraperwiki
import math

#needed for accessing query strings
import cgi
import os

#checking query strings for page numbers
if "QUERY_STRING" in os.environ:
    get = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    if "page" in get:
        pagenumber = int(get["page"])
else:
    pagenumber = 1

#offset for record grabbing
offset = str((pagenumber*10)-10)

scraperwiki.sqlite.attach("brevard_county_sheriff_inmate_photos")

#determine number of pages
recordlist = scraperwiki.sqlite.select('''count(*) from brevard_county_sheriff_inmate_photos.swdata''')
recordcount = int(recordlist[0]["count(*)"])
pagecount = ((recordcount+10-1) / 10)


data = scraperwiki.sqlite.select(           
    '''* from brevard_county_sheriff_inmate_photos.swdata 
    order by id asc limit '''+offset+''',10'''
)

print "<!DOCTYPE html>"
print "<html lang=\"en\">"
print "  <head>"
print "    <meta charset=\"utf-8\">"
print "    <title>Brevard County Sheriff Inmate Population</title>"
print "    <meta name=\"description\" content=\"\">"
print "    <meta name=\"author\" content=\"\">"
print ""
print "    <!-- Le HTML5 shim, for IE6-8 support of HTML elements -->"
print "    <!--[if lt IE 9]>"
print "      <script src=\"http://html5shim.googlecode.com/svn/trunk/html5.js\"></script>"
print "    <![endif]-->"
print ""
print "    <!-- Le styles -->"
print "      <link rel=\"stylesheet\" href=\"http://twitter.github.com/bootstrap/1.4.0/bootstrap.min.css\">"
print "    <style type=\"text/css\">"
print "      body {"
print "        padding-top: 60px;"
print "      }"
print "    </style>"
print ""
print "    <!-- Le fav and touch icons -->"
print "    <link rel=\"shortcut icon\" href=\"images/favicon.ico\">"
print "    <link rel=\"apple-touch-icon\" href=\"images/apple-touch-icon.png\">"
print "    <link rel=\"apple-touch-icon\" sizes=\"72x72\" href=\"images/apple-touch-icon-72x72.png\">"
print "    <link rel=\"apple-touch-icon\" sizes=\"114x114\" href=\"images/apple-touch-icon-114x114.png\">"
print "  </head>"
print ""
print "  <body>"
print ""
print "    <div class=\"container\">"
print "    <div class=\"content\">"
print "      <div class=\"hero-unit\">"
print "        <h1><a href=\"https://views.scraperwiki.com/run/bcso_inmates/\">Brevard County Sheriff Inmate Population</a></h1>"
print "      </div>"

print "<div class=\"pagination\">"
print "  <ul>"
if pagenumber == 1:
    print "<li class=\"prev disabled\"><a href=\"#\">&larr; Previous</a></li>"
else:
    previouspage = str(pagenumber-1)
    print "<li class=\"prev\"><a href=\"?page="+previouspage+"\">&larr; Previous</a></li>"
current = str(pagenumber)
print "<li class=\"disabled\"><a href=\"#\">"+current+"</a></li>"
if pagenumber == pagecount:
    print "<li class=\"next disabled\"><a href=\"#\">Next &rarr;</a></li>"
else:
    nextpage = str(pagenumber+1)
    print "<li class=\"next\"><a href=\"?page="+nextpage+"\">Next &rarr;</a></li>"
print "  </ul>"
print "</div>"

print "          <div class=\"span16\">"

for d in data:
    print "                <hr />"
    print "                <h2><a href='"+d["report"]+"'>"+d["name"]+"</a></h2>"
    print "                <ul class=\"media-grid\">"
    print "                  <li>"
    print "                    <a href='"+d["report"]+"'>"
    print "                      <img class=\"thumbnail\" src='"+d["photo1"]+"' alt=\"\" width=\"450px\">"
    print "                    </a>"
    print "                  </li>"
    print "                  <li>"
    print "                    <a href='"+d["report"]+"'>"
    print "                      <img class=\"thumbnail\" src='"+d["photo2"]+"' alt=\"\" width=\"450px\">"
    print "                    </a>"
    print "                  </li>"
    print "                </ul>"

print "        <footer>"

print "<div class=\"pagination\">"
print "  <ul>"
if pagenumber == 1:
    print "<li class=\"prev disabled\"><a href=\"#\">&larr; Previous</a></li>"
else:
    previouspage = str(pagenumber-1)
    print "<li class=\"prev\"><a href=\"?page="+previouspage+"\">&larr; Previous</a></li>"
current = str(pagenumber)
print "<li class=\"disabled\"><a href=\"#\">"+current+"</a></li>"
if pagenumber == pagecount:
    print "<li class=\"next disabled\"><a href=\"#\">Next &rarr;</a></li>"
else:
    nextpage = str(pagenumber+1)
    print "<li class=\"next\"><a href=\"?page="+nextpage+"\">Next &rarr;</a></li>"
print "  </ul>"
print "</div>"


print "        </footer>"
print "      </div>"
print "    </div>"
print "    </div>"
print ""
print "  </body>"
print "</html>"sourcescraper = 'brevard_county_sheriff_inmate_photos'

import scraperwiki
import math

#needed for accessing query strings
import cgi
import os

#checking query strings for page numbers
if "QUERY_STRING" in os.environ:
    get = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    if "page" in get:
        pagenumber = int(get["page"])
else:
    pagenumber = 1

#offset for record grabbing
offset = str((pagenumber*10)-10)

scraperwiki.sqlite.attach("brevard_county_sheriff_inmate_photos")

#determine number of pages
recordlist = scraperwiki.sqlite.select('''count(*) from brevard_county_sheriff_inmate_photos.swdata''')
recordcount = int(recordlist[0]["count(*)"])
pagecount = ((recordcount+10-1) / 10)


data = scraperwiki.sqlite.select(           
    '''* from brevard_county_sheriff_inmate_photos.swdata 
    order by id asc limit '''+offset+''',10'''
)

print "<!DOCTYPE html>"
print "<html lang=\"en\">"
print "  <head>"
print "    <meta charset=\"utf-8\">"
print "    <title>Brevard County Sheriff Inmate Population</title>"
print "    <meta name=\"description\" content=\"\">"
print "    <meta name=\"author\" content=\"\">"
print ""
print "    <!-- Le HTML5 shim, for IE6-8 support of HTML elements -->"
print "    <!--[if lt IE 9]>"
print "      <script src=\"http://html5shim.googlecode.com/svn/trunk/html5.js\"></script>"
print "    <![endif]-->"
print ""
print "    <!-- Le styles -->"
print "      <link rel=\"stylesheet\" href=\"http://twitter.github.com/bootstrap/1.4.0/bootstrap.min.css\">"
print "    <style type=\"text/css\">"
print "      body {"
print "        padding-top: 60px;"
print "      }"
print "    </style>"
print ""
print "    <!-- Le fav and touch icons -->"
print "    <link rel=\"shortcut icon\" href=\"images/favicon.ico\">"
print "    <link rel=\"apple-touch-icon\" href=\"images/apple-touch-icon.png\">"
print "    <link rel=\"apple-touch-icon\" sizes=\"72x72\" href=\"images/apple-touch-icon-72x72.png\">"
print "    <link rel=\"apple-touch-icon\" sizes=\"114x114\" href=\"images/apple-touch-icon-114x114.png\">"
print "  </head>"
print ""
print "  <body>"
print ""
print "    <div class=\"container\">"
print "    <div class=\"content\">"
print "      <div class=\"hero-unit\">"
print "        <h1><a href=\"https://views.scraperwiki.com/run/bcso_inmates/\">Brevard County Sheriff Inmate Population</a></h1>"
print "      </div>"

print "<div class=\"pagination\">"
print "  <ul>"
if pagenumber == 1:
    print "<li class=\"prev disabled\"><a href=\"#\">&larr; Previous</a></li>"
else:
    previouspage = str(pagenumber-1)
    print "<li class=\"prev\"><a href=\"?page="+previouspage+"\">&larr; Previous</a></li>"
current = str(pagenumber)
print "<li class=\"disabled\"><a href=\"#\">"+current+"</a></li>"
if pagenumber == pagecount:
    print "<li class=\"next disabled\"><a href=\"#\">Next &rarr;</a></li>"
else:
    nextpage = str(pagenumber+1)
    print "<li class=\"next\"><a href=\"?page="+nextpage+"\">Next &rarr;</a></li>"
print "  </ul>"
print "</div>"

print "          <div class=\"span16\">"

for d in data:
    print "                <hr />"
    print "                <h2><a href='"+d["report"]+"'>"+d["name"]+"</a></h2>"
    print "                <ul class=\"media-grid\">"
    print "                  <li>"
    print "                    <a href='"+d["report"]+"'>"
    print "                      <img class=\"thumbnail\" src='"+d["photo1"]+"' alt=\"\" width=\"450px\">"
    print "                    </a>"
    print "                  </li>"
    print "                  <li>"
    print "                    <a href='"+d["report"]+"'>"
    print "                      <img class=\"thumbnail\" src='"+d["photo2"]+"' alt=\"\" width=\"450px\">"
    print "                    </a>"
    print "                  </li>"
    print "                </ul>"

print "        <footer>"

print "<div class=\"pagination\">"
print "  <ul>"
if pagenumber == 1:
    print "<li class=\"prev disabled\"><a href=\"#\">&larr; Previous</a></li>"
else:
    previouspage = str(pagenumber-1)
    print "<li class=\"prev\"><a href=\"?page="+previouspage+"\">&larr; Previous</a></li>"
current = str(pagenumber)
print "<li class=\"disabled\"><a href=\"#\">"+current+"</a></li>"
if pagenumber == pagecount:
    print "<li class=\"next disabled\"><a href=\"#\">Next &rarr;</a></li>"
else:
    nextpage = str(pagenumber+1)
    print "<li class=\"next\"><a href=\"?page="+nextpage+"\">Next &rarr;</a></li>"
print "  </ul>"
print "</div>"


print "        </footer>"
print "      </div>"
print "    </div>"
print "    </div>"
print ""
print "  </body>"
print "</html>"