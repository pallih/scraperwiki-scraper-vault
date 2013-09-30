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
    // Trusses page 2
//$page = "http://www.thomasnet.com/products/trusses-96156054-2.html";   
//$page = "http://www.thomasnet.com/products/plastic-pipe-58530403-1.html";

// scrape page
$html_content = scraperwiki::scrape($page);
$html = str_get_html($html_content);



// pull company name
//$company = $html->find("div.modlinks a", 0);
for( $i = 0; $i < 10; $i++ )
{
    $company = $html->find("span.coname2 a", $i);
    print $company . "\n";
    // deal with weird css from their website
    /*
    if( $company == "" || $company == 0 )
    {
        $company = $html->find("span.coname1 a", $i);
    }
    */
    $page_link = html_entity_decode($html->find("span.coname2 a", $i)->href);

    $domain = "http://www.thomasnet.com";
    $url = $domain . $page_link;



    // get an array of search results to scrape
    $aMyResults[$i] = $url;

    // scrape each result
    // set page
    $page2 = $aMyResults[$i];
    //$page = "http://www.thomasnet.com/products/plastic-pipe-58530403-1.html";
    
    // scrape page
    $html_content2 = scraperwiki::scrape($page2);
    $html2 = str_get_html($html_content2);

    // second td in the table is the company's name
    //$companyresults = $html2->find("div.tnsearchopts", 0);
    //$companyresults = $html2->find("div.tncontent", 0);
        // Phone
    //$companyresults = $html2->find("div#tncontent strong",0);
        // All Phone and Address info - Needs testing
    $companyresults = $html2->find("div#tncontent td",1);
    


    //save the data
    //scraperwiki::save_sqlite(array("company", "number"), array("company"=>"Suz", "number"=>2491 ));
    scraperwiki::save_sqlite(array("number", "company", "url", "companyresults"), array( "number"=>$i, "company"=>$company->plaintext, "url"=>$aMyResults[$i], "companyresults"=>$companyresults->plaintext ));
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
    // Trusses page 2
//$page = "http://www.thomasnet.com/products/trusses-96156054-2.html";   
//$page = "http://www.thomasnet.com/products/plastic-pipe-58530403-1.html";

// scrape page
$html_content = scraperwiki::scrape($page);
$html = str_get_html($html_content);



// pull company name
//$company = $html->find("div.modlinks a", 0);
for( $i = 0; $i < 10; $i++ )
{
    $company = $html->find("span.coname2 a", $i);
    print $company . "\n";
    // deal with weird css from their website
    /*
    if( $company == "" || $company == 0 )
    {
        $company = $html->find("span.coname1 a", $i);
    }
    */
    $page_link = html_entity_decode($html->find("span.coname2 a", $i)->href);

    $domain = "http://www.thomasnet.com";
    $url = $domain . $page_link;



    // get an array of search results to scrape
    $aMyResults[$i] = $url;

    // scrape each result
    // set page
    $page2 = $aMyResults[$i];
    //$page = "http://www.thomasnet.com/products/plastic-pipe-58530403-1.html";
    
    // scrape page
    $html_content2 = scraperwiki::scrape($page2);
    $html2 = str_get_html($html_content2);

    // second td in the table is the company's name
    //$companyresults = $html2->find("div.tnsearchopts", 0);
    //$companyresults = $html2->find("div.tncontent", 0);
        // Phone
    //$companyresults = $html2->find("div#tncontent strong",0);
        // All Phone and Address info - Needs testing
    $companyresults = $html2->find("div#tncontent td",1);
    


    //save the data
    //scraperwiki::save_sqlite(array("company", "number"), array("company"=>"Suz", "number"=>2491 ));
    scraperwiki::save_sqlite(array("number", "company", "url", "companyresults"), array( "number"=>$i, "company"=>$company->plaintext, "url"=>$aMyResults[$i], "companyresults"=>$companyresults->plaintext ));
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

