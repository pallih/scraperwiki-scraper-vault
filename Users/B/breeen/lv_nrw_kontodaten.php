<?php

# Blank PHP

<?php

require 'scraperwiki/simple_html_dom.php';           
$html_content = scraperwiki::scrape("https://verwaltung.piratenpartei-nrw.de/#user_stats");
$html = str_get_html($html_content);
$member_data = array("kreise", "bezirke", "plz");
$bank_data = array();
$area = ""; // in welcher Tabelle befinden wir uns?

foreach ($html->find("table tr") as $el) {           
    
    $first_value = strip_tags($el->children(0)->innertext);
    $first_value = trim($first_value);

    if(is_object($el->children(1)) === true) {
        $second_value = strip_tags($el->children(1)->innertext);
        $second_value = trim($second_value);
    } else {
        $second_value = "";
    }
    
    if(is_object($el->children(2)) === true) {
        $third_value = strip_tags($el->children(2)->innertext);
        $third_value = str_replace("&nbsp;", "", $third_value);
        $third_value = trim($third_value);
    } else {
        $third_value = "";
    }

    if(is_object($el->children(3)) === true) {
        $fourth_value = strip_tags($el->children(3)->innertext);
        $fourth_value = trim($fourth_value);
    } else {
        $fourth_value = "";    
    }

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
        $area = ""; // Rest unten
    }

    if($area == "" || $area == "k" || $area == "b" || $area == "p") {
        continue;
    }

    /*if($area == "bank") {
        $bank_data[] = array("Datum" => $first_value, "Buchungstext" => $second_value, "Verwendungszweck" => $third_value, "Betrag" => $fourth_value);
        scraperwiki::save_sqlite(array("Datum", "Buchungstext", "Verwendungszweck", "Betrag"), array("Datum" => $first_value, "Buchungstext" => $second_value, "Verwendungszweck" => $third_value, "Betrag" => $fourth_value));     
    } else {*/
        scraperwiki::save_sqlite(array("Bereich", "Ort", "Wert"), array("Bereich" => $area, "Ort" => $first_value, "Wert" => $second_value));     
    //}    
}
?>
