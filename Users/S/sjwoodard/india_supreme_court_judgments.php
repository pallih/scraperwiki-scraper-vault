<?php
function scrape($cookie, $offset) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://164.100.9.38/judis/handle/123456789/2/simple-search?query=%25&sort_by=2&order=ASC&rpp=100&etal=0&start='. $offset,
        CURLOPT_COOKIE => $cookie,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CONNECTTIMEOUT => 0,
        CURLOPT_TIMEOUT => 1000,
    ));

    echo "Loading data ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(curl_exec($ch));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//table[@class="miscTable"]/tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing results ...\n";
    $results = array();
    $n = $query->length;
    for ($i = 0; $i < $n; $i++) {
        $row = $query->item($i);
        if ($row->childNodes->item(7)->childNodes) {
            if ($row->childNodes->item(7)->childNodes->item(0)) {
                $a = $row->childNodes->item(7)->childNodes->item(0)->getAttribute('href');
            }
        }
        @$result = array(
            'judgment_date' => $row->childNodes->item(0)->nodeValue,
            'case_number' => $row->childNodes->item(2)->nodeValue,
            'path' => $a,
            'judge' => $row->childNodes->item(3)->nodeValue,
            'petitioner' => $row->childNodes->item(4)->nodeValue,
            'respondent' => $row->childNodes->item(5)->nodeValue,
            'unique_id' => preg_replace('/\s+|+W+/', '', $row->childNodes->item(2)->nodeValue .'-'. $a)
        );
        if ($i > 0) array_push($results, $result);
    }
    
    $results_found = count($results);
    scraperwiki::save_sqlite(array('unique_id'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    $query = null;
    $results = null;
    unset($query);
    unset($results);
    if ($results_found >= 100) {
        scrape($cookie, ($offset+100));
    }
}

$data = get_headers('http://164.100.9.38/judis/');
preg_match('/Set-Cookie: (.*?);/i', $data[4], $cookie);
scrape($cookie[1], 0);
?><?php
function scrape($cookie, $offset) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://164.100.9.38/judis/handle/123456789/2/simple-search?query=%25&sort_by=2&order=ASC&rpp=100&etal=0&start='. $offset,
        CURLOPT_COOKIE => $cookie,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CONNECTTIMEOUT => 0,
        CURLOPT_TIMEOUT => 1000,
    ));

    echo "Loading data ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(curl_exec($ch));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//table[@class="miscTable"]/tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing results ...\n";
    $results = array();
    $n = $query->length;
    for ($i = 0; $i < $n; $i++) {
        $row = $query->item($i);
        if ($row->childNodes->item(7)->childNodes) {
            if ($row->childNodes->item(7)->childNodes->item(0)) {
                $a = $row->childNodes->item(7)->childNodes->item(0)->getAttribute('href');
            }
        }
        @$result = array(
            'judgment_date' => $row->childNodes->item(0)->nodeValue,
            'case_number' => $row->childNodes->item(2)->nodeValue,
            'path' => $a,
            'judge' => $row->childNodes->item(3)->nodeValue,
            'petitioner' => $row->childNodes->item(4)->nodeValue,
            'respondent' => $row->childNodes->item(5)->nodeValue,
            'unique_id' => preg_replace('/\s+|+W+/', '', $row->childNodes->item(2)->nodeValue .'-'. $a)
        );
        if ($i > 0) array_push($results, $result);
    }
    
    $results_found = count($results);
    scraperwiki::save_sqlite(array('unique_id'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    $query = null;
    $results = null;
    unset($query);
    unset($results);
    if ($results_found >= 100) {
        scrape($cookie, ($offset+100));
    }
}

$data = get_headers('http://164.100.9.38/judis/');
preg_match('/Set-Cookie: (.*?);/i', $data[4], $cookie);
scrape($cookie[1], 0);
?>