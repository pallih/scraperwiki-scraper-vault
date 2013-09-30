# -*- coding: utf-8 -*-
import scraperwiki
import codecs

ENCODING = 'utf_8'


DATA_LABEL_LIST = ( \
    (u'circle', u'サークル'), \
    (u'vocal', u'歌手名'), \
    (u'album', u'アルバム'), \
    (u'song', u'曲名'), \
    (u'original', u'原作'), \
    (u'original_song', u'原曲名'), \
    (u'request', u'リクエスト番号'), \
    (u'publish', u'配信日'), \
#    (u'movie_link_official', u'公式動画'), \
#    (u'movie_link_karaoke', u'カラオケ'), \
#    (u'movie_link_other', u'他'), \
    )

scraperwiki.sqlite.attach( "touhou_karaoke" )

data = scraperwiki.sqlite.select( '* from touhou_karaoke.swdata order by publish desc, circle asc, album asc, song asc, original asc, original_song asc' )

print '''<html lang="ja">
<head>
    <title>東方カラオケデータベース</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<style type="text/css">
<!--
body {
    font-size: 0.9em;
}
table {
    border-collapse: collapse;
}
td,th {
    font-size: 0.7em;
    border-style: solid;
    border-width: 1px;
    border-color: #5555AA
}
th {
    background-color: #AAAAFF;
}
--> 
</style>
</head>
<body>
<h1>東方カラオケデータベース</h1>
<p>東方カラオケwiki(<a href="http://www32.atwiki.jp/toho_karaoke/" target="_blank">http://www32.atwiki.jp/toho_karaoke/</a>)のスクレイピングデータベースのサンプルです.</p>
<p>動画リンクは省略しています.</p>
<table>'''

print '<tr>'
for (label,name) in DATA_LABEL_LIST:
    print u'<th>{0}</th>'.format( name ).encode( ENCODING )
print '</tr>'

i = 0
for line in data:
    if i % 2:
        c = '#DDDDFF'
    else:
        c = '#FFFFFF'
    print '<tr style="background-color:{0}">'.format( c )
    for (label,name) in DATA_LABEL_LIST:
        print u'<td>{0}</td>'.format( line[label] ).encode( ENCODING )
    print '</tr>'
    i += 1

print '''</table>
</body>
</html>'''# -*- coding: utf-8 -*-
import scraperwiki
import codecs

ENCODING = 'utf_8'


DATA_LABEL_LIST = ( \
    (u'circle', u'サークル'), \
    (u'vocal', u'歌手名'), \
    (u'album', u'アルバム'), \
    (u'song', u'曲名'), \
    (u'original', u'原作'), \
    (u'original_song', u'原曲名'), \
    (u'request', u'リクエスト番号'), \
    (u'publish', u'配信日'), \
#    (u'movie_link_official', u'公式動画'), \
#    (u'movie_link_karaoke', u'カラオケ'), \
#    (u'movie_link_other', u'他'), \
    )

scraperwiki.sqlite.attach( "touhou_karaoke" )

data = scraperwiki.sqlite.select( '* from touhou_karaoke.swdata order by publish desc, circle asc, album asc, song asc, original asc, original_song asc' )

print '''<html lang="ja">
<head>
    <title>東方カラオケデータベース</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<style type="text/css">
<!--
body {
    font-size: 0.9em;
}
table {
    border-collapse: collapse;
}
td,th {
    font-size: 0.7em;
    border-style: solid;
    border-width: 1px;
    border-color: #5555AA
}
th {
    background-color: #AAAAFF;
}
--> 
</style>
</head>
<body>
<h1>東方カラオケデータベース</h1>
<p>東方カラオケwiki(<a href="http://www32.atwiki.jp/toho_karaoke/" target="_blank">http://www32.atwiki.jp/toho_karaoke/</a>)のスクレイピングデータベースのサンプルです.</p>
<p>動画リンクは省略しています.</p>
<table>'''

print '<tr>'
for (label,name) in DATA_LABEL_LIST:
    print u'<th>{0}</th>'.format( name ).encode( ENCODING )
print '</tr>'

i = 0
for line in data:
    if i % 2:
        c = '#DDDDFF'
    else:
        c = '#FFFFFF'
    print '<tr style="background-color:{0}">'.format( c )
    for (label,name) in DATA_LABEL_LIST:
        print u'<td>{0}</td>'.format( line[label] ).encode( ENCODING )
    print '</tr>'
    i += 1

print '''</table>
</body>
</html>'''