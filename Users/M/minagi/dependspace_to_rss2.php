<?php
// DependSpace 2 Atom (View) 
// 
// date3339関数はBoris Korobkovによる(phpマニュアルユーザノートより)
date_default_timezone_set('Asia/Tokyo');

scraperwiki::attach("tmp_dependspace"); 
$item= scraperwiki::select( "* from swdata" );

$lastupdate = scraperwiki::sqliteexecute("select date from swdata where id='0'"); 
$lastupdate = date("r", strtotime($lastupdate->data[0][0]));

// RSS2.0 published
scraperwiki::httpresponseheader("Content-Type", "application/rss+xml");

echo '<?xml version="1.0" encoding="utf-8"?>'.PHP_EOL;
echo '<rss version="2.0">'.PHP_EOL;
echo '<channel>'.PHP_EOL;

echo '<title>DependSpace v.9 メーカーサイト更新情報、発売日情報サイト</title>'.PHP_EOL;
echo '<description>DependSpace v.9 メーカーサイト更新情報、発売日情報サイト</description>'.PHP_EOL;
echo '<link>http://www.nona.dti.ne.jp/d-space/</link>'.PHP_EOL;
echo '<language>ja</language>'.PHP_EOL;
echo '<pubDate>'.$lastupdate.'</pubDate>'.PHP_EOL;
echo '<lastBuildDate>'.$lastupdate.'</lastBuildDate>'.PHP_EOL;
//echo '<managingEditor>nono@example.com</managingEditor>'.PHP_EOL;

foreach($item as $key => $val) {
    $val['text'] = htmlspecialchars($val['text'], ENT_QUOTES);

    echo '<item>'.PHP_EOL;
    echo '    <title>'.$val['text'].'</title>'.PHP_EOL;
    echo '    <link>'.$val['href'].'</link>'.PHP_EOL;
//    echo '    <guid isPermaLink="true">'.$val['href'].'</guid>'.PHP_EOL;
    echo '    <pubDate>'.date("r", strtotime($val['date'])).'</pubDate>'.PHP_EOL;
    echo '    <description><![CDATA['.$val['text'].']]></description>'.PHP_EOL;
    echo '</item>'.PHP_EOL;
}
echo '</channel>'.PHP_EOL;
echo '</rss>'.PHP_EOL;
exit;<?php
// DependSpace 2 Atom (View) 
// 
// date3339関数はBoris Korobkovによる(phpマニュアルユーザノートより)
date_default_timezone_set('Asia/Tokyo');

scraperwiki::attach("tmp_dependspace"); 
$item= scraperwiki::select( "* from swdata" );

$lastupdate = scraperwiki::sqliteexecute("select date from swdata where id='0'"); 
$lastupdate = date("r", strtotime($lastupdate->data[0][0]));

// RSS2.0 published
scraperwiki::httpresponseheader("Content-Type", "application/rss+xml");

echo '<?xml version="1.0" encoding="utf-8"?>'.PHP_EOL;
echo '<rss version="2.0">'.PHP_EOL;
echo '<channel>'.PHP_EOL;

echo '<title>DependSpace v.9 メーカーサイト更新情報、発売日情報サイト</title>'.PHP_EOL;
echo '<description>DependSpace v.9 メーカーサイト更新情報、発売日情報サイト</description>'.PHP_EOL;
echo '<link>http://www.nona.dti.ne.jp/d-space/</link>'.PHP_EOL;
echo '<language>ja</language>'.PHP_EOL;
echo '<pubDate>'.$lastupdate.'</pubDate>'.PHP_EOL;
echo '<lastBuildDate>'.$lastupdate.'</lastBuildDate>'.PHP_EOL;
//echo '<managingEditor>nono@example.com</managingEditor>'.PHP_EOL;

foreach($item as $key => $val) {
    $val['text'] = htmlspecialchars($val['text'], ENT_QUOTES);

    echo '<item>'.PHP_EOL;
    echo '    <title>'.$val['text'].'</title>'.PHP_EOL;
    echo '    <link>'.$val['href'].'</link>'.PHP_EOL;
//    echo '    <guid isPermaLink="true">'.$val['href'].'</guid>'.PHP_EOL;
    echo '    <pubDate>'.date("r", strtotime($val['date'])).'</pubDate>'.PHP_EOL;
    echo '    <description><![CDATA['.$val['text'].']]></description>'.PHP_EOL;
    echo '</item>'.PHP_EOL;
}
echo '</channel>'.PHP_EOL;
echo '</rss>'.PHP_EOL;
exit;