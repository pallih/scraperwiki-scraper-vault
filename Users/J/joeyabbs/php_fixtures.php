<?php
require "scraperwiki/simple_html_dom.php";

$html = file_get_html("http://www.sportsmanager.ie/t7.php?userid=&report=1&reporttype=results&sportid=1&countyid=4&contentcountyid=4&contentsportid=1&lastweek=1");
$fields = array("home","scorehome","scoreaway","away","venue","comment","other");
$results = array();

foreach($html->find("tr.reportrow") as $row) {
    $index = 0;
    $comp_cell = $row->prev_sibling()->prev_sibling()->first_child();
    if ( "reportrow_competition_name_small" === $comp_cell->getAttribute("class") ) {
        if ($sub_results) {
            $results[] = $sub_results;
        }
        $sub_results = array();
        $sub_results["title"] = $comp_cell->plaintext;
        $sub_results["results"] = array();
    }
    $result = array();
    foreach($row->children() as $element) {
        $result[$fields[$index++]] = $element->plaintext;
    }
    $sub_results["results"][] = $result;
    scraperwiki::save(array('match_results'),$result);
}

if ($sub_results) {
    $results[] = $sub_results;
}

//scraperwiki::save_sqlite(array('table_cell'), array('table_cell' => $results));
//scraperwiki::save(array('table_cell'), $results);


$callback = $_GET['callback'];
if ($callback) {
    header("Content-Type: text/javascript; charset=utf8");
    echo $callback . "(" . json_encode($results) . ");";
} else {
    header("Content-type: application/json");
    echo json_encode($results);
}
<?php
require "scraperwiki/simple_html_dom.php";

$html = file_get_html("http://www.sportsmanager.ie/t7.php?userid=&report=1&reporttype=results&sportid=1&countyid=4&contentcountyid=4&contentsportid=1&lastweek=1");
$fields = array("home","scorehome","scoreaway","away","venue","comment","other");
$results = array();

foreach($html->find("tr.reportrow") as $row) {
    $index = 0;
    $comp_cell = $row->prev_sibling()->prev_sibling()->first_child();
    if ( "reportrow_competition_name_small" === $comp_cell->getAttribute("class") ) {
        if ($sub_results) {
            $results[] = $sub_results;
        }
        $sub_results = array();
        $sub_results["title"] = $comp_cell->plaintext;
        $sub_results["results"] = array();
    }
    $result = array();
    foreach($row->children() as $element) {
        $result[$fields[$index++]] = $element->plaintext;
    }
    $sub_results["results"][] = $result;
    scraperwiki::save(array('match_results'),$result);
}

if ($sub_results) {
    $results[] = $sub_results;
}

//scraperwiki::save_sqlite(array('table_cell'), array('table_cell' => $results));
//scraperwiki::save(array('table_cell'), $results);


$callback = $_GET['callback'];
if ($callback) {
    header("Content-Type: text/javascript; charset=utf8");
    echo $callback . "(" . json_encode($results) . ");";
} else {
    header("Content-type: application/json");
    echo json_encode($results);
}
