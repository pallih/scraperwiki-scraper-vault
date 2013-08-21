<?php

//require 'scraperwiki.php';
require 'scraperwiki/simple_html_dom.php';


$directory_url = "http://www.govsm.com/w/Mayors";

$records = get_sources($directory_url);

foreach ($records as $record) {
    scraperwiki::save(array('city'), $record);
}

//header('Content-type: application/json');
//print json_encode($records);


function get_sources($url) {
    
    
    $html = scraperWiki::scrape($url);

    $dom = new simple_html_dom();
    $dom->load($html);

    $list = $dom->find("table[class=wikitable] tbody", 0);
    $count = 1;
    foreach($list->find("tr") as $row){

        $record = null;
        
        // The > 2 is a cheap hack to get past the two header rows.
        if ($count > 2) {

              $record['first_name'] = trim($row->find("td", 1)->plaintext);
              $record['last_name'] = trim($row->find("td", 2)->plaintext);
              $record['party'] = trim($row->find("td", 3)->plaintext);                
              $record['city'] = trim($row->find("td", 4)->plaintext);                        
              $record['state'] = trim($row->find("td", 5)->plaintext);                        
            
            
               $record['facebook'] = ($row->find("td", 6)->find('a',0)) ? $row->find("td", 6)->find("a", 0)->href : null;    
            $record['twitter'] = ($row->find("td", 7)->find('a',0)) ? $row->find("td", 7)->find('a',0)->href : null;    
            $record['youtube'] = ($row->find("td", 8)->find('a',0)) ? $row->find("td", 8)->find('a',0)->href : null;    
            $record['flickr'] = ($row->find("td", 10)->find('a',0)) ? $row->find("td", 10)->find('a',0)->href : null;                
        
            if ((!empty($record['facebook'])) || (!empty($record['twitter'])) || (!empty($record['youtube'])) || (!empty($record['flickr']))) {
                $records[] = $record;
            }
        }
        
        $count++;
        
    }
    
    return $records;
        
}





?>