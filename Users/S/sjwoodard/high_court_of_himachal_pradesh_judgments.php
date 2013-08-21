<?php
function scrape() { //USE MONTH/DAY/YEAR!!!!!
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://hphighcourt.nic.in/inetjudord/jud_periodoutnew.asp',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CONNECTTIMEOUT => 0,
        CURLOPT_TIMEOUT => 1000,
        CURLOPT_POSTFIELDS => http_build_query(array(
            'FDATE' => ltrim(date("m", strtotime("-30 days")), '0') .'/'. ltrim(date("d", strtotime("-30 days")), '0') .'/'. date('Y', strtotime("-30 days")),
            'TDATE' => ltrim(date("m"), '0') .'/'. ltrim(date("d"), '0') .'/'. date('Y'),
            'submit' => 'Submit',
        )),
    ));

    echo "Loading data ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(curl_exec($ch));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//table[@width="80%"]/tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $row = $query->item($i);
        $title = explode('-Vs-', $row->childNodes->item(2)->nodeValue);
        @$result = array(
            'case_number' => trim($row->childNodes->item(0)->nodeValue),
            'judgment_date' => trim($row->childNodes->item(1)->nodeValue),
            'petitioner' => trim($title[0]),
            'respondent' => trim($title[1]),
            'path' => ltrim($row->getElementsByTagName('a')->item(0)->getAttribute('href'), '.'),
            'has_connected_matter' => '',
            'unique_id' => preg_replace('/\s+\W+/', '', trim($row->childNodes->item(0)->nodeValue) .'-'. ltrim($row->getElementsByTagName('a')->item(0)->getAttribute('href'), '.'))
        );
        if ($row->getElementsByTagName('a')->length > 1) { 
            $result['has_connected_matter'] = 'YES';
        }
        array_push($results, $result);
        //Clean loop variables
        $option = null;
        $result = null;
        unset($option);
        unset($result);
        if ($i > 1 && $i % 100 === 0) {
            scraperwiki::save_sqlite(array('unique_id'), $results);
            $results = array();
        }
    }
    
    //Clean up
    $options = null;
    $ch = null;
    unset($options);
    unset($ch);

    //Last save to database
    scraperwiki::save_sqlite(array('unique_id'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

scrape();
?><?php
function scrape() { //USE MONTH/DAY/YEAR!!!!!
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://hphighcourt.nic.in/inetjudord/jud_periodoutnew.asp',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CONNECTTIMEOUT => 0,
        CURLOPT_TIMEOUT => 1000,
        CURLOPT_POSTFIELDS => http_build_query(array(
            'FDATE' => ltrim(date("m", strtotime("-30 days")), '0') .'/'. ltrim(date("d", strtotime("-30 days")), '0') .'/'. date('Y', strtotime("-30 days")),
            'TDATE' => ltrim(date("m"), '0') .'/'. ltrim(date("d"), '0') .'/'. date('Y'),
            'submit' => 'Submit',
        )),
    ));

    echo "Loading data ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(curl_exec($ch));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//table[@width="80%"]/tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $row = $query->item($i);
        $title = explode('-Vs-', $row->childNodes->item(2)->nodeValue);
        @$result = array(
            'case_number' => trim($row->childNodes->item(0)->nodeValue),
            'judgment_date' => trim($row->childNodes->item(1)->nodeValue),
            'petitioner' => trim($title[0]),
            'respondent' => trim($title[1]),
            'path' => ltrim($row->getElementsByTagName('a')->item(0)->getAttribute('href'), '.'),
            'has_connected_matter' => '',
            'unique_id' => preg_replace('/\s+\W+/', '', trim($row->childNodes->item(0)->nodeValue) .'-'. ltrim($row->getElementsByTagName('a')->item(0)->getAttribute('href'), '.'))
        );
        if ($row->getElementsByTagName('a')->length > 1) { 
            $result['has_connected_matter'] = 'YES';
        }
        array_push($results, $result);
        //Clean loop variables
        $option = null;
        $result = null;
        unset($option);
        unset($result);
        if ($i > 1 && $i % 100 === 0) {
            scraperwiki::save_sqlite(array('unique_id'), $results);
            $results = array();
        }
    }
    
    //Clean up
    $options = null;
    $ch = null;
    unset($options);
    unset($ch);

    //Last save to database
    scraperwiki::save_sqlite(array('unique_id'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

scrape();
?>