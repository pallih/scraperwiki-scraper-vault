<?php
// Load the C.P.E. Events page
$html =  scraperWiki::scrape("http://k9cpe.com/events.htm");             
require 'scraperwiki/simple_html_dom.php';            
$dom = new simple_html_dom(); 
$dom->load($html);

// Each row is an event
foreach($dom->find("tr") as $data)
{ 
    $events = $data->find("td"); 
        if(count($events)==5)
        { 
            $record = array( 'dates' => $events[0]->plaintext, 
                             'state' => $events[1]->plaintext, 
                             'city' => $events[2]->plaintext,
                             'club' => $events[3]->plaintext,
                             'more'=> $events[4]->plaintext
                           ); 
            scraperwiki::save(array('more'), $record);  
        } 
}
?>
<?php
// Load the C.P.E. Events page
$html =  scraperWiki::scrape("http://k9cpe.com/events.htm");             
require 'scraperwiki/simple_html_dom.php';            
$dom = new simple_html_dom(); 
$dom->load($html);

// Each row is an event
foreach($dom->find("tr") as $data)
{ 
    $events = $data->find("td"); 
        if(count($events)==5)
        { 
            $record = array( 'dates' => $events[0]->plaintext, 
                             'state' => $events[1]->plaintext, 
                             'city' => $events[2]->plaintext,
                             'club' => $events[3]->plaintext,
                             'more'=> $events[4]->plaintext
                           ); 
            scraperwiki::save(array('more'), $record);  
        } 
}
?>
