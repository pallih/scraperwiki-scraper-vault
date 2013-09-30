<?php
function scrape($year, $case_type) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://jhr.nic.in/case_status/resp_output.php',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POSTFIELDS => http_build_query(array(
            'year'  => $year,
            'case_type' => $case_type
        )),
        CURLOPT_CONNECTTIMEOUT => 0,
        CURLOPT_TIMEOUT => 1000,
    ));

    echo "Loading data (year: $year; case type: $case_type) ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(curl_exec($ch));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 1; $i < $n; $i++) {
        $row = $query->item($i);
        if ($row->getElementsByTagName('a')->item(0)) {
            $path = $row->getElementsByTagName('a')->item(0)->getAttribute('href');
        }
        @$result = array(
            'case_number' => trim($row->getElementsByTagName('a')->item(0)->nodeValue),
            'path' => trim($path),
            'petitioner' => trim(preg_replace('/\xC2\x8E/', '', $row->childNodes->item(2)->nodeValue)),
            'respondent' => trim(preg_replace('/\xC2\x8E/', '', $row->childNodes->item(4)->nodeValue)),
            'judgment_year' =>  $year,
            'filing_number' => trim($row->childNodes->item(0)->nodeValue)
        );
        if ($result['filing_number']) array_push($results, $result);
        //Clean loop variables
        $option = null;
        $result = null;
        unset($option);
        unset($result);
        if ($i % 100 === 0) {
            scraperwiki::save_sqlite(array('path'), $results);
            $results = array();
        }
    }
    
    //Clean up
    $query = null;
    $xpath = null;
    $ch = null;
    unset($query);
    unset($xpath);
    unset($ch);

    //Final save to database
    scraperwiki::save_sqlite(array('path'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

$case_types = array(67,57,65,66,62,61,55,12,11,8,63,58,20,37,34,42,21,39,35,5,24,27,54,6,29,7,64,53,52,16,51,15,28,14,1,25,31,3,19,33,2,10,23,32,60,56,74,36,40,68,9,26,43,73,4,22,17,50);
for ($year = date('Y'); $year < (date('Y')+1); $year++) {
    foreach ($case_types as $case_type) {
        scrape($year, $case_type);
    }
}
?><?php
function scrape($year, $case_type) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://jhr.nic.in/case_status/resp_output.php',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POSTFIELDS => http_build_query(array(
            'year'  => $year,
            'case_type' => $case_type
        )),
        CURLOPT_CONNECTTIMEOUT => 0,
        CURLOPT_TIMEOUT => 1000,
    ));

    echo "Loading data (year: $year; case type: $case_type) ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(curl_exec($ch));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 1; $i < $n; $i++) {
        $row = $query->item($i);
        if ($row->getElementsByTagName('a')->item(0)) {
            $path = $row->getElementsByTagName('a')->item(0)->getAttribute('href');
        }
        @$result = array(
            'case_number' => trim($row->getElementsByTagName('a')->item(0)->nodeValue),
            'path' => trim($path),
            'petitioner' => trim(preg_replace('/\xC2\x8E/', '', $row->childNodes->item(2)->nodeValue)),
            'respondent' => trim(preg_replace('/\xC2\x8E/', '', $row->childNodes->item(4)->nodeValue)),
            'judgment_year' =>  $year,
            'filing_number' => trim($row->childNodes->item(0)->nodeValue)
        );
        if ($result['filing_number']) array_push($results, $result);
        //Clean loop variables
        $option = null;
        $result = null;
        unset($option);
        unset($result);
        if ($i % 100 === 0) {
            scraperwiki::save_sqlite(array('path'), $results);
            $results = array();
        }
    }
    
    //Clean up
    $query = null;
    $xpath = null;
    $ch = null;
    unset($query);
    unset($xpath);
    unset($ch);

    //Final save to database
    scraperwiki::save_sqlite(array('path'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

$case_types = array(67,57,65,66,62,61,55,12,11,8,63,58,20,37,34,42,21,39,35,5,24,27,54,6,29,7,64,53,52,16,51,15,28,14,1,25,31,3,19,33,2,10,23,32,60,56,74,36,40,68,9,26,43,73,4,22,17,50);
for ($year = date('Y'); $year < (date('Y')+1); $year++) {
    foreach ($case_types as $case_type) {
        scrape($year, $case_type);
    }
}
?><?php
function scrape($year, $case_type) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://jhr.nic.in/case_status/resp_output.php',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POSTFIELDS => http_build_query(array(
            'year'  => $year,
            'case_type' => $case_type
        )),
        CURLOPT_CONNECTTIMEOUT => 0,
        CURLOPT_TIMEOUT => 1000,
    ));

    echo "Loading data (year: $year; case type: $case_type) ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(curl_exec($ch));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 1; $i < $n; $i++) {
        $row = $query->item($i);
        if ($row->getElementsByTagName('a')->item(0)) {
            $path = $row->getElementsByTagName('a')->item(0)->getAttribute('href');
        }
        @$result = array(
            'case_number' => trim($row->getElementsByTagName('a')->item(0)->nodeValue),
            'path' => trim($path),
            'petitioner' => trim(preg_replace('/\xC2\x8E/', '', $row->childNodes->item(2)->nodeValue)),
            'respondent' => trim(preg_replace('/\xC2\x8E/', '', $row->childNodes->item(4)->nodeValue)),
            'judgment_year' =>  $year,
            'filing_number' => trim($row->childNodes->item(0)->nodeValue)
        );
        if ($result['filing_number']) array_push($results, $result);
        //Clean loop variables
        $option = null;
        $result = null;
        unset($option);
        unset($result);
        if ($i % 100 === 0) {
            scraperwiki::save_sqlite(array('path'), $results);
            $results = array();
        }
    }
    
    //Clean up
    $query = null;
    $xpath = null;
    $ch = null;
    unset($query);
    unset($xpath);
    unset($ch);

    //Final save to database
    scraperwiki::save_sqlite(array('path'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

$case_types = array(67,57,65,66,62,61,55,12,11,8,63,58,20,37,34,42,21,39,35,5,24,27,54,6,29,7,64,53,52,16,51,15,28,14,1,25,31,3,19,33,2,10,23,32,60,56,74,36,40,68,9,26,43,73,4,22,17,50);
for ($year = date('Y'); $year < (date('Y')+1); $year++) {
    foreach ($case_types as $case_type) {
        scrape($year, $case_type);
    }
}
?><?php
function scrape($year, $case_type) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://jhr.nic.in/case_status/resp_output.php',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POSTFIELDS => http_build_query(array(
            'year'  => $year,
            'case_type' => $case_type
        )),
        CURLOPT_CONNECTTIMEOUT => 0,
        CURLOPT_TIMEOUT => 1000,
    ));

    echo "Loading data (year: $year; case type: $case_type) ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(curl_exec($ch));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 1; $i < $n; $i++) {
        $row = $query->item($i);
        if ($row->getElementsByTagName('a')->item(0)) {
            $path = $row->getElementsByTagName('a')->item(0)->getAttribute('href');
        }
        @$result = array(
            'case_number' => trim($row->getElementsByTagName('a')->item(0)->nodeValue),
            'path' => trim($path),
            'petitioner' => trim(preg_replace('/\xC2\x8E/', '', $row->childNodes->item(2)->nodeValue)),
            'respondent' => trim(preg_replace('/\xC2\x8E/', '', $row->childNodes->item(4)->nodeValue)),
            'judgment_year' =>  $year,
            'filing_number' => trim($row->childNodes->item(0)->nodeValue)
        );
        if ($result['filing_number']) array_push($results, $result);
        //Clean loop variables
        $option = null;
        $result = null;
        unset($option);
        unset($result);
        if ($i % 100 === 0) {
            scraperwiki::save_sqlite(array('path'), $results);
            $results = array();
        }
    }
    
    //Clean up
    $query = null;
    $xpath = null;
    $ch = null;
    unset($query);
    unset($xpath);
    unset($ch);

    //Final save to database
    scraperwiki::save_sqlite(array('path'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

$case_types = array(67,57,65,66,62,61,55,12,11,8,63,58,20,37,34,42,21,39,35,5,24,27,54,6,29,7,64,53,52,16,51,15,28,14,1,25,31,3,19,33,2,10,23,32,60,56,74,36,40,68,9,26,43,73,4,22,17,50);
for ($year = date('Y'); $year < (date('Y')+1); $year++) {
    foreach ($case_types as $case_type) {
        scrape($year, $case_type);
    }
}
?>