<?php
######################################
# NCAA Football Rankings
######################################
require  'scraperwiki/simple_html_dom.php';
scraperwiki::sqliteexecute("DELETE FROM swdata");
$html = scraperwiki::scrape("http://espn.go.com/college-football/rankings");
$dom = new simple_html_dom();
$dom->load($html);
$current = "";
foreach($dom->find('table[class=tablehead] tr[class!=colhead]') as $data) {
    $first = trim($data->children(0)->plaintext);
    $second = "";
    if( intval($first) and strlen($current) > 0 ) {
        $second = preg_replace("/\([^\)]*\)/","",$data->children(1)->plaintext);
        scraperwiki::save_sqlite(array("poll","rank","team"), array("poll" => $current, "rank" => "$first", "team" => trim($second)));
    } else if( preg_match("/BCS Standings/",trim($first)) ) {
        $current = "bcs";
    } else if( preg_match("/AP Top 25/",trim($first)) ) {
        $current = "ap";
    } else if( preg_match("/USA Today Poll/",trim($first)) ) {
        $current = "usa";
    } else {
        $current = "";
    }
}
scraperwiki::sqlitecommit();
?>