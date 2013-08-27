<?php

require 'scraperwiki/simple_html_dom.php';

//Get list of clans formatted to tartanweb database
$names = array();

$data = fopen('http://www.letteringdelights.com/dallan_tools/tartanweb_clans.csv', 'r');

$i = 0;
while (($line = fgetcsv($data, 1000,':')) !== FALSE) {
    ++$i;
    if($i % 2 == 0) array_push($names , str_replace(' ' , '_' , strtolower(trim($line[1]))));
}
    
fclose($data);

$clanData = array();

foreach($names as $name) {

    //Clan scrape src
    $html = scraperWiki::scrape('http://scotclans.com/scottish_clans/clans/' . $name . '/history.html'); 
            
    //Load src
    $dom = new simple_html_dom();
    $dom->load($html);
    
    //Scrape from top table
    $topData = $dom->find('#clan_topdetails' , 0);

    if(count($topData) > 0) {
        
        $clan['Image'] = $topData->find('img' , 0)->src;
        
        $rows = $topData->find('tr');
        
        $firstRow = array_shift($rows);
        if(is_object($firstRow) && $firstRow->plaintext) $clan['Name'] = $firstRow->plaintext;
        
        //Get top elements and values
        foreach($rows as $row) {
            $data = $row->find('td');
            if(count($data == 2) && is_object($data[0]) && is_object($data[1]) && $data[0]->plaintext && $data[1]->plaintext) 
                $clan[str_replace(':' , '' , $data[0]->plaintext)] = $data[1]->plaintext;
        }

        //Get history
        $history = '';
        $body = $dom->find('#content_home' , 0);
        $clan['History'] = $body->innertext;
    }
    
    scraperwiki::save($clan , $clan);
}





?><?php

require 'scraperwiki/simple_html_dom.php';

//Get list of clans formatted to tartanweb database
$names = array();

$data = fopen('http://www.letteringdelights.com/dallan_tools/tartanweb_clans.csv', 'r');

$i = 0;
while (($line = fgetcsv($data, 1000,':')) !== FALSE) {
    ++$i;
    if($i % 2 == 0) array_push($names , str_replace(' ' , '_' , strtolower(trim($line[1]))));
}
    
fclose($data);

$clanData = array();

foreach($names as $name) {

    //Clan scrape src
    $html = scraperWiki::scrape('http://scotclans.com/scottish_clans/clans/' . $name . '/history.html'); 
            
    //Load src
    $dom = new simple_html_dom();
    $dom->load($html);
    
    //Scrape from top table
    $topData = $dom->find('#clan_topdetails' , 0);

    if(count($topData) > 0) {
        
        $clan['Image'] = $topData->find('img' , 0)->src;
        
        $rows = $topData->find('tr');
        
        $firstRow = array_shift($rows);
        if(is_object($firstRow) && $firstRow->plaintext) $clan['Name'] = $firstRow->plaintext;
        
        //Get top elements and values
        foreach($rows as $row) {
            $data = $row->find('td');
            if(count($data == 2) && is_object($data[0]) && is_object($data[1]) && $data[0]->plaintext && $data[1]->plaintext) 
                $clan[str_replace(':' , '' , $data[0]->plaintext)] = $data[1]->plaintext;
        }

        //Get history
        $history = '';
        $body = $dom->find('#content_home' , 0);
        $clan['History'] = $body->innertext;
    }
    
    scraperwiki::save($clan , $clan);
}





?>