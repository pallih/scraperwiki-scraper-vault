<?php
// my stuff

//Scraper to extract candidate information for PHP developers
require 'scraperwiki/simple_html_dom.php';

// set page
    // Insulation page 1
//$page = "http://www.thomasnet.com/products/insulation-40839003-1.html";
    // 10,000
$page = "http://www.thomasnet.com/products/plastic-pipe-58530403-1.html";
//$page = "http://www.thomasnet.com/products/trusses-96156054-1.html";
//$page = "http://www.thomasnet.com/products/trusses-96156054-1.html?WTZO=Find%20Suppliers";
    // Trusses page 2
//$page = "http://www.thomasnet.com/products/trusses-96156054-3.html";   
//$page = "http://www.thomasnet.com/products/plastic-pipe-58530403-6.html";
    // Last page of plastic pipe
//$page = "http://www.thomasnet.com/products/plastic-pipe-58530403-72.html";

// scrape page
$html_content = scraperwiki::scrape($page);
$html = str_get_html($html_content);

global $part1, $part2;


    // Get number of all results
//$num_of_results = $html->find("div#rsltlbls b", 0);
    // Example:  Displaying 126 to 150 out of 1,792 results
$num_of_results = $html->find("div#rsltlbls", 0);
$total_results = $num_of_results->plaintext;
print $total_results[1] . "\n";

function BreakApartUrl( $url )
{
    $string_full_length_url = strlen( $url );
    $string_length_url = strlen( $url );
    $char = 'a';

    while( $char != '-' ||  $string_length_url <= 0 )
    {
        --$string_length_url;
        $char = $url[ $string_length_url ];
    }
    //--$string_length_url;
    echo "URL IS : " . $char . "\n";
    $part1_end = $string_length_url;
    $part1 = substr($url, 0, $part1_end);
    echo "PART1 IS : " . $part1 . "\n";

    
    $char = 'a';
    while( $char != '.' || $string_length_url > $string_full_length_url )
    {
        ++$string_length_url;
        $char = $url[ $string_length_url ];
    }
    echo "URL IS 2 : " . $char . "\n";
    $part2_start = $string_length_url;
    $part2 = substr($url, $part2_start, $string_full_length_url );
    echo "PART2 IS : " . $part2 . "\n";

        // Store results in array
    $url_parts[0] = $part1;
    $url_parts[1] = $part2;
    return $url_parts;
}

function GetTotalResults( $full_string ) 
{
        // Get length of string
    $string_length = strlen($full_string);
        // Make length negative to traverse backwards first
    $negative_string_length = $string_length * (-1);
    echo $negative_string_length . "\n";

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
    $string_length = $string_length + 3;
    $char_compare = $full_string[$string_length];
    echo "char compare is: " . $char_compare . "\n";


        // Get starting point, then ending point
    $starting_point = $string_length;
    echo "CHAR_COMPARE IS: " . $char_compare . "\n";
        // See if a space character with work
    while( $char_compare != ' ')
    {
        echo "CHAR_COMPARE IS: " . $char_compare . "\n";
        $char_compare = $full_string[$string_length];
        echo "char 2 compare is now: " . $char_compare . "\n";
        ++$string_length;
        echo $string_length . "\n";
        
    }
    
            // Now have ending point  
        $ending_point = $string_length;

            // Get just the number
        $results_number = substr($full_string, $starting_point, $ending_point);
        echo "RESULTS NUMBER IS: " . $results_number . "\n";
            // Take out comma
        $results_length = strlen($results_number);
        
        //for( $i = 0; $i < $results_length; $results_number[$i] != ' '; $i++ )
        $i = 0;
        while( $results_number[$i] != ' ' )
        {
            
            if( $results_number[$i] == ',' )
            {
                    // Skip the comma
                ++$i;
            }
            $final_result[$i] = $results_number[$i];
            ++$i;
        } 

        $final_string = implode("", $final_result);
        echo "FINAL RESULT: " . $final_string . "\n";

            // Divide by 25, the number of results per page
        $number_of_pages = ceil( $final_string / 25 );
        echo "PAGE NUMBER: " . $number_of_pages . "\n";

        //  Will need to return the number of results instead
    return $number_of_pages;
    
}



$number_of_pages = GetTotalResults( $total_results );
echo "char at now is: " . $char_at_now . "\n";

$my_url = "http://www.thomasnet.com/products/plastic-pipe-58530403-6.html";
$parts_of_page = BreakApartUrl( $my_url );


// START MAIN LOOP FOR ALL PAGES
for( $j = 1; $j <= $number_of_pages; $j++ )
{
    $page = $parts_of_page[0] . "-" . $j . $parts_of_page[1];
    echo "THE PAGE IS: " . $page . "\n";
        // scrape page
    $html_content = scraperwiki::scrape($page);
    $html = str_get_html($html_content);
    //$html = $html->plaintext;

            // Example:  Displaying 126 to 150 out of 1,792 results
    $num_of_results = $html->find("div#rsltlbls", 0);
    $total_results = $num_of_results->plaintext;

    //------------
    
    // pull company name
    //$company = $html->find("div.modlinks a", 0);
    for( $i = 0; $i < 25; $i++ )
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
        $phone = $html2->find("div#tncontent strong",0);
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
        //scraperwiki::save_sqlite(array("Fax_Number"),array("Phone_Number"=>$phone->plaintext, "Fax_Number"=>$fax, "Company"=>$company->plaintext, "NumResults"=>$char_at_now, "Increment"=>$i));
        scraperwiki::save_sqlite(array("Fax_Number"),array("Fax_Number"=>$fax, "Company"=>$company->plaintext, "NumResults"=>$char_at_now, "Phone_Number"=>$phone->plaintext));
    
        //print scraperwiki::get_var('last_page');
    }
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
    // Insulation page 1
//$page = "http://www.thomasnet.com/products/insulation-40839003-1.html";
    // 10,000
$page = "http://www.thomasnet.com/products/plastic-pipe-58530403-1.html";
//$page = "http://www.thomasnet.com/products/trusses-96156054-1.html";
//$page = "http://www.thomasnet.com/products/trusses-96156054-1.html?WTZO=Find%20Suppliers";
    // Trusses page 2
//$page = "http://www.thomasnet.com/products/trusses-96156054-3.html";   
//$page = "http://www.thomasnet.com/products/plastic-pipe-58530403-6.html";
    // Last page of plastic pipe
//$page = "http://www.thomasnet.com/products/plastic-pipe-58530403-72.html";

// scrape page
$html_content = scraperwiki::scrape($page);
$html = str_get_html($html_content);

global $part1, $part2;


    // Get number of all results
//$num_of_results = $html->find("div#rsltlbls b", 0);
    // Example:  Displaying 126 to 150 out of 1,792 results
$num_of_results = $html->find("div#rsltlbls", 0);
$total_results = $num_of_results->plaintext;
print $total_results[1] . "\n";

function BreakApartUrl( $url )
{
    $string_full_length_url = strlen( $url );
    $string_length_url = strlen( $url );
    $char = 'a';

    while( $char != '-' ||  $string_length_url <= 0 )
    {
        --$string_length_url;
        $char = $url[ $string_length_url ];
    }
    //--$string_length_url;
    echo "URL IS : " . $char . "\n";
    $part1_end = $string_length_url;
    $part1 = substr($url, 0, $part1_end);
    echo "PART1 IS : " . $part1 . "\n";

    
    $char = 'a';
    while( $char != '.' || $string_length_url > $string_full_length_url )
    {
        ++$string_length_url;
        $char = $url[ $string_length_url ];
    }
    echo "URL IS 2 : " . $char . "\n";
    $part2_start = $string_length_url;
    $part2 = substr($url, $part2_start, $string_full_length_url );
    echo "PART2 IS : " . $part2 . "\n";

        // Store results in array
    $url_parts[0] = $part1;
    $url_parts[1] = $part2;
    return $url_parts;
}

function GetTotalResults( $full_string ) 
{
        // Get length of string
    $string_length = strlen($full_string);
        // Make length negative to traverse backwards first
    $negative_string_length = $string_length * (-1);
    echo $negative_string_length . "\n";

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
    $string_length = $string_length + 3;
    $char_compare = $full_string[$string_length];
    echo "char compare is: " . $char_compare . "\n";


        // Get starting point, then ending point
    $starting_point = $string_length;
    echo "CHAR_COMPARE IS: " . $char_compare . "\n";
        // See if a space character with work
    while( $char_compare != ' ')
    {
        echo "CHAR_COMPARE IS: " . $char_compare . "\n";
        $char_compare = $full_string[$string_length];
        echo "char 2 compare is now: " . $char_compare . "\n";
        ++$string_length;
        echo $string_length . "\n";
        
    }
    
            // Now have ending point  
        $ending_point = $string_length;

            // Get just the number
        $results_number = substr($full_string, $starting_point, $ending_point);
        echo "RESULTS NUMBER IS: " . $results_number . "\n";
            // Take out comma
        $results_length = strlen($results_number);
        
        //for( $i = 0; $i < $results_length; $results_number[$i] != ' '; $i++ )
        $i = 0;
        while( $results_number[$i] != ' ' )
        {
            
            if( $results_number[$i] == ',' )
            {
                    // Skip the comma
                ++$i;
            }
            $final_result[$i] = $results_number[$i];
            ++$i;
        } 

        $final_string = implode("", $final_result);
        echo "FINAL RESULT: " . $final_string . "\n";

            // Divide by 25, the number of results per page
        $number_of_pages = ceil( $final_string / 25 );
        echo "PAGE NUMBER: " . $number_of_pages . "\n";

        //  Will need to return the number of results instead
    return $number_of_pages;
    
}



$number_of_pages = GetTotalResults( $total_results );
echo "char at now is: " . $char_at_now . "\n";

$my_url = "http://www.thomasnet.com/products/plastic-pipe-58530403-6.html";
$parts_of_page = BreakApartUrl( $my_url );


// START MAIN LOOP FOR ALL PAGES
for( $j = 1; $j <= $number_of_pages; $j++ )
{
    $page = $parts_of_page[0] . "-" . $j . $parts_of_page[1];
    echo "THE PAGE IS: " . $page . "\n";
        // scrape page
    $html_content = scraperwiki::scrape($page);
    $html = str_get_html($html_content);
    //$html = $html->plaintext;

            // Example:  Displaying 126 to 150 out of 1,792 results
    $num_of_results = $html->find("div#rsltlbls", 0);
    $total_results = $num_of_results->plaintext;

    //------------
    
    // pull company name
    //$company = $html->find("div.modlinks a", 0);
    for( $i = 0; $i < 25; $i++ )
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
        $phone = $html2->find("div#tncontent strong",0);
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
        //scraperwiki::save_sqlite(array("Fax_Number"),array("Phone_Number"=>$phone->plaintext, "Fax_Number"=>$fax, "Company"=>$company->plaintext, "NumResults"=>$char_at_now, "Increment"=>$i));
        scraperwiki::save_sqlite(array("Fax_Number"),array("Fax_Number"=>$fax, "Company"=>$company->plaintext, "NumResults"=>$char_at_now, "Phone_Number"=>$phone->plaintext));
    
        //print scraperwiki::get_var('last_page');
    }
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

