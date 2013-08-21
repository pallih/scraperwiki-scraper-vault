<?php

$html = scraperWiki::scrape("http://www.wheresthematch.com/channels/SKY-Sports.asp?showdatestart=&showdateend=&sportid=4");           
// print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

// for each line of html find td
foreach($dom->find("td[class=fixture-details]") as $data){

      //  print $data;
    $teams = $data->find("a");
    if($teams){

// $record is a new array to store the values found
        $record = array(
            'teams' => $teams[0]->plaintext, 
        );
// output json 
        print json_encode($record) . "\n";
        scraperwiki::save(array('teams'), $record);   
    }
}



?>
<?php

$html = scraperWiki::scrape("http://www.wheresthematch.com/channels/SKY-Sports.asp?showdatestart=&showdateend=&sportid=4");           
// print $html . "\n";

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);

// for each line of html find td
foreach($dom->find("td[class=fixture-details]") as $data){

      //  print $data;
    $teams = $data->find("a");
    if($teams){

// $record is a new array to store the values found
        $record = array(
            'teams' => $teams[0]->plaintext, 
        );
// output json 
        print json_encode($record) . "\n";
        scraperwiki::save(array('teams'), $record);   
    }
}



?>
