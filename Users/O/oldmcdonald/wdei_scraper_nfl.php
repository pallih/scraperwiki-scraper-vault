<?php

require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://sports.yahoo.com/nfl/stats/byteam?group=Defense&cat=Total&conference=NFL&year=season_2012&sort=530&old_category=Total");           
$base_url = 'http://sports.yahoo.com';

$dom = new simple_html_dom();
$dom->load($html);

$firstrow = false;

$teams = array();

foreach($dom->find("table tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==26){
        if(!$firstrow){
            $firstrow = true;
            continue;
        }
        
        $team = cleanText($tds[0]->plaintext);
        $teams[$team] = array();
        
        $teams[$team]['team'] = $team;
        
        $as = $tds[0]->find("a");
        $teams[$team]['link'] =  $base_url . $as[0]->href;
        
        $teams[$team]['points/game'] = cleanText($tds[4]->plaintext);
        $teams[$team]['yards/game'] = cleanText($tds[6]->plaintext);
        
        getDetails($teams[$team]['link'], $team);
    }
}

foreach($teams as $team){
    scraperwiki::save(array('team'), $team);
}

function getDetails($url, $team){
        global $teams;
        $html = scraperWiki::scrape($url);
        $dom = new simple_html_dom();
        $dom->load($html);
        foreach($dom->find("tr.active") as $data){
            $tds = $data->find("td.title a");
            $teams[$team]['nextOpponent'] = $tds[0]->plaintext;
        }
}

function cleanText($text){
    return str_replace('&nbsp;', '', $text);
}
?>
