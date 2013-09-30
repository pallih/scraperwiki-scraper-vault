<?php
######################################
# NCAA Women's Rankings
######################################
require  'scraperwiki/simple_html_dom.php';
$html = scraperwiki::scrape("http://espn.go.com/womens-college-basketball/rankings");
$dom = new simple_html_dom();
$dom->load($html);
$current = "";
foreach($dom->find('table[class=tablehead] tr[class!=colhead]') as $data) {
    $first = trim($data->children(0)->plaintext);
    $second = "";
    if( intval($first) ) {
        $second = preg_replace("/\([^\)]*\)/","",$data->children(1)->plaintext);
        scraperwiki::save(array("poll","rank"), array("poll" => $current, "rank" => "$first", "team" => trim($second)));
    } else if( preg_match("/AP Top 25/",trim($first)) ) {
        $current = "ap";
    } else if( preg_match("/Coaches Poll/",trim($first)) ) {
        $current = "coach";
    }
}
scraperwiki::sqlitecommit();
?><?php
######################################
# NCAA Women's Rankings
######################################
require  'scraperwiki/simple_html_dom.php';
$html = scraperwiki::scrape("http://espn.go.com/womens-college-basketball/rankings");
$dom = new simple_html_dom();
$dom->load($html);
$current = "";
foreach($dom->find('table[class=tablehead] tr[class!=colhead]') as $data) {
    $first = trim($data->children(0)->plaintext);
    $second = "";
    if( intval($first) ) {
        $second = preg_replace("/\([^\)]*\)/","",$data->children(1)->plaintext);
        scraperwiki::save(array("poll","rank"), array("poll" => $current, "rank" => "$first", "team" => trim($second)));
    } else if( preg_match("/AP Top 25/",trim($first)) ) {
        $current = "ap";
    } else if( preg_match("/Coaches Poll/",trim($first)) ) {
        $current = "coach";
    }
}
scraperwiki::sqlitecommit();
?>