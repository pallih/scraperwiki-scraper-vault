<?php
function scrape() {
    $post = http_build_query(array( //Input fields for POST
        'stateName1' => '',
        'distName1' => '',
        'comboDistrict' => '0',
        'comboState' => 'ALL',
        'districtCode' => '0',
        'stateCode' => '',
        'location' => 'S',
        'fromDate' => date("d/m/Y", strtotime("-30 days")), //Look back 30 days
        'toDate' => date("d/m/Y"),
    ));

    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://164.100.72.12/ncdrcrep/JTSStateNationalDates.jsp',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POSTFIELDS => $post,
    ));

    echo "Loading data ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(curl_exec($ch));
    $ch = null;
    unset($ch);
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//table[@id="content"]/tr[2]/td/table/tr[2]/td[2]/table/tr/td/a');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $a = $query->item($i);
        $row = $a->parentNode->parentNode;
        @$result = array(
            'state' => trim($row->childNodes->item(2)->nodeValue),
            'case_number' => trim($a->nodeValue),
            'path' => $a->getAttribute('href'),
            'complainant' => $row->childNodes->item(6)->nodeValue,
            'respondent' => $row->childNodes->item(8)->nodeValue,
            'judgment_date' => $row->childNodes->item(10)->nodeValue,
        );
        if ($result['case_number']) array_push($results, $result);
        $a = null;
        $row = null;
        $result = null;
        unset($a);
        unset($row);
        unset($result);
    }
    
    //Clean up and save
    $query = null;
    unset($query);
    scraperwiki::save_sqlite(array('case_number'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

scrape();

?>
<?php
function scrape() {
    $post = http_build_query(array( //Input fields for POST
        'stateName1' => '',
        'distName1' => '',
        'comboDistrict' => '0',
        'comboState' => 'ALL',
        'districtCode' => '0',
        'stateCode' => '',
        'location' => 'S',
        'fromDate' => date("d/m/Y", strtotime("-30 days")), //Look back 30 days
        'toDate' => date("d/m/Y"),
    ));

    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://164.100.72.12/ncdrcrep/JTSStateNationalDates.jsp',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POSTFIELDS => $post,
    ));

    echo "Loading data ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(curl_exec($ch));
    $ch = null;
    unset($ch);
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//table[@id="content"]/tr[2]/td/table/tr[2]/td[2]/table/tr/td/a');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $a = $query->item($i);
        $row = $a->parentNode->parentNode;
        @$result = array(
            'state' => trim($row->childNodes->item(2)->nodeValue),
            'case_number' => trim($a->nodeValue),
            'path' => $a->getAttribute('href'),
            'complainant' => $row->childNodes->item(6)->nodeValue,
            'respondent' => $row->childNodes->item(8)->nodeValue,
            'judgment_date' => $row->childNodes->item(10)->nodeValue,
        );
        if ($result['case_number']) array_push($results, $result);
        $a = null;
        $row = null;
        $result = null;
        unset($a);
        unset($row);
        unset($result);
    }
    
    //Clean up and save
    $query = null;
    unset($query);
    scraperwiki::save_sqlite(array('case_number'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

scrape();

?>
<?php
function scrape() {
    $post = http_build_query(array( //Input fields for POST
        'stateName1' => '',
        'distName1' => '',
        'comboDistrict' => '0',
        'comboState' => 'ALL',
        'districtCode' => '0',
        'stateCode' => '',
        'location' => 'S',
        'fromDate' => date("d/m/Y", strtotime("-30 days")), //Look back 30 days
        'toDate' => date("d/m/Y"),
    ));

    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://164.100.72.12/ncdrcrep/JTSStateNationalDates.jsp',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POSTFIELDS => $post,
    ));

    echo "Loading data ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(curl_exec($ch));
    $ch = null;
    unset($ch);
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//table[@id="content"]/tr[2]/td/table/tr[2]/td[2]/table/tr/td/a');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $a = $query->item($i);
        $row = $a->parentNode->parentNode;
        @$result = array(
            'state' => trim($row->childNodes->item(2)->nodeValue),
            'case_number' => trim($a->nodeValue),
            'path' => $a->getAttribute('href'),
            'complainant' => $row->childNodes->item(6)->nodeValue,
            'respondent' => $row->childNodes->item(8)->nodeValue,
            'judgment_date' => $row->childNodes->item(10)->nodeValue,
        );
        if ($result['case_number']) array_push($results, $result);
        $a = null;
        $row = null;
        $result = null;
        unset($a);
        unset($row);
        unset($result);
    }
    
    //Clean up and save
    $query = null;
    unset($query);
    scraperwiki::save_sqlite(array('case_number'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

scrape();

?>
<?php
function scrape() {
    $post = http_build_query(array( //Input fields for POST
        'stateName1' => '',
        'distName1' => '',
        'comboDistrict' => '0',
        'comboState' => 'ALL',
        'districtCode' => '0',
        'stateCode' => '',
        'location' => 'S',
        'fromDate' => date("d/m/Y", strtotime("-30 days")), //Look back 30 days
        'toDate' => date("d/m/Y"),
    ));

    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://164.100.72.12/ncdrcrep/JTSStateNationalDates.jsp',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POSTFIELDS => $post,
    ));

    echo "Loading data ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(curl_exec($ch));
    $ch = null;
    unset($ch);
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//table[@id="content"]/tr[2]/td/table/tr[2]/td[2]/table/tr/td/a');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $a = $query->item($i);
        $row = $a->parentNode->parentNode;
        @$result = array(
            'state' => trim($row->childNodes->item(2)->nodeValue),
            'case_number' => trim($a->nodeValue),
            'path' => $a->getAttribute('href'),
            'complainant' => $row->childNodes->item(6)->nodeValue,
            'respondent' => $row->childNodes->item(8)->nodeValue,
            'judgment_date' => $row->childNodes->item(10)->nodeValue,
        );
        if ($result['case_number']) array_push($results, $result);
        $a = null;
        $row = null;
        $result = null;
        unset($a);
        unset($row);
        unset($result);
    }
    
    //Clean up and save
    $query = null;
    unset($query);
    scraperwiki::save_sqlite(array('case_number'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

scrape();

?>
