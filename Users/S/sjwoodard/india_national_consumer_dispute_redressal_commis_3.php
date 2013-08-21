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

function scrape() {
    $const_post = http_build_query(array( //Input fields for POST
        'method' => 'loadMainNcdrcQryPg',
        'stateCode' => '0',
        'login' => '',
        'distCode' => '0',
        'loginType' => 'B',
        'stateName' => '',
        'districtName' => '',
        'cid' => '',
        'userType' => 'B',
        'ncdrc_id' => 'ncdrc',
        'state_id' => '0',
        'state_idD' => '0',
        'dist_id' => '0',
        'fano' => '',
        'dtFrom' => date("d/m/Y", strtotime("-30 days")), //Look back 30 days; Use 01/01/1900 to load all results (takes 2-3 mins)
        'dtTo' => date("d/m/Y", strtotime("+5 days")),   //Look forward 5 days
        'andor' => 'or'
    ));

    $results = array();

    for ($i = 0; $i < 2; $i++) { //POST is split up into two sets of conditions because of website limitations. This executive cURL twice.
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
        $query = $xpath->query('*//tr');
        $n = $query->length;
        curl_close($ch);

        echo "Parsing results ...\n";
        for ($j = 0; $j < $n; $j++) {
            $row = $query->item($j);
            @$result = array(
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
            $result = null;
            $row = null;
            unset($result);
            unset($row);
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

    //Save results
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    scraperwiki::save_sqlite(array('case_number'), $results);
}

scrape();
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

function scrape() {
    $const_post = http_build_query(array( //Input fields for POST
        'method' => 'loadMainNcdrcQryPg',
        'stateCode' => '0',
        'login' => '',
        'distCode' => '0',
        'loginType' => 'B',
        'stateName' => '',
        'districtName' => '',
        'cid' => '',
        'userType' => 'B',
        'ncdrc_id' => 'ncdrc',
        'state_id' => '0',
        'state_idD' => '0',
        'dist_id' => '0',
        'fano' => '',
        'dtFrom' => date("d/m/Y", strtotime("-30 days")), //Look back 30 days; Use 01/01/1900 to load all results (takes 2-3 mins)
        'dtTo' => date("d/m/Y", strtotime("+5 days")),   //Look forward 5 days
        'andor' => 'or'
    ));

    $results = array();

    for ($i = 0; $i < 2; $i++) { //POST is split up into two sets of conditions because of website limitations. This executive cURL twice.
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
        $query = $xpath->query('*//tr');
        $n = $query->length;
        curl_close($ch);

        echo "Parsing results ...\n";
        for ($j = 0; $j < $n; $j++) {
            $row = $query->item($j);
            @$result = array(
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
            $result = null;
            $row = null;
            unset($result);
            unset($row);
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

    //Save results
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    scraperwiki::save_sqlite(array('case_number'), $results);
}

scrape();
?>