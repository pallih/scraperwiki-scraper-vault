<?php
// my stuff

//Scraper to extract candidate information for PHP developers
require 'scraperwiki/simple_html_dom.php';

// set page
//$page = "http://www.thomasnet.com/products/trusses-96156054-1.html?WTZO=Find%20Suppliers";
    // Trusses page 2
//$page = "http://www.thomasnet.com/products/trusses-96156054-3.html";   
$page = "http://www.thomasnet.com/products/plastic-pipe-58530403-6.html";
    // Last page of plastic pipe
//$page = "http://www.thomasnet.com/products/plastic-pipe-58530403-72.html";

// scrape page
$html_content = scraperwiki::scrape($page);
$html = str_get_html($html_content);


    // Get number of all results
//$num_of_results = $html->find("div#rsltlbls b", 0);
    // Example:  Displaying 126 to 150 out of 1,792 results
$num_of_results = $html->find("div#rsltlbls", 0);
$total_results = $num_of_results->plaintext;
print $total_results[1] . "\n";

function GetTotalResults( $full_string ) 
{
        // Get length of string
    $string_length = strlen($full_string);
        // Make length negative to traverse backwards first
    //$negative_string_length = $string_length * (-1);
    //echo $negative_string_length . "\n";

        // set char_compare to something to start off
    //$char_compare = $full_string[$negative_string_length];
    $char_compare = 'a';

        // While haven't found 'f' and haven't reached the beginning of the string
    while( $char_compare != 'f' || $string_length < 0 )
    {
            // Traverse backwards to get beginning of number
        $char_compare = $full_string[ $string_length];
        echo "char compare is: " . $char_compare . "\n";
        $string_length--;
        echo $string_length . "\n";

    }
        // Go forward til getting to "1"
    $char_compare = $full_string[ ( 3 + $string_length ) ];
    echo "char compare is: " . $char_compare . "\n";

    return $char_compare;
    
}

$char_at_now = GetTotalResults( $total_results );
echo "char at now is: " . $char_at_now . "\n";
echo "string_length now is: " . $string_length . "\n";


// pull company name
//$company = $html->find("div.modlinks a", 0);
for( $i = 0; $i < 10; $i++ )
{

    ////$company = $html->find("span.coname2 a", $i);
    //$company = $html->find("span.rsltsubtitle", $i);
    $company = $html->find("div.resultdata a", $i);
    print $company . "\n";

    // deal with weird css from their website
    /*
    if( $company == "" || $company == 0 )
    {
        $company = $html->find("span.coname1 a", $i);
    }
    */
    $page_link = html_entity_decode($html->find("div.resultdata a", $i)->href);
    //$page_link = 0;

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
    //$companyresults = "companyresults";

        // Split string to get last 10 digits - the fax number
    $str = $companyresults;

    //$end = strlen($str);
    
    $companyresults = $companyresults->plaintext;

        // last 10 characters are the fax number
    $fax = substr($companyresults, -12); 
    print $fax . "\n"; 
    
    


    //save the data
    //scraperwiki::save_sqlite(array("company", "number"), array("company"=>"Suz", "number"=>2491 ));
   ////scraperwiki::save_sqlite(array("number", "company", "url", "companyresults"), array( "number"=>$i, "company"=>$company->plaintext, "url"=>$aMyResults[$i], "companyresults"=>$companyresults->plaintext ));    scraperwiki
    //scraperwiki::save_var('company_var', $company);    
    //scraperwiki::save_var('incrementor', $i);       
    ////scraperwiki::save_var('url_var' . $i, $url);
    ////scraperwiki::save_var('fax_var' . $i, $fax);
    scraperwiki::save_sqlite(array("Fax"),array("Fax"=>$fax, "Company"=>$company->plaintext, "NumResults"=>$char_at_now, "Increment"=>$i));

    //print scraperwiki::get_var('last_page');
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


