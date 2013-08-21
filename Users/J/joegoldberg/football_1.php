<?php

require 'scraperwiki/simple_html_dom.php';

scraperwiki::sqliteexecute("CREATE TABLE if not exists Football (gameID TEXT)");

    $html = scraperWiki::scrape("http://www.pro-football-reference.com/years/2012/games.htm");
    $dom = new simple_html_dom();
    $dom->load($html);

    $records = array();

    $table = $dom ->find('table',0);
    $trs = $table->find('tr');

    foreach($trs as $tr){
        
        $td = $tr->find('td', 3);
        $gameID = substr($td,40,-19);
        echo "{$td}\n";

scraperwiki::sqliteexecute("INSERT INTO Football (gameID) VALUES ('".$gameID."')");
            
scraperwiki::sqlitecommit();

}
?>
