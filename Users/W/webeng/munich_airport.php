<?php

# Exercise sheet 8 - Task 12
# www.munich-airport.de

# we extracted information of the arrivales and takeoffs of the munich airport

# we wanted schedule time of 5 minutes but this is not allowed for a standard account (1 day)

require "scraperwiki/simple_html_dom.php";

function grep_munich($url, $table_name){
    $html = scraperWiki::scrape($url);
    $count = 0;
    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);

    //Drop all old informations by dropping the table
    scraperwiki::sqliteexecute("drop table if exists ".$table_name);
    scraperwiki::sqlitecommit();

    $table = $dom->getElementById('flight_info_area');
    foreach($table->find('tr') as $data) 
    {
            
            // Flight details. Read tds or ths
            $tds = $data->find("td");

            //if there are less then 7 columns continue to next loop
            if(sizeof($tds)<7){
                continue;
            }

            //print $data->plaintext . "\n";
        
            $flightnr = $tds[1]->plaintext;
            $from = $tds[2]->plaintext;
            $time = $tds[3]->plaintext;
            $expected_time = $tds[4]->plaintext;
             
            //Create date
            $date = date("Y-m-d");
    
            //Build array of flight informations
            $flight_data = array("date"=>$date,
                                 "count"=>$count,
                                 "flightnr"=>$flightnr,
                                 "from" => $from,
                                 "time"=>$time,
                                 "expected_time"=>$expected_time
                                );

            //Save the informations of one flight
            scraperwiki::save_sqlite(array("date","count"), $flight_data, $table_name);
            $count = $count+1;
    }
}

//grep arrive and save it in table arrive
grep_munich("http://www.munich-airport.de/en/consumer/fluginfo/arr/index.jsp", "arrive");
//grep takeoff and save it in table takeoff
grep_munich("http://www.munich-airport.de/en/consumer/fluginfo/dep/index.jsp", "takeoff");

?>
<?php

# Exercise sheet 8 - Task 12
# www.munich-airport.de

# we extracted information of the arrivales and takeoffs of the munich airport

# we wanted schedule time of 5 minutes but this is not allowed for a standard account (1 day)

require "scraperwiki/simple_html_dom.php";

function grep_munich($url, $table_name){
    $html = scraperWiki::scrape($url);
    $count = 0;
    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);

    //Drop all old informations by dropping the table
    scraperwiki::sqliteexecute("drop table if exists ".$table_name);
    scraperwiki::sqlitecommit();

    $table = $dom->getElementById('flight_info_area');
    foreach($table->find('tr') as $data) 
    {
            
            // Flight details. Read tds or ths
            $tds = $data->find("td");

            //if there are less then 7 columns continue to next loop
            if(sizeof($tds)<7){
                continue;
            }

            //print $data->plaintext . "\n";
        
            $flightnr = $tds[1]->plaintext;
            $from = $tds[2]->plaintext;
            $time = $tds[3]->plaintext;
            $expected_time = $tds[4]->plaintext;
             
            //Create date
            $date = date("Y-m-d");
    
            //Build array of flight informations
            $flight_data = array("date"=>$date,
                                 "count"=>$count,
                                 "flightnr"=>$flightnr,
                                 "from" => $from,
                                 "time"=>$time,
                                 "expected_time"=>$expected_time
                                );

            //Save the informations of one flight
            scraperwiki::save_sqlite(array("date","count"), $flight_data, $table_name);
            $count = $count+1;
    }
}

//grep arrive and save it in table arrive
grep_munich("http://www.munich-airport.de/en/consumer/fluginfo/arr/index.jsp", "arrive");
//grep takeoff and save it in table takeoff
grep_munich("http://www.munich-airport.de/en/consumer/fluginfo/dep/index.jsp", "takeoff");

?>
