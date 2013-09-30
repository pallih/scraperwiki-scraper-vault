<?php
/*

//Scraper to extract candidate information for PHP developers

require 'scraperwiki/simple_html_dom.php';

$country = array("uk");
//$topic = array("PHP","symphony","technology","big-data","cloud","innovation");

for ($c = 0; $c < (count($country)); $c++) {

    //for ($t = 0; $t < (count($topic)); $t++) {
    for ($t = 0; $t < 1; $t++) {
       // $page = "http://lanyrd.com/topics/".$topic[$t]."/in/".$country[$c];
        $page = "http://www.thomasnet.com/products/trusses-96156054-1.html?WTZO=Find%20Suppliers";
        $html_content = scraperwiki::scrape($page);
        $html = str_get_html($html_content);
        // $eventscount = count($html->find("li.conference"));
        $eventscount = count($html->find("li.rsltlbls"));
        
        for ($i = 0; $i < $eventscount; $i++) {
            
            $event = $html->find("li.conference h4", $i);
            $location = $html->find("p.location", $i);
            $date = $html->find("p.date", $i);
            $url = html_entity_decode($html->find("h4 a", $i)->href);
            $company = $html->find("td.coname1", $i);

        //save the data

            scraperwiki::save_sqlite(array("event"),array("event"=>$event->plaintext, "location"=>$location->plaintext, "date"=>$date->plaintext,"company"=>$company->plaintext, "url"=>"http://lanyrd.com".$url, "topic"=>$topic[$t], "country"=>$country[$c]));
            

        }

    }

}
*/
?>





<?php
// my stuff

//Scraper to extract candidate information for PHP developers
require 'scraperwiki/simple_html_dom.php';

// set page
$page = "http://www.thomasnet.com/products/trusses-96156054-1.html?WTZO=Find%20Suppliers";

// scrape page
$html_content = scraperwiki::scrape($page);
$html = str_get_html($html_content);



// pull company name
//$company = $html->find("div.modlinks a", 0);
for( $i = 0; $i < 25; $i++ )
{
    $company = $html->find("span.coname2 a", $i);
    //save the data
    //scraperwiki::save_sqlite(array("company", "number"), array("company"=>"Suz", "number"=>2491 ));
    scraperwiki::save_sqlite(array("company", "number"), array("company"=>$company->plaintext, "number"=>9710 ));
}

/*
// pull company name
//$company = $html->find("div.modlinks a", 0);
for ($i = 0; $i < 25; $i++) 
{
    //$company = $html->find("span.coname1 a", $i);
    //$url = $html->find("span.coname1 a", $i);
    //$url =     $html->find("a.primary", $i);
    //$url = html_entity_decode($html->find("a.primary", $i)->href);
    //$url =     "test";

    //save the data
    scraperwiki::save_sqlite(array("company", "number"), array("company" => "Suz", "number" => 2491 ));
    //scraperwiki::save_sqlite(array("company", "number"), array("company" => $company->plaintext, "number" => $url ));
}
scraperwiki::save_sqlite(array("company", "number"), array("company" => "Suz", "number" => 2491 ));
*/

?>

<?php
/*

//Scraper to extract candidate information for PHP developers

require 'scraperwiki/simple_html_dom.php';

$country = array("uk");
//$topic = array("PHP","symphony","technology","big-data","cloud","innovation");

for ($c = 0; $c < (count($country)); $c++) {

    //for ($t = 0; $t < (count($topic)); $t++) {
    for ($t = 0; $t < 1; $t++) {
       // $page = "http://lanyrd.com/topics/".$topic[$t]."/in/".$country[$c];
        $page = "http://www.thomasnet.com/products/trusses-96156054-1.html?WTZO=Find%20Suppliers";
        $html_content = scraperwiki::scrape($page);
        $html = str_get_html($html_content);
        // $eventscount = count($html->find("li.conference"));
        $eventscount = count($html->find("li.rsltlbls"));
        
        for ($i = 0; $i < $eventscount; $i++) {
            
            $event = $html->find("li.conference h4", $i);
            $location = $html->find("p.location", $i);
            $date = $html->find("p.date", $i);
            $url = html_entity_decode($html->find("h4 a", $i)->href);
            $company = $html->find("td.coname1", $i);

        //save the data

            scraperwiki::save_sqlite(array("event"),array("event"=>$event->plaintext, "location"=>$location->plaintext, "date"=>$date->plaintext,"company"=>$company->plaintext, "url"=>"http://lanyrd.com".$url, "topic"=>$topic[$t], "country"=>$country[$c]));
            

        }

    }

}
*/
?>





<?php
// my stuff

//Scraper to extract candidate information for PHP developers
require 'scraperwiki/simple_html_dom.php';

// set page
$page = "http://www.thomasnet.com/products/trusses-96156054-1.html?WTZO=Find%20Suppliers";

// scrape page
$html_content = scraperwiki::scrape($page);
$html = str_get_html($html_content);



// pull company name
//$company = $html->find("div.modlinks a", 0);
for( $i = 0; $i < 25; $i++ )
{
    $company = $html->find("span.coname2 a", $i);
    //save the data
    //scraperwiki::save_sqlite(array("company", "number"), array("company"=>"Suz", "number"=>2491 ));
    scraperwiki::save_sqlite(array("company", "number"), array("company"=>$company->plaintext, "number"=>9710 ));
}

/*
// pull company name
//$company = $html->find("div.modlinks a", 0);
for ($i = 0; $i < 25; $i++) 
{
    //$company = $html->find("span.coname1 a", $i);
    //$url = $html->find("span.coname1 a", $i);
    //$url =     $html->find("a.primary", $i);
    //$url = html_entity_decode($html->find("a.primary", $i)->href);
    //$url =     "test";

    //save the data
    scraperwiki::save_sqlite(array("company", "number"), array("company" => "Suz", "number" => 2491 ));
    //scraperwiki::save_sqlite(array("company", "number"), array("company" => $company->plaintext, "number" => $url ));
}
scraperwiki::save_sqlite(array("company", "number"), array("company" => "Suz", "number" => 2491 ));
*/

?>

