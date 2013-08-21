# -*- coding: utf-8 -*-
#sourcescraper = 'tvtimetable'

import re
import sys
from datetime import datetime, timedelta
#import sqlite3
#from BeautifulSoup import BeautifulStoneSoup
import scraperwiki
import cgi
import os
import unicodedata

stdin = sys.stdin
stdout = sys.stdout
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdin = stdin
sys.stdout = stdout

chFree = ['Dlife','FOXbs238','e2ガイド','ウェザーニュース','放送大学BS1','ＢＳ-ＴＢＳ','ＢＳジャパン','ＢＳフジ','ＢＳ日テレ','ＢＳ朝日','ＢＳ１１','ＮＨＫ ＢＳプレミアム','ＮＨＫ ＢＳ１','ＴｗｅｌｌＶ', 'BSスカパー!']

chPay = ['BSアニマックス', 'BS日本映画専門チャンネル', 'BS釣りビジョン', 'IMAGICA BS', 'J SPORTS 1', 'J SPORTS 2','J SPORTS 3','J SPORTS 4','グリーンチャンネル','スター・チャンネル1','スター・チャンネル2','スター・チャンネル3','ディズニー・チャンネル','ＷＯＷＯＷシネマ',
'ＷＯＷＯＷプライム','ＷＯＷＯＷライブ']

def datestr2date(s):
    d = datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')
    return d

WD = ("月","火","水","木","金","土","日")

def d2week(d):
        return '%d/%d(%s)%02d:%02d' % (d.month, d.day, WD[d.weekday()], d.hour, d.minute)

def datestr2week(s):
    d = datestr2date(s)
    return d2week(d)

def output():

    scraperwiki.sqlite.attach('tvtimetable')
    scraperwiki.sqlite.attach('tvtimetablebs')

#    print datetime.now()
    d = datetime.today() + timedelta(hours=9)

    sqlstr = 'ch,start,end, title from (select ch,start,title,end from tvtimetable.swdata where genre like "%野球%" union select ch,start,title,end from tvtimetablebs.swdata where genre like "%野球%") where end > "' + d.isoformat() + '" order by start'

    a = scraperwiki.sqlite.select(sqlstr)

    html = ""
    paylist = []
    minilist = []
    for row in a:
#        if row['ch'] in chPay:
#            if row['title'].find('[無]') != 1:
#                paylist.append(datestr2week(row['start']) + ' ' + row['ch'] + row['title'])
#                continue
#        if (datestr2date(row['end']) - datestr2date(row['start'])) <= timedelta(minutes=30):
#        print datestr2date(row['start']), datestr2date(row['end']), row['title']
        if (datestr2date(row['end']) - datestr2date(row['start'])) <= timedelta(minutes=30) or (row['ch'].find('J SPORTS') != -1 and row['title'].find('野球好きニュース') != -1):
                diff = datestr2date(row['end']) - datestr2date(row['start'])
                #print diff
                minilist.append(datestr2week(row['start']) + ' ' + str(diff.seconds/60) + '分 ' + row['ch'] + row['title'])
                continue

        ch = unicodedata.normalize('NFKC', row['ch'])


#ch name override
#        if row['ch'] == 'ＮＨＫ総合・東京':
#            ch = row['ch'] = 'ＮＨＫ総合'

        if row['ch'].find('テレ朝チャンネル') == 0:
            ch = row['ch'] = 'テレ朝ch2'

        if row['ch'] == '朝日ニュースターＨＤ':
            ch = row['ch'] = '朝日HD'

        if row['ch'] == 'スカイ・A　sports＋':
            ch = row['ch'] = 'スカイ・A'

        title = row['title']
#        if ch == 'NHK BS1':
#            sqlstr = '* from mlbjpgyao.swdata where ch like "BS1%" and start="' + row['start'] + '"'
#            sqlstr = '* from tvtimetablebs.swdata where genre like "%野球%" and ch="ＮＨＫ ＢＳ１" and start=%s' % (row['start'],)
#            print sqlstr
#            a = scraperwiki.sqlite.select(sqlstr)
#            if a:
#                continue

        if ch == 'NHK BS1' and title.find('ＭＬＢ・アメリカ大リーグ') == 0:
            title = title.replace('ＭＬＢ・アメリカ大リーグ', '')

#program skip 
#        if row['ch'] == 'J SPORTS 3' and title.find('[無][生]野球好きニュース'):
#            continue

        if row['ch'] == 'FOXbs238' and title.find('BASEBALL　CENTER') != -1:
#            minilist.append(datestr2week(row['start']) + ' ' + str((row['end']-row['start'])/60) + '分 ' + row['ch'] + row['title'])
            continue

        if ch == 'NHK BS1' and title.find('ワールドスポーツMLB') != -1:
            continue

        d = datetime.strptime(row['start'], '%Y-%m-%dT%H:%M:%S')
        dstr1 = '%d/%d' % (d.month, d.day)
        dstr2 = '(%s)%02d:%02d' % ( WD[d.weekday()], d.hour, d.minute)
#        dstr = str(d.month) + '月' + str(d.day) + '日('+ WD[d.weekday()] +')'+ str(d.hour) + ':' + str(d.minute)
        html += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (ch, dstr1+dstr2, title)
#        html += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (row['ch'],row['title'],row['start'],row['shosai'])
#        print html

    print """
<html>
<head>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
</head>
<body>
   <style type="text/css">
      <!--
table.data td, table.data th {
    border: 2px solid #FFFFFF;
    line-height: 2em;
    padding: 0.3em 0.5em;
}
        -->
    </style>
<table border>"""
    print html
    print """
</table><br><br><br><br><br><br><br>
"""
    if minilist:
        print '30分以内番組：<br>'
    for i in minilist:
        print i + '<br>'
    if paylist:
        print '有料枠：<br>'
    for i in paylist:
        print i + '<br>'
    print """
</body></html>
"""
output()
