<?php
function scrape($day, $month, $year) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://www.hcbombayatgoa.nic.in/date_JQ.asp',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_USERAGENT => 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17',
        CURLOPT_POSTFIELDS => http_build_query(array(
            'txtday' => $day,
            'txtmonth' => $month,
            'txtyear' => $year,
        )),
    ));

    echo "Loading data for ". $day.'/'. $month .'/'. $year ." ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(curl_exec($ch));
    $ch = null;
    unset($ch);
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//*[@id="txtlist"]/option');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $row = $query->item($i);
        $outer_text = explode("\n", $row->nodeValue);
        preg_match_all('/&gt;(.*?)&lt;/i', $row->ownerDocument->saveXML($row), $inner_text);
        $date_in = trim($outer_text[2]);
        preg_match_all('/\s?(.*?)\s+/', $date_in, $matches);
        $month = $matches[1][1];
        $date = trim($matches[1][2], ',');
        $year = $matches[1][3];
        $month_array = array(
            'January' => '01',
            'February' => '02',
            'March' => '03',
            'April' => '04',
            'May' => '05',
            'June' => '06',
            'July' => '07',
            'August' => '08',
            'September' => '09',
            'October' => '10',
            'November' => '11',
            'December' => '12',
        );
        $date_out = $date .'/'. $month_array[$month] .'/'. $year;
        @$result = array(
            'case_number' => preg_replace('/\xC2\xA0|\s+/', '', $outer_text[1]),
            'path' => $row->getAttribute('value'),
            'petitioner' => $inner_text[1][1],
            'respondent' => $inner_text[1][4],
            'judge' => $inner_text[1][7],
            'judgment_date' => $date_out,
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

for ($i = 0; $i< 30; $i++) {
    $day = date('d', strtotime('-'. $i .' days'));
    $month = date('m', strtotime('-'. $i .' days'));
    $year = date('Y', strtotime('-'. $i .' days'));
    scrape($day, $month, $year);
}
?>
