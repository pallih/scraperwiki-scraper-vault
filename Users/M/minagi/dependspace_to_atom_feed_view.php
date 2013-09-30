<?php
// DependSpace 2 Atom (View) 
// 
// date3339関数はBoris Korobkovによる(phpマニュアルユーザノートより)

scraperwiki::attach("tmp_dependspace"); 
$item= scraperwiki::select( "* from swdata" );

$lastupdate= scraperwiki::sqliteexecute("select date from swdata where id='0'"); 

// ATOM published
scraperwiki::httpresponseheader("Content-Type", "application/atom+xml");

echo '<?xml version="1.0" encoding="utf-8"?>'.PHP_EOL;
echo '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="ja">'.PHP_EOL;
echo '    <title>DependSpace v.9 メーカーサイト更新情報、発売日情報サイト</title>'.PHP_EOL;
echo '    <subtitle type="text">DependSpace v.9 メーカーサイト更新情報、発売日情報サイト</subtitle>'.PHP_EOL;
echo '    <link rel="alternate" type="text/html" href="http://www.nona.dti.ne.jp/d-space/" />'.PHP_EOL;
echo '    <link rel="self" type="application/atom+xml" href="https://views.scraperwiki.com/run/dependspace_to_atom_feed_view/" />'.PHP_EOL;
echo '    <updated>'. $lastupdate->data[0][0]. '</updated>'.PHP_EOL;
echo '    <id>tag:dependspace.net,'.date("Y").':'.date("m").':'.date("d").'</id>'.PHP_EOL;
echo '    <link rel="start" href="https://views.scraperwiki.com/run/dependspace_to_atom_feed_view/" type="application/rss+xml"/>'.PHP_EOL;

foreach($item as $key => $val) {
    $val['text'] = htmlspecialchars($val['text'], ENT_QUOTES);
    echo '    <entry>'.PHP_EOL;
    echo '        <title>'.$val['text'].'</title>'.PHP_EOL;
    echo '        <link rel="alternate" type="text/html" href="'.$val['href'].'" />'.PHP_EOL;
    echo '        <id>tag:dependppace.net,'.date("Y").':feed/'.$val['id'].'</id>'.PHP_EOL;
    echo '        <published>'.$val['date'].'</published>'.PHP_EOL;
    echo '        <updated>'.$val['date'].'</updated>'.PHP_EOL;
//echo '        <author><name>hoge</name><email>foo@example.net</email></author>'.PHP_L;
    echo '        <summary>'.$val['text'].'</summary>'.PHP_EOL;
    echo '        <content type="html"><![CDATA[<a href="'.$val['href'].'">'.$val['text'].'</a>]]></content>'.PHP_EOL;
    echo '    </entry>'.PHP_EOL;
}
echo '    </feed>'.PHP_EOL;
    
/**
 * Get date in RFC3339
 * For example used in XML/Atom
 *
 * @param integer $timestamp
 * @return string date in RFC3339
 * @author Boris Korobkov
 * @see http://tools.ietf.org/html/rfc3339
 */
function date3339($timestamp=0) {

    if (!$timestamp) {
        $timestamp = time();
    }
    $date = date('Y-m-d\TH:i:s', $timestamp);

    $matches = array();
    if (preg_match('/^([\-+])(\d{2})(\d{2})$/', date('O', $timestamp), $matches)) {
        $date .= $matches[1].$matches[2].':'.$matches[3];
    } else {
        $date .= 'Z';
    }
    return $date;

}
 ?>
<?php
// DependSpace 2 Atom (View) 
// 
// date3339関数はBoris Korobkovによる(phpマニュアルユーザノートより)

scraperwiki::attach("tmp_dependspace"); 
$item= scraperwiki::select( "* from swdata" );

$lastupdate= scraperwiki::sqliteexecute("select date from swdata where id='0'"); 

// ATOM published
scraperwiki::httpresponseheader("Content-Type", "application/atom+xml");

echo '<?xml version="1.0" encoding="utf-8"?>'.PHP_EOL;
echo '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="ja">'.PHP_EOL;
echo '    <title>DependSpace v.9 メーカーサイト更新情報、発売日情報サイト</title>'.PHP_EOL;
echo '    <subtitle type="text">DependSpace v.9 メーカーサイト更新情報、発売日情報サイト</subtitle>'.PHP_EOL;
echo '    <link rel="alternate" type="text/html" href="http://www.nona.dti.ne.jp/d-space/" />'.PHP_EOL;
echo '    <link rel="self" type="application/atom+xml" href="https://views.scraperwiki.com/run/dependspace_to_atom_feed_view/" />'.PHP_EOL;
echo '    <updated>'. $lastupdate->data[0][0]. '</updated>'.PHP_EOL;
echo '    <id>tag:dependspace.net,'.date("Y").':'.date("m").':'.date("d").'</id>'.PHP_EOL;
echo '    <link rel="start" href="https://views.scraperwiki.com/run/dependspace_to_atom_feed_view/" type="application/rss+xml"/>'.PHP_EOL;

foreach($item as $key => $val) {
    $val['text'] = htmlspecialchars($val['text'], ENT_QUOTES);
    echo '    <entry>'.PHP_EOL;
    echo '        <title>'.$val['text'].'</title>'.PHP_EOL;
    echo '        <link rel="alternate" type="text/html" href="'.$val['href'].'" />'.PHP_EOL;
    echo '        <id>tag:dependppace.net,'.date("Y").':feed/'.$val['id'].'</id>'.PHP_EOL;
    echo '        <published>'.$val['date'].'</published>'.PHP_EOL;
    echo '        <updated>'.$val['date'].'</updated>'.PHP_EOL;
//echo '        <author><name>hoge</name><email>foo@example.net</email></author>'.PHP_L;
    echo '        <summary>'.$val['text'].'</summary>'.PHP_EOL;
    echo '        <content type="html"><![CDATA[<a href="'.$val['href'].'">'.$val['text'].'</a>]]></content>'.PHP_EOL;
    echo '    </entry>'.PHP_EOL;
}
echo '    </feed>'.PHP_EOL;
    
/**
 * Get date in RFC3339
 * For example used in XML/Atom
 *
 * @param integer $timestamp
 * @return string date in RFC3339
 * @author Boris Korobkov
 * @see http://tools.ietf.org/html/rfc3339
 */
function date3339($timestamp=0) {

    if (!$timestamp) {
        $timestamp = time();
    }
    $date = date('Y-m-d\TH:i:s', $timestamp);

    $matches = array();
    if (preg_match('/^([\-+])(\d{2})(\d{2})$/', date('O', $timestamp), $matches)) {
        $date .= $matches[1].$matches[2].':'.$matches[3];
    } else {
        $date .= 'Z';
    }
    return $date;

}
 ?>
