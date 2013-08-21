<?php

require 'scraperwiki/simple_html_dom.php';

scraperwiki::sqliteexecute("CREATE TABLE if not exists Football (gameID, winner_Pts, loser_Pts, winner_Yds, loser_Yds, winner_Turnovers, loser_Turnovers)");

    $html = scraperWiki::scrape("http://www.pro-football-reference.com/years/2012/games.htm");
    $dom = new simple_html_dom();
    $dom->load($html);

    $records = array();

    $table = $dom ->find('table',0);
    $trs = $table->find('tr');

    foreach($trs as $tr){
        
        $td = $tr->find('td', 3);
        $gameID = substr($td,40,-19)->plaintext;   
        $winner_Pts = $tr->find('td',7)->plaintext;
        $loser_Pts = $tr->find('td',8)->plaintext;
        $winner_Yds = $tr->find('td',9)->plaintext;
        $loser_Yds = $tr->find('td',11)->plaintext;
        $winner_Turnovers = $tr->find('td',10)->plaintext;
        $loser_Turnovers = $tr->find('td',12)->plaintext;

scraperwiki::sqliteexecute("INSERT INTO Football (gameID, winner_Pts, loser_Pts, winner_Yds, loser_Yds, winner_Turnovers, loser_Turnovers, winner_PenaltyYds, Loser_PenaltyYds) VALUES ('".$gameID."','".$Winner_Pts."','".$Loser_Pts."','".$Winner_Yds."','".$Loser_Yds."','".$Winner_Turnovers."','".$Loser_Turnovers."')");
            
scraperwiki::sqlitecommit();

}
?>
