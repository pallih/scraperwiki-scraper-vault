<?php
function scrape($year) {
    echo "Loading data ($year) ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(
        scraperwiki::scrape("")
    );
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//ul/li');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $row = $query->item($i)->getElementsByTagName('span');
        @$result = array(
            'id' => preg_replace('/\s/', '', $year .'-'. $row->item(0)->nodeValue),
            'year' => trim($year),
            'rank' => trim($row->item(0)->nodeValue),
            'company' => trim($row->item(1)->nodeValue),
            'revenue' => trim($row->item(3)->nodeValue),
            'profits' => trim($row->item(4)->nodeValue),
        );
        if (!empty($result['company'])) array_push($results, $result);
        //Clean loop variables
        $option = null;
        $result = null;
        unset($option);
        unset($result);
    }
    
    //Clean up
    $options = null;
    $ch = null;
    unset($options);
    unset($ch);
    scraperwiki::save_sqlite(array('id'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

scrape(2013);
?><?php
function scrape($year) {
    echo "Loading data ($year) ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(
        scraperwiki::scrape("")
    );
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//ul/li');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $row = $query->item($i)->getElementsByTagName('span');
        @$result = array(
            'id' => preg_replace('/\s/', '', $year .'-'. $row->item(0)->nodeValue),
            'year' => trim($year),
            'rank' => trim($row->item(0)->nodeValue),
            'company' => trim($row->item(1)->nodeValue),
            'revenue' => trim($row->item(3)->nodeValue),
            'profits' => trim($row->item(4)->nodeValue),
        );
        if (!empty($result['company'])) array_push($results, $result);
        //Clean loop variables
        $option = null;
        $result = null;
        unset($option);
        unset($result);
    }
    
    //Clean up
    $options = null;
    $ch = null;
    unset($options);
    unset($ch);
    scraperwiki::save_sqlite(array('id'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

scrape(2013);
?>