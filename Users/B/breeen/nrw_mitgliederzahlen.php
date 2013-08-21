<?php

require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("https://verwaltung.piratenpartei-nrw.de/#user_stats");
$html = str_get_html($html_content);
$area = ""; // in welcher Tabelle befinden wir uns?
$count = 1;
$counter_trans = array("1" => "first", "2" => "second", "3" => "third", "4" => "fourth", "5" => "fifth", "6" => "sixth", "7" => "seventh", "8" => "eigth", "9" => "nineth", "10" => "tenth", "11" => "eleventh", "12" => "twelvth");
$date = date("d.m.Y", time());

foreach ($html->find("table tr") as $el) {           
    
    // init
    foreach($counter_trans as $key => $value) {
        $counter = $value . "_value";
        $$counter = "";
    }

    foreach($el->children() as $child) {
        $counter = $counter_trans[$count] . "_value";
        $$counter = $child->innertext;
        $$counter = strip_tags($$counter);
        $$counter = trim($$counter);
        //print $$counter;
        $count++;
    }
    $count = 1;
    
    if($first_value == "Ennepe-Ruhr-Kreis") {
        $area = "kreise";
    } else if($first_value == "Arnsberg") {
        $area = "bezirke";
    } else if($first_value == "32049") {
        $area = "plz";
    } else if($first_value == "Datum") {
        $area = "bank";
    } else if($first_value == "Aktueller Kontostand (LV NRW)") {
        $area = ""; // Rest unten
    } else if($first_value == "Aachen") {
        $area = ""; // Rest 
    } else if($first_value == "Reqierungsbezirk") {
        $area = ""; // Rest unten
    }

    if($area == "" || $area == "k" || $area == "b" || $area == "p" || $area == "bank") {
        continue;
    }

    /*foreach($counter_trans as $key => $value) {
        $counter = $value . "_value";
        print $$counter;
        if($key == "11") {
            print "-" . "\n";
        } else {
            print "-";
        }
    }*/

    if($fourth_value !== "") {
        scraperwiki::save_sqlite(array("Datum","Ort", "Wert"), array("Datum" => $date, "Ort" => $first_value, "Wert" => $second_value));
        scraperwiki::save_sqlite(array("Datum","Ort", "Wert"), array("Datum" => $date, "Ort" => $fourth_value, "Wert" => $fifth_value));
        scraperwiki::save_sqlite(array("Datum","Ort", "Wert"), array("Datum" => $date, "Ort" => $seventh_value, "Wert" => $eigth_value));
        scraperwiki::save_sqlite(array("Datum","Ort", "Wert"), array("Datum" => $date, "Ort" => $tenth_value, "Wert" => $eleventh_value));     
    } else {
        scraperwiki::save_sqlite(array("Datum","Ort", "Wert"), array("Datum" => $date, "Ort" => $first_value, "Wert" => $second_value));
    }
}

?>