<?php

# Exercise sheet 8 - Task 12
# www.munich-airport.de

# we extracted information of the arivales of the munich airport

# we wanted schedule time of 5 minutes but this is not alowed for standard acount (1 day)


require "scraperwiki/simple_html_dom.php";

$html = scraperWiki::scrape("http://www.munich-airport.de/de/consumer/index.jsp");

# Use the PHP Simple HTML DOM Parser to extract <td> tags
$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->getElementById('navigation_mainpage_flightinfo_table');
foreach($table->find('tr') as $data) 
{
   print $data->plaintext . "\n";

// Flight details. Read tds or ths
        $tds = sizeof($data->find("td"))>1?$data->find("td"):$data->find("th");

        if(sizeof($tds)==0){
            break;
        }
        
        $flightnr = $tds[1]->plaintext;
        $from = $tds[2]->plaintext;
        $time = $tds[3]->plaintext;
        $expected_time = $tds[4]->plaintext;
        
        // Skip header
        if($flightnr == "Flug") {
            continue;
        }
      
        //Create date
        $date = date("m.d.y");
    
        //Build array of flight informations
        $flight_data = array("date"=>$date,
                             "flightnr"=>$flightnr,
                             "from" => $from,
                             "time"=>$time,
                             "expected_time"=>$expected_time
                            );
    
        //Save the informations of one flight
        scraperWiki::save_sqlite(array("date","flightnr"), $flight_data);
}

?>
