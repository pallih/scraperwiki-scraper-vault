<?php
function scrape($year) {
    $data = scraperwiki::scrape('http://bifr.nic.in/registercases'.$year.'.htm');

    echo "Loading data ($year) ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML($data);
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 3; $i < $n; $i++) {
        $row = $query->item($i);
        if ($a = $row->getElementsByTagName('a')->item(0)) {
            $url = $a->getAttribute('href');
        } else {
            $url = null;
        }
        array_push($results, @$result = array(
            'case_number' => $row->childNodes->item(2)->nodeValue,
            'name_of_company'=> preg_replace('/\xC2\xA0|\r|\n/', '', $row->childNodes->item(4)->nodeValue)
        ));
        //Clean loop variables
        $option = null;
        $result = null;
        unset($option);
        unset($result);
    }

    //Clean up
    $options = null;
    unset($options);

    //Save to database
    scraperwiki::save_sqlite(array('case_number'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

for ($year = 1987; $year <= date('Y'); $year++) {
    scrape($year);
}

?>