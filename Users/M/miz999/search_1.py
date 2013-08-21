# -*- coding: utf-8 -*-
sourcescraper = 'tvtimetable'

import urllib
from BeautifulSoup import BeautifulSoup, Comment
import re
import sys
from datetime import datetime, timedelta
import sqlite3
from BeautifulSoup import BeautifulStoneSoup
import scraperwiki
import cgi
import os

stdin = sys.stdin
stdout = sys.stdout
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdin = stdin
sys.stdout = stdout

searchHTML = ''

def makeQueryPage():
    global searchHTML

    chHtml = ''
    scraperwiki.sqlite.attach('tvtimetable')
    scraperwiki.sqlite.attach('tvtimetablebs')
    sqlstr = 'ch from (select distinct ch from tvTimeTablebs.swdata union all select distinct ch from tvTimeTable.swdata)'
    a = scraperwiki.sqlite.select(sqlstr)
    for row in a:
        chHtml += '<input type="checkbox" name="ch" value="%s">%s' % (row['ch'], row['ch'])
#        html += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (row['ch'],row['title'],row['start'],row['shosai'])
#        print html
    searchHTML = """
<html>
<head>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
</head>
<body>
<script language="JavaScript">
<!--
function encodeForm(){
document.f1.genre.value = escape(document.f1.genre.value);
return true;
}
//-->
</script>
<form name="f1" method="get" accept-charset="utf-8" action="" onSubmit="return encodeForm()">
<fieldset>
<legend>チャンネル</legend>
"""
    searchHTML += chHtml
    searchHTML += """
</fieldset>

<p>タイトル<br>
<input type="text" name="title" size="30" maxlength="30" value="">
</p>

<p>番組詳細<br>
<input type="text" name="shosai" size="30" maxlength="30" value="">
</p>

<p>ジャンル<br>
<input type="text" name="genre" size="30" maxlength="30" value="">
</p>

<p><input type="submit" value="送信する"></p>

</form></body></html>
"""


def search(query):
#    print query

    where = ""
    whereList = []
    chList = []
    import urllib

    if query.has_key('ch'):
        print query['ch']
        ch = query['ch'].split(',')
        for i in ch:
            chList.append("ch='%s'" % i)
        chListSql = '(' + ' or '.join(chList) + ')'
#        print chListSql
        whereList.append(chListSql)
        
    if query.has_key('title'):
        title = query['title']
        whereList.append("title like '%s'" % title)

    if query.has_key('shosai'):
        title = query['shosai']
        whereList.append("shosai like '%s'" % shosai)

    if query.has_key('genre'):
        genre = query['genre']
        print genre
        genre = urllib.unquote(genre)
        print genre, type(genre)
#        print 'genre' , type(genre)
#        genre.decode('ascii')
        whereList.append("genre like '%%%s%%'" % genre)

    scraperwiki.sqlite.attach(sourcescraper)
    if len(whereList) > 0:
        sqlstr = ' * from swdata where ' + ' and '.join(whereList)
    else:
        sqlstr = " * from swdata where (" + ' or '.join(chList) + ')'
#    sqlstr = u'* from swdata where genre like "%野球%"'
#    sqlstr = "* from " + sourcescraper + ".swdata where (" + ' or '.join(chList) + ') and ' + ' and '.join(whereList)
#    sqlstr = "* from swdata where " + ' and '.join(whereList)
#    print sqlstr
#    a = scraperwiki.sqlite.execute(sqlstr)
    a = scraperwiki.sqlite.select(sqlstr)
#    print a
    html = ""
    for row in a:
        html += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (row['ch'],row['title'],row['start'],row['shosai'])
        print html

    print """
<html>
<head>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
   <style type="text/css">
      <!--
table.data td, table.data th {
    border: 1px solid #CAD0DC;
    line-height: 1em;
    padding: 0.3em 0.5em;
}
        -->
    </style>
</head>
<body>

<div>
<img src="https://scraperwiki.com/media/images/powered.png" alt="Powered by ScraperWiki.com" />
</div> 
"""
    print html
    print sqlstr
    print """
</body></html>
"""
#<iframe width="100%" height="400px" src="https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=tvtimetable&query=select%20*%20from%20%60swdata%60%20where%20genre%20like%20%27%25%E9%87%8E%E7%90%83%25%27"></iframe>

#print (u'ああああ')[0]
#print type(u'ああああ')
getQuery = scraperwiki.utils.GET()
#print dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
if getQuery.has_key('ch') or getQuery.has_key('title') or getQuery.has_key('shosai') or getQuery.has_key('genre'):
#    print type((dict(cgi.parse_qsl(os.getenv("QUERY_STRING", ""))))['genre'])
#    print len(((dict(cgi.parse_qsl(os.getenv("QUERY_STRING", ""))))['genre']))
    search(getQuery)
else:
    makeQueryPage()
    print searchHTML

