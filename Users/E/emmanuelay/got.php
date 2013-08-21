<?php

# Scraper for retrieving arrivals/departures from Swedish airport Landvetter
# Work in progress
# http://swedavia.se/sv/Goteborg/Resenar/Ankomster-inrikes/ <-- ankomster
# http://swedavia.se/got_inr_AnkAvg


require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$html = scraperwiki::scrape("http://swedavia.se/sv/Goteborg/Resenar/Ankomster-inrikes/");
$dom->load($html);
$grid = $dom->find('#FlightGrid',0); 
$listItem = $grid->find("tr");

$rowCount = 0;
$columns = array();
$data = array();

foreach($listItem as $row) {

    if ($rowCount == 0) {
         // Header
        $rows = $row->find("th");
        $rowData = "";
        $colCount=0;
        foreach($rows as $cell) {
            $rowData = $rowData . $cell->plaintext . ", ";
            array_push($columns, fix_chars($cell->plaintext));
            $data[$colCount] = array();
            $colCount++;
        }

    } else {
        $rows = $row->find("td");
        $rowData = "";
        $colCount = 0;
        $rowResult = array();
        foreach($rows as $cell) {
            $rowData = $rowData . $cell->plaintext . ", ";
            array_push($data[$colCount], fix_chars($cell->plaintext));
            $colCount++;
        }
    }
    $rowCount++;
}

$colCount = 0;
$rowCount = 0;
$currentDate = date('Y-m-d');

foreach($data[0] as $row) {

    $cols = array();

    $colCount = 0;
    foreach($columns as $col) {
        array_push($cols, "aa");
        $colCount++;
    }

    if ($data[0][$rowCount] != "&nbsp;") { // If first column is empty, then this might be a grouping indicator (date)

        $dataset = array(
            'Datum' => $currentDate,
            ''.$columns[0].'' => html_entity_decode($data[0][$rowCount]),
            ''.$columns[1].'' => html_entity_decode($data[1][$rowCount]),
            ''.$columns[2].'' => html_entity_decode($data[2][$rowCount]),
            ''.$columns[3].'' => html_entity_decode($data[3][$rowCount]),
            ''.$columns[4].'' => html_entity_decode($data[4][$rowCount])
        );    
        
        scraperwiki::save( array('Tid', 'Datum'), $dataset );
    } else {
        if (is_date($data[1][$rowCount])) {
            $currentDate = $data[1][$rowCount];
        }
    }
    $rowCount++;
}

function fix_chars( $str ) {
    $str = str_replace("Ã¥", "å", $str);
    $str = str_replace("Ã¤", "ä", $str);
    $str = str_replace("Ã", "Ö", $str);

    return $str;
}

function is_date( $str ) 
{ 
  $stamp = strtotime( $str ); 
  
  if (!is_numeric($stamp)) 
  { 
     return FALSE; 
  } 
  $month = date( 'm', $stamp ); 
  $day   = date( 'd', $stamp ); 
  $year  = date( 'Y', $stamp ); 
  
  if (checkdate($month, $day, $year)) 
  { 
     return TRUE; 
  } 
  
  return FALSE; 
} 

?>
