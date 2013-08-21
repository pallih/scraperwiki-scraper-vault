<?php

require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("http://news.bbc.co.uk/sport1/hi/tennis/results/default.stm");
$html = str_get_html($html_content);

scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `wimbledon_2012_data` (`winner` text, `looser` text, `round` text)");

$winner = $looser = $round = null;

$rounds = $html->find("div.datasection h3");

foreach ($rounds as $roundHeader) {
    $round = $roundHeader->innertext;
    $matches = $roundHeader->nextSibling()->find("tr");
    
    foreach ($matches as $match) {
        $row = str_get_html($match);
        $col = $row->find("td");
        if (count($col) == 0) 
            continue;
    
        $winner = $col[0]->innertext;
        $looser = $col[4]->innertext;

        if (!$winner || !$looser)
            continue;
    
        $data = array(
            'winner' => $winner,
            'looser' => $looser,
            'round' => $round
        );    
    
        scraperwiki::save_sqlite(array('winner', 'looser', 'round'), $data, "wimbledon_2012_data", 2);
    }
}