<?php
function scrape($cookie, $offset) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://lobis.nic.in/ori/title1.php?offset='. $offset,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_COOKIE => $cookie,
        CURLOPT_CONNECTTIMEOUT => 0,
        CURLOPT_TIMEOUT => 1000,
        CURLOPT_POSTFIELDS => http_build_query(array(
            'radiosel'  => 'O',
            'p_name'  => '%',
            'frdate' => date("d/m/Y", strtotime("-10 days")),
            'todate' => date("d/m/Y"),
            'Submit' => 'Submit',
        )),
    ));

    echo "Loading data ...\n";
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
    for ($i = 0; $i < $n; $i++) {
        $row = $query->item($i);
        $case_title = explode('Vs.', $row->childNodes->item(3)->nodeValue);
        @$result = array(
            'case_number'    => trim(str_replace('--', ' ', $row->childNodes->item(1)->nodeValue)),
            'judgment_date'  => trim($row->childNodes->item(2)->nodeValue),
            'petitioner'     => trim($case_title[0]),
            'respondent'     => trim($case_title[1]),
            'path'           => $row->childNodes->item(1)->childNodes->item(0)->getAttribute('href'),
        );
        if ($i > 0 && $result['case_number']) array_push($results, $result);
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

    //Save to database
    scraperwiki::save_sqlite(array('case_number'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

$ch = curl_init();
curl_setopt_array($ch, array(
    CURLOPT_URL => 'http://lobis.nic.in/ori/title1.php?dc=19&fflag=1',
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_HEADER => true,
    CURLOPT_POSTFIELDS => http_build_query(array(
        'radiosel'  => 'O',
        'p_name'  => '%',
        'frdate' => date("d/m/Y", strtotime("-10 days")),
        'todate' => date("d/m/Y"),
        'Submit' => 'Submit',
    )),
    CURLOPT_CONNECTTIMEOUT => 0,
    CURLOPT_TIMEOUT => 1000,
));
    echo "Loading data ...\n";
    $dom = new DOMDocument();
    $data = curl_exec($ch);
    preg_match('/Set-Cookie: (.*?);/i', $data, $cookie);
    @$dom->loadHTML($data);
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $total_results = intval(preg_replace('/\D+/', '', $xpath->query('//p[@class="style2"]')->item(0)->nodeValue));
    $xpath = null;
    unset($xpath);

for ($i = 0; $i < ($total_results/10); $i++) { //10 results per page
    scrape($cookie[1], $i*10);
}

?>