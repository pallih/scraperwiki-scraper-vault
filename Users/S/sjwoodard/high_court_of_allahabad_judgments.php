<?php
function scrape($from, $to, $mode, $cookie, $page, $pages) {
    if ($mode == 'get_results_total') {
        echo "Loading session data (". $from[0].'/'.$from[1].'/'.$from[2].' -> '.$to[0].'/'.$to[1].'/'.$to[2].") ...\n";
        $options = array(
            CURLOPT_URL => 'http://elegalix.allahabadhighcourt.in/elegalix/WebTitleSearch.do',
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_HEADER => true,
            CURLOPT_POSTFIELDS => http_build_query(array(
                'titleType'  => 'X',
                'title'  => '%',
                'highCourtBenchCode'   => 'X',
                'fromDay' => $from[0],
                'fromMonth' => $from[1],
                'fromYear' => $from[2],
                'toDay' => $to[0],
                'toMonth' => $to[1],
                'toYear' => $to[2],
                'navigator_appname' => 'Netscape',
                'navigator_useragent' => 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17',
                'navigator_appversion' => '5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17',
                'submit' => 'Submit',
            )),
            CURLOPT_CONNECTTIMEOUT => 0,
            CURLOPT_TIMEOUT => 1000,
        );
    }
    if ($mode == 'first_page') {
        echo "Loading data (". $from[0].'/'.$from[1].'/'.$from[2].' -> '.$to[0].'/'.$to[1].'/'.$to[2]."; page 1 of $pages) ...\n";
        $options = array(
            CURLOPT_URL => 'http://elegalix.allahabadhighcourt.in/elegalix/WebTitleSearch.do',
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_COOKIE => $cookie,
            CURLOPT_POSTFIELDS => http_build_query(array(
                'titleType'  => 'X',
                'title'  => '%',
                'highCourtBenchCode'   => 'X',
                'fromDay' => $from[0],
                'fromMonth' => $from[1],
                'fromYear' => $from[2],
                'toDay' => $to[0],
                'toMonth' => $to[1],
                'toYear' => $to[2],
                'navigator_appname' => 'Netscape',
                'navigator_useragent' => 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17',
                'navigator_appversion' => '5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17',
                'submit' => 'Submit',
            )),
            CURLOPT_CONNECTTIMEOUT => 0,
            CURLOPT_TIMEOUT => 1000,
        );
    }
    if ($mode == 'next_page') {
        echo "Loading data (". $from[0].'/'.$from[1].'/'.$from[2].' -> '.$to[0].'/'.$to[1].'/'.$to[2]."; page ". ($page + 1) ." of $pages) ...\n";
        $options = array(
            CURLOPT_URL => 'http://elegalix.allahabadhighcourt.in/elegalix/WebShowResults.do?pagenumber='. $page,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_COOKIE => $cookie,
            CURLOPT_CONNECTTIMEOUT => 0,
            CURLOPT_TIMEOUT => 1000,
        );
echo $cookie;
    }

    $ch = curl_init();
    curl_setopt_array($ch, $options);
    $dom = new DOMDocument();
    $html = curl_exec($ch);
    @$dom->loadHTML($html);
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    if ($mode == 'get_results_total') {
        preg_match('/Set-Cookie:\s+(.*?);/i', $html, $cookie);
        return @array($cookie[1], intval(preg_replace('/\D+/', '', $xpath->query('//p/i/font')->item(0)->nodeValue)));
    }
    $html = null;
    unset($html);
    $query = $xpath->query('//tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    $results = array();
    for ($i = 1; $i < ($n - 1); $i++) {
        $row = $query->item($i);
        $html = preg_replace('/&#13;|<br\/>|-|\n|\r|\xC2\xA0/i', '', $row->childNodes->item(2)->ownerDocument->saveXML($row->childNodes->item(2)));
        preg_match_all('/<\/b>(.*?)<b>/is', preg_replace('/\s+/s', ' ', $html), $row_matches);
        $a = $row->getElementsByTagName('a')->item(0);
        if ($a) {
            $title = explode(':', preg_replace('/\s+/s', ' ', $a->nodeValue));
            @$subjects = explode('Vs.', $title[1]);
            @$result = array(
                'unique_id' => $from[0].$from[1].$from[2].'-'.$to[0].$to[1].$to[2].'-'.preg_replace('/\xC2\xA0|\./', '', $row->childNodes->item(0)->nodeValue).'-'.preg_replace('/\D+/', '', $a->getAttribute('href')),
                'case_number' => trim($title[0]),
                'path'        => trim($a->getAttribute('href')),
                'petitioner'  => trim($subjects[0]),
                'respondent'  => trim($subjects[1]),
                'judgment_date'  => trim($row_matches[1][0]),
                'court_number'   => trim($row_matches[1][1]),
                'judgment_type'  => trim($row_matches[1][2]),
                'coram'  => trim($row_matches[1][3]),
            );
            if (strpos($result['path'], 'WebShowResults.do') === false) array_push($results, $result);
        }
        //Clean loop variables
        $option = null;
        $result = null;
        unset($option);
        unset($result);
        if ($i % 100 === 0) {
            //scraperwiki::save_sqlite(array('unique_id'), $results);
            $results = array();
        }
    }
    
    //Clean up
    $options = null;
    $ch = null;
    unset($options);
    unset($ch);
    //Final save to database
    //scraperwiki::save_sqlite(array('unique_id'), $results);
    $results = null;
    unset($results);
}

for ($year = date('Y'); $year < (date('Y') + 1); $year++) {
    for ($month = (date('m') - 1); $month < (date('m') + 1); $month++) {
        $end_day = cal_days_in_month(CAL_GREGORIAN, $month, $year);
        $from = array(1, $month, $year);
        $to = array($end_day, $month, $year);
        $details = scrape($from, $to, 'get_results_total', null, 'NA', 'NA');
        $cookie = $details[0];
        $pages = ceil($details[1] / 50);
        scrape($from, $to, 'first_page', $cookie, 0, $pages);
        for ($i = 1; $i < $pages; $i++) {
            scrape($from, $to, 'next_page', $cookie, $i, $pages);
        }
    }
}
?>