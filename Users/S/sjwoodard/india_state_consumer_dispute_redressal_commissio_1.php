<?php
function conditions($i) {
    //We need to search a total of 10 case types, but we can only run 6 at a time.
    //i=0 returns the first 6 and i=1 returns the last 4.
    
    $conditions = '';
    if ($i === 0) {
        for ($j = 1; $j < 7; $j++) { //Add initial 6 conditions
            $conditions .= '&condition=6&searchTxtHid='. $j .'&searchTxt=&ctId='. $j;
        }
    } elseif ($i === 1) {
        for ($j = 7; $j < 11; $j++) { //Add final 4 conditions
            $conditions .= '&condition=6&searchTxtHid='. $j .'&searchTxt=&ctId='. $j;
        }
        for ($j = 0; $j < 2; $j++) { //Must have 2 additional blank conditions
            $conditions .= '&condition=0&searchTxtHid=&searchTxt=&ctId=0';
        }
    }
    return $conditions;
}

function scrape($state_code, $state_name) {
    $const_post = http_build_query(array( //Input fields for POST
        'method' => 'loadMainNcdrcQryPg',
        'stateCode' => $state_code,
        'login' => '',
        'distCode' => '0',
        'loginType' => 'C',
        'stateName' => '',
        'districtName' => '',
        'cid' => '',
        'userType' => 'C',
        'ncdrc_id' => 'ncdrc',
        'state_id' => $state_code,
        'state_idD' => '0',
        'dist_id' => '0',
        'fano' => '',
        'dtFrom' => date('d/m/Y', strtotime('-10 days')), //Look back 30 days
        'dtTo' => date('d/m/Y'),
        'andor' => 'or'
    ));

    $results = array();

    for ($i = 0; $i < 2; $i++) { //POST is split up into two sets of conditions.
        $post = $const_post . conditions($i);

        $ch = curl_init();
        curl_setopt_array($ch, array(
            CURLOPT_URL => 'http://164.100.72.12/ncdrcusersWeb/login.do',
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POSTFIELDS => $post,
        ));

        echo "Loading data ...\n";
        $dom = new DOMDocument();
        @$dom->loadHTML(curl_exec($ch));
        $xpath = new DOMXPath($dom);
        if ($xpath->query('//title')->item(0)->nodeValue != 'Query Report') return array();
        $query = $xpath->query('//tr');
        $dom = null;
        $xpath = null;
        unset($dom);
        unset($xpath);
        $n = $query->length;
        curl_close($ch);

        echo "Parsing results ...\n";
        for ($j = 0; $j < $n; $j++) {
            $row = $query->item($j);
            if (!@preg_match('/No record is available/i', $row->childNodes->item(2)->nodeValue)) {
                @$result = array(
                    'state' => $state_name,
                    'case_number' => trim($row->childNodes->item(2)->nodeValue),
                    'complainant' => trim(str_replace('&amp;', '&', $row->childNodes->item(4)->nodeValue)),
                    'respondent' => trim(str_replace('&amp;', '&', $row->childNodes->item(6)->nodeValue)),
                    'complainant_advocate' => trim(str_replace('&amp;', '&', $row->childNodes->item(8)->nodeValue)),
                    'respondent_advocate' => trim(str_replace('&amp;', '&', $row->childNodes->item(10)->nodeValue)),
                    'filing_date' => trim($row->childNodes->item(12)->nodeValue),
                );
                if ($result['complainant'] == '-') $result['complainant'] = '';
                if ($result['respondent'] == '-') $result['respondent'] = '';
                if ($result['complainant_advocate'] == '-') $result['complainant_advocate'] = '';
                if ($result['respondent_advocate'] == '-') $result['respondent_advocate'] = '';
                if ($j > 0 && $result['case_number']) array_push($results, $result);
            }
            $result = null;
            $row = null;
            unset($result);
            unset($row);
            if ($j % 100 === 0) {
                scraperwiki::save_sqlite(array('case_number'), $results);
                $results = array();
            }
        }
        $dom = null;
        $xpath = null;
        $query = null;
        $ch = null;
        unset($dom);
        unset($xpath);
        unset($query);
        unset($ch);
    }
    //Last save to database
    scraperwiki::save_sqlite(array('case_number'), $results);
    $results = null;
    unset($results);
}

$state_array = array(
    2 => 'Jharkhand',
    4 => 'West Bengal',
    6 => 'Chandigarh',
    7 => 'Andaman Nicobar',
    8 => 'Delhi',
    9 => 'Haryana',
    10 => 'Himachal Pradesh',
    12 => 'Punjab',
    13 => 'Rajasthan',
    14 => 'Uttar Pradesh',
    15 => 'Uttaranchal',
    16 => 'Andhra Pradesh',
    17 => 'Kerala',
    19 => 'Tamil Nadu',
    20 => 'Gujarat',
    21 => 'Maharastra',
    22 => 'Madhya Pradesh',
    23 => 'Chhattisgarh',
    30 => 'Meghalaya',
    33 => 'Goa',
    36 => 'Circuit Bench Aurangabad',
    37 => 'Circuit Bench Nagpur',
);

foreach ($state_array as $state_code => $state_name) {
    scrape($state_code, $state_name);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}
?><?php
function conditions($i) {
    //We need to search a total of 10 case types, but we can only run 6 at a time.
    //i=0 returns the first 6 and i=1 returns the last 4.
    
    $conditions = '';
    if ($i === 0) {
        for ($j = 1; $j < 7; $j++) { //Add initial 6 conditions
            $conditions .= '&condition=6&searchTxtHid='. $j .'&searchTxt=&ctId='. $j;
        }
    } elseif ($i === 1) {
        for ($j = 7; $j < 11; $j++) { //Add final 4 conditions
            $conditions .= '&condition=6&searchTxtHid='. $j .'&searchTxt=&ctId='. $j;
        }
        for ($j = 0; $j < 2; $j++) { //Must have 2 additional blank conditions
            $conditions .= '&condition=0&searchTxtHid=&searchTxt=&ctId=0';
        }
    }
    return $conditions;
}

function scrape($state_code, $state_name) {
    $const_post = http_build_query(array( //Input fields for POST
        'method' => 'loadMainNcdrcQryPg',
        'stateCode' => $state_code,
        'login' => '',
        'distCode' => '0',
        'loginType' => 'C',
        'stateName' => '',
        'districtName' => '',
        'cid' => '',
        'userType' => 'C',
        'ncdrc_id' => 'ncdrc',
        'state_id' => $state_code,
        'state_idD' => '0',
        'dist_id' => '0',
        'fano' => '',
        'dtFrom' => date('d/m/Y', strtotime('-10 days')), //Look back 30 days
        'dtTo' => date('d/m/Y'),
        'andor' => 'or'
    ));

    $results = array();

    for ($i = 0; $i < 2; $i++) { //POST is split up into two sets of conditions.
        $post = $const_post . conditions($i);

        $ch = curl_init();
        curl_setopt_array($ch, array(
            CURLOPT_URL => 'http://164.100.72.12/ncdrcusersWeb/login.do',
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POSTFIELDS => $post,
        ));

        echo "Loading data ...\n";
        $dom = new DOMDocument();
        @$dom->loadHTML(curl_exec($ch));
        $xpath = new DOMXPath($dom);
        if ($xpath->query('//title')->item(0)->nodeValue != 'Query Report') return array();
        $query = $xpath->query('//tr');
        $dom = null;
        $xpath = null;
        unset($dom);
        unset($xpath);
        $n = $query->length;
        curl_close($ch);

        echo "Parsing results ...\n";
        for ($j = 0; $j < $n; $j++) {
            $row = $query->item($j);
            if (!@preg_match('/No record is available/i', $row->childNodes->item(2)->nodeValue)) {
                @$result = array(
                    'state' => $state_name,
                    'case_number' => trim($row->childNodes->item(2)->nodeValue),
                    'complainant' => trim(str_replace('&amp;', '&', $row->childNodes->item(4)->nodeValue)),
                    'respondent' => trim(str_replace('&amp;', '&', $row->childNodes->item(6)->nodeValue)),
                    'complainant_advocate' => trim(str_replace('&amp;', '&', $row->childNodes->item(8)->nodeValue)),
                    'respondent_advocate' => trim(str_replace('&amp;', '&', $row->childNodes->item(10)->nodeValue)),
                    'filing_date' => trim($row->childNodes->item(12)->nodeValue),
                );
                if ($result['complainant'] == '-') $result['complainant'] = '';
                if ($result['respondent'] == '-') $result['respondent'] = '';
                if ($result['complainant_advocate'] == '-') $result['complainant_advocate'] = '';
                if ($result['respondent_advocate'] == '-') $result['respondent_advocate'] = '';
                if ($j > 0 && $result['case_number']) array_push($results, $result);
            }
            $result = null;
            $row = null;
            unset($result);
            unset($row);
            if ($j % 100 === 0) {
                scraperwiki::save_sqlite(array('case_number'), $results);
                $results = array();
            }
        }
        $dom = null;
        $xpath = null;
        $query = null;
        $ch = null;
        unset($dom);
        unset($xpath);
        unset($query);
        unset($ch);
    }
    //Last save to database
    scraperwiki::save_sqlite(array('case_number'), $results);
    $results = null;
    unset($results);
}

$state_array = array(
    2 => 'Jharkhand',
    4 => 'West Bengal',
    6 => 'Chandigarh',
    7 => 'Andaman Nicobar',
    8 => 'Delhi',
    9 => 'Haryana',
    10 => 'Himachal Pradesh',
    12 => 'Punjab',
    13 => 'Rajasthan',
    14 => 'Uttar Pradesh',
    15 => 'Uttaranchal',
    16 => 'Andhra Pradesh',
    17 => 'Kerala',
    19 => 'Tamil Nadu',
    20 => 'Gujarat',
    21 => 'Maharastra',
    22 => 'Madhya Pradesh',
    23 => 'Chhattisgarh',
    30 => 'Meghalaya',
    33 => 'Goa',
    36 => 'Circuit Bench Aurangabad',
    37 => 'Circuit Bench Nagpur',
);

foreach ($state_array as $state_code => $state_name) {
    scrape($state_code, $state_name);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}
?>