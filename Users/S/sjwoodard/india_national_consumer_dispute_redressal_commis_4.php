<?php
function scrape() {
    $post = http_build_query(array( //Input fields for POST
        'stateName1' => '',
        'distName1' => '',
        'comboDistrict' => '0',
        'comboState' => '0',
        'districtCode' => '0',
        'stateCode' => '0',
        'location' => 'N',
        'fromDate' => date("d/m/Y", strtotime("-30 days")), //Look back 30 days
        'toDate' => date("d/m/Y", strtotime("+5 days")), //Look forward 5 days
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
    $xpath = new DOMXPath($dom);
    $query = $xpath->query('//table[@id="content"]/tr[2]/td/table/tr[2]/td[2]/table/tr/td/a');
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $a = $query->item($i);
        $row = $a->parentNode->parentNode;
        @$result = array(
            'case_number' => $a->nodeValue,
            'path' => $a->getAttribute('href'),
            'complainant' => $row->childNodes->item(4)->nodeValue,
            'respondent' => $row->childNodes->item(6)->nodeValue,
            'judgment_date' => $row->childNodes->item(8)->nodeValue,
        );
        if ($result['case_number']) array_push($results, $result);
        //Clean loop variables
        $a = null;
        $row = null;
        $result = null;
        unset($a);
        unset($row);
        unset($result);
    }
    
    //Clean up
    $query = null;
    $dom = null;
    $xpath = null;
    $ch = null;
    unset($query);
    unset($dom);
    unset($xpath);
    unset($ch);

    //Save to database
    scraperwiki::save_sqlite(array('case_number'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

scrape();
?><?php
function scrape() {
    $post = http_build_query(array( //Input fields for POST
        'stateName1' => '',
        'distName1' => '',
        'comboDistrict' => '0',
        'comboState' => '0',
        'districtCode' => '0',
        'stateCode' => '0',
        'location' => 'N',
        'fromDate' => date("d/m/Y", strtotime("-30 days")), //Look back 30 days
        'toDate' => date("d/m/Y", strtotime("+5 days")), //Look forward 5 days
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
    $xpath = new DOMXPath($dom);
    $query = $xpath->query('//table[@id="content"]/tr[2]/td/table/tr[2]/td[2]/table/tr/td/a');
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $a = $query->item($i);
        $row = $a->parentNode->parentNode;
        @$result = array(
            'case_number' => $a->nodeValue,
            'path' => $a->getAttribute('href'),
            'complainant' => $row->childNodes->item(4)->nodeValue,
            'respondent' => $row->childNodes->item(6)->nodeValue,
            'judgment_date' => $row->childNodes->item(8)->nodeValue,
        );
        if ($result['case_number']) array_push($results, $result);
        //Clean loop variables
        $a = null;
        $row = null;
        $result = null;
        unset($a);
        unset($row);
        unset($result);
    }
    
    //Clean up
    $query = null;
    $dom = null;
    $xpath = null;
    $ch = null;
    unset($query);
    unset($dom);
    unset($xpath);
    unset($ch);

    //Save to database
    scraperwiki::save_sqlite(array('case_number'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

scrape();
?><?php
function scrape() {
    $post = http_build_query(array( //Input fields for POST
        'stateName1' => '',
        'distName1' => '',
        'comboDistrict' => '0',
        'comboState' => '0',
        'districtCode' => '0',
        'stateCode' => '0',
        'location' => 'N',
        'fromDate' => date("d/m/Y", strtotime("-30 days")), //Look back 30 days
        'toDate' => date("d/m/Y", strtotime("+5 days")), //Look forward 5 days
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
    $xpath = new DOMXPath($dom);
    $query = $xpath->query('//table[@id="content"]/tr[2]/td/table/tr[2]/td[2]/table/tr/td/a');
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $a = $query->item($i);
        $row = $a->parentNode->parentNode;
        @$result = array(
            'case_number' => $a->nodeValue,
            'path' => $a->getAttribute('href'),
            'complainant' => $row->childNodes->item(4)->nodeValue,
            'respondent' => $row->childNodes->item(6)->nodeValue,
            'judgment_date' => $row->childNodes->item(8)->nodeValue,
        );
        if ($result['case_number']) array_push($results, $result);
        //Clean loop variables
        $a = null;
        $row = null;
        $result = null;
        unset($a);
        unset($row);
        unset($result);
    }
    
    //Clean up
    $query = null;
    $dom = null;
    $xpath = null;
    $ch = null;
    unset($query);
    unset($dom);
    unset($xpath);
    unset($ch);

    //Save to database
    scraperwiki::save_sqlite(array('case_number'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

scrape();
?>