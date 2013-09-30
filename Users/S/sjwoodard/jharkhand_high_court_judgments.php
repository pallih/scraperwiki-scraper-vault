<?php
function scrape($page) {
    $ch = curl_init();
    $q = http_build_query(array(
        'page' => $page,
        'respname'  => '%',
        'from' => date('Y/m/d', strtotime("-1 month")),
        'to' => date('Y/m/d')
    ));
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://jhr.nic.in/hcjudge/resp_output.php?'. $q,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CONNECTTIMEOUT => 0,
        CURLOPT_TIMEOUT => 1000,
    ));

    echo "Loading data (page $page)...\n";
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
        preg_match_all('/>(.*?)</m', $row->childNodes->item(2)->ownerDocument->saveXML($row->childNodes->item(2)), $case_details);
        $subjects = preg_split('/Vs/i', str_replace('&amp;', '&', str_replace("\n", "", $case_details[1][1])));
        @$result = array(
            'case_number' => trim(str_replace("\n", " ", $case_details[1][0])),
            'path' => $path,
            'petitioner' => trim($subjects[0]),
            'respondent' => trim($subjects[1]),
            'judgment_date' =>  $row->childNodes->item(2)->nodeValue,
            'unique_id' => trim(str_replace("\n", " ", $case_details[1][0])) .'-'. $path
        );
        array_push($results, $result);
        //Clean loop variables
        $option = null;
        $result = null;
        unset($option);
        unset($result);
        if ($i % 100 === 0) {
            scraperwiki::save_sqlite(array('unique_id'), $results);
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
    scraperwiki::save_sqlite(array('unique_id'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    
    if ($n < 10) {
        return true;
    } else {
        return false;
    }
}

$i = 1;
$a = scrape($i);
$i++;
while ($a === false) {
    $a = scrape($i);
    $i++;
}
?><?php
function scrape($page) {
    $ch = curl_init();
    $q = http_build_query(array(
        'page' => $page,
        'respname'  => '%',
        'from' => date('Y/m/d', strtotime("-1 month")),
        'to' => date('Y/m/d')
    ));
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://jhr.nic.in/hcjudge/resp_output.php?'. $q,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CONNECTTIMEOUT => 0,
        CURLOPT_TIMEOUT => 1000,
    ));

    echo "Loading data (page $page)...\n";
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
        preg_match_all('/>(.*?)</m', $row->childNodes->item(2)->ownerDocument->saveXML($row->childNodes->item(2)), $case_details);
        $subjects = preg_split('/Vs/i', str_replace('&amp;', '&', str_replace("\n", "", $case_details[1][1])));
        @$result = array(
            'case_number' => trim(str_replace("\n", " ", $case_details[1][0])),
            'path' => $path,
            'petitioner' => trim($subjects[0]),
            'respondent' => trim($subjects[1]),
            'judgment_date' =>  $row->childNodes->item(2)->nodeValue,
            'unique_id' => trim(str_replace("\n", " ", $case_details[1][0])) .'-'. $path
        );
        array_push($results, $result);
        //Clean loop variables
        $option = null;
        $result = null;
        unset($option);
        unset($result);
        if ($i % 100 === 0) {
            scraperwiki::save_sqlite(array('unique_id'), $results);
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
    scraperwiki::save_sqlite(array('unique_id'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    
    if ($n < 10) {
        return true;
    } else {
        return false;
    }
}

$i = 1;
$a = scrape($i);
$i++;
while ($a === false) {
    $a = scrape($i);
    $i++;
}
?><?php
function scrape($page) {
    $ch = curl_init();
    $q = http_build_query(array(
        'page' => $page,
        'respname'  => '%',
        'from' => date('Y/m/d', strtotime("-1 month")),
        'to' => date('Y/m/d')
    ));
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://jhr.nic.in/hcjudge/resp_output.php?'. $q,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CONNECTTIMEOUT => 0,
        CURLOPT_TIMEOUT => 1000,
    ));

    echo "Loading data (page $page)...\n";
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
        preg_match_all('/>(.*?)</m', $row->childNodes->item(2)->ownerDocument->saveXML($row->childNodes->item(2)), $case_details);
        $subjects = preg_split('/Vs/i', str_replace('&amp;', '&', str_replace("\n", "", $case_details[1][1])));
        @$result = array(
            'case_number' => trim(str_replace("\n", " ", $case_details[1][0])),
            'path' => $path,
            'petitioner' => trim($subjects[0]),
            'respondent' => trim($subjects[1]),
            'judgment_date' =>  $row->childNodes->item(2)->nodeValue,
            'unique_id' => trim(str_replace("\n", " ", $case_details[1][0])) .'-'. $path
        );
        array_push($results, $result);
        //Clean loop variables
        $option = null;
        $result = null;
        unset($option);
        unset($result);
        if ($i % 100 === 0) {
            scraperwiki::save_sqlite(array('unique_id'), $results);
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
    scraperwiki::save_sqlite(array('unique_id'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    
    if ($n < 10) {
        return true;
    } else {
        return false;
    }
}

$i = 1;
$a = scrape($i);
$i++;
while ($a === false) {
    $a = scrape($i);
    $i++;
}
?><?php
function scrape($page) {
    $ch = curl_init();
    $q = http_build_query(array(
        'page' => $page,
        'respname'  => '%',
        'from' => date('Y/m/d', strtotime("-1 month")),
        'to' => date('Y/m/d')
    ));
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://jhr.nic.in/hcjudge/resp_output.php?'. $q,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CONNECTTIMEOUT => 0,
        CURLOPT_TIMEOUT => 1000,
    ));

    echo "Loading data (page $page)...\n";
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
        preg_match_all('/>(.*?)</m', $row->childNodes->item(2)->ownerDocument->saveXML($row->childNodes->item(2)), $case_details);
        $subjects = preg_split('/Vs/i', str_replace('&amp;', '&', str_replace("\n", "", $case_details[1][1])));
        @$result = array(
            'case_number' => trim(str_replace("\n", " ", $case_details[1][0])),
            'path' => $path,
            'petitioner' => trim($subjects[0]),
            'respondent' => trim($subjects[1]),
            'judgment_date' =>  $row->childNodes->item(2)->nodeValue,
            'unique_id' => trim(str_replace("\n", " ", $case_details[1][0])) .'-'. $path
        );
        array_push($results, $result);
        //Clean loop variables
        $option = null;
        $result = null;
        unset($option);
        unset($result);
        if ($i % 100 === 0) {
            scraperwiki::save_sqlite(array('unique_id'), $results);
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
    scraperwiki::save_sqlite(array('unique_id'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    
    if ($n < 10) {
        return true;
    } else {
        return false;
    }
}

$i = 1;
$a = scrape($i);
$i++;
while ($a === false) {
    $a = scrape($i);
    $i++;
}
?>