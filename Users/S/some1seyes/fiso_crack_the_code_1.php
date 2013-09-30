<?php

$html = scraperWiki::scrape('http://crackthecode.fiso.co.uk/CHANGES.XML');
print $html . "\n"; 


require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom(); 
$dom->load($html); 
foreach($dom->find("PLAYER") as $data){ 
    $snapdate = $data->find("SNAPSHOT_DATE"); 
    $name = $data->find("NAME"); 
    $team = $data->find("TEAM");
    $cost = $data->find("NOW_COST");
    $event = $data->find("EVENT_DESC");
    $record = array( 
        'Date' => $snapdate[0]->plaintext, 
        'Name' => $name[0]->plaintext, 
        'Team' => $team[0]->plaintext, 
        'Price' => $cost[0]->plaintext, 
        'Event' => $event[0]->plaintext, 
    ); 
    //print_r($record) . "\n";
    scraperwiki::save(array('Name'), $record);
}
?>
<?php

$html = scraperWiki::scrape('http://crackthecode.fiso.co.uk/CHANGES.XML');
print $html . "\n"; 


require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom(); 
$dom->load($html); 
foreach($dom->find("PLAYER") as $data){ 
    $snapdate = $data->find("SNAPSHOT_DATE"); 
    $name = $data->find("NAME"); 
    $team = $data->find("TEAM");
    $cost = $data->find("NOW_COST");
    $event = $data->find("EVENT_DESC");
    $record = array( 
        'Date' => $snapdate[0]->plaintext, 
        'Name' => $name[0]->plaintext, 
        'Team' => $team[0]->plaintext, 
        'Price' => $cost[0]->plaintext, 
        'Event' => $event[0]->plaintext, 
    ); 
    //print_r($record) . "\n";
    scraperwiki::save(array('Name'), $record);
}
?>
