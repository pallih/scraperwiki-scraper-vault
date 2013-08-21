<?php

// Initialisation
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://etrinex.evok.ch/degresjours/Default.aspx");
$html = str_get_html($html_content);

// initialize empty array to store the data array from each row
$tabledata = array();

// loop over rows
foreach($html->find("table#Table1 tr") as $row) {

    // initialize array to store the cell data from each row
    $rowdata = array();
    foreach($row->find('td') as $cell) {

        // change separator and type of temperature value
        // and format date
        $value = str_replace(",", ".", $cell->innertext);
        if ( strpos($value, ".") ) {
            $value += 0;
        } else if ( preg_match("/\d-\d/", $value) ) {
            $value = make_date(date_parse_from_format("d-m-Y", $value));
        }
        // push the cell's text to the array
        $rowdata[] = $value;
        // duplicate cell if colspan present
        if( isset($cell->colspan) ) {
            $rowdata[] = $value;
        }
    }

    // push the row's data array to the 'big' array
    $tabledata[] = $rowdata;
}
$html->__destruct();

// delete unused row 0 and 2
unset($tabledata[0]);
unset($tabledata[2]);
// reindex array
$tabledata = array_values($tabledata);

// keep relevant columns only, namely 0,1,3,5,7,9,11,13
// transpose array
$transposeddata = transpose($tabledata);
// delete even columns
for ( $i=2; $i<17; $i+=2  ) {
    unset($transposeddata[$i]);
}
// delete last column
array_pop($transposeddata);
// reindex array
$transposeddata = array_values($transposeddata);

$header = array_shift($transposeddata);
$header[0] = "Date";

$tabledata = transpose($transposeddata);
$tabledata = array_combine($header, $tabledata);
$transposeddata = transpose($tabledata);

foreach ($transposeddata as $key => $data) {
    scraperwiki::save_sqlite(array("Date"), $data);
}


function make_date($date = array()) {
    if ( $date["year"] ) {
        return DateTime::createFromFormat('Y-m-d', $date["year"] . "-" . $date["month"] . "-" .  $date["day"])->format('Y-m-d');
    }
    return "";
}

function transpose($array) {
    $transposed_array = array();
    if ($array) {
        foreach ($array as $row_key => $row) {
            if (is_array($row) && !empty($row)) { //check to see if there is a second dimension
                foreach ($row as $column_key => $element) {
                    $transposed_array[$column_key][$row_key] = $element;
                }
            } else {
                $transposed_array[0][$row_key] = $row;
            }
        }
    return $transposed_array;
    }
}

// Needed for PHP < 5.5
function array_column(array $input, $columnKey, $indexKey = null) {
    $result = array();

    if (null === $indexKey) {
        if (null === $columnKey) {
            // trigger_error('What are you doing? Use array_values() instead!', E_USER_NOTICE);
            $result = array_values($input);
        }
        else {
            foreach ($input as $row) {
                $result[] = $row[$columnKey];
            }
        }
    }
    else {
        if (null === $columnKey) {
            foreach ($input as $row) {
                $result[$row[$indexKey]] = $row;
            }
        }
        else {
            foreach ($input as $row) {
                $result[$row[$indexKey]] = $row[$columnKey];
            }
        }
    }

    return $result;
}

?>