<?php

// Initialisation
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://etrinex.evok.ch/degresjours/Default.aspx");
$html = str_get_html($html_content);

$dates = array();
$temperatures = array();

foreach ($html->find("table#Table1 tr") as $i => $row) {
    if( $i == 1) { // row of dates (2nd row)
        foreach ($row->find("td") as $j=>$cell) {
            if ($j > 0 && $j < 8) {
                $dates[] = make_date(date_parse_from_format("d-m-Y", $cell->innertext));
                //$dates[] = $cell->innertext;
            }
        }
    }
    if( $i == 7) { // row for Fribourg data (8th row)
        foreach ($row->find("td") as $j => $cell) {
            if ( $j > 0 && $j < 14 && $j % 2 == 1 ) {
                if ( $cell->innertext == "-" ) {
                    $temperatures[] = "";
                } else {
                    $temperatures[] = str_replace(",", ".", $cell->innertext) + 0;
                }
            }
        }
    }
}

//$html->__destruct();

foreach ($dates as $index => $date) {
    scraperwiki::save_sqlite(array("Date"), array("Date" => $date, "Température" => $temperatures[$index]));
}

function make_date($date = array()) {
    if ( $date["year"] ) {
        return DateTime::createFromFormat('Y-m-d', $date["year"] . "-" . $date["month"] . "-" .  $date["day"])->format('Y-m-d');
    }
    return "";
}

// Get href of month buttons
$month_buttons = array();
foreach ($html->find("table#Calendar1 a") as $el) {
    if ($el->plaintext === "&lt;") {
        $prev_month_button = $el->href;
    } else if ($el->plaintext === "&gt;") {
        $next_month_button = $el->href;
    } else {
        $month_buttons[] = $el->href;
    }
}

// Week number
$week_text = explode(" ", $html->find("span#txtNumSemaine", 0)->plaintext);
$week_number = end($week_text) + 0;


print($prev_month_button);
print($next_month_button);
print_r($month_buttons);


?>