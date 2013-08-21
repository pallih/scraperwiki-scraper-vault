<?php
//ASP.Net gives unique credentials when first running a query. Therefore, the script needed to acces the first page
//is more intensive than the script for all other pages. 

function first_page($cookie, $viewstate, $event_validation, $from, $to) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://judis.nic.in/Judis_Jammu/causetitle.aspx',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_COOKIE => $cookie,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => http_build_query(array(
            '__VIEWSTATE' => $viewstate,
            '__EVENTVALIDATION' => $event_validation,
            'txttitle' => '',
            'seltitletype' => '1',
            'selfday' => $from['day'],
            'selfmonth' => $from['month'],
            'selfyear' => $from['year'],
            'seltday' => $to['day'],
            'seltmonth' => $to['month'],
            'seltyear' => $to['year'],
            'button' => 'Submit',
        )),
    ));
    $data = curl_exec($ch);
    curl_close($ch);
    $ch = null;
    unset($ch);
    return $data;
}

function not_first_page($cookie, $viewstate, $event_validation, $page) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://judis.nic.in/Judis_Jammu/Chrseq.aspx',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_COOKIE => $cookie,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => http_build_query(array(
            '__VIEWSTATE' => $viewstate,
            '__EVENTVALIDATION' => $event_validation,
            '__EVENTTARGET' => 'DataGrid1$ctl19$ctl'. sprintf("%02s", $page),
            '__EVENTARGUMENT' => '',
        )),
    ));
    $data = curl_exec($ch);
    curl_close($ch);
    $ch = null;
    unset($ch);
    return $data;
}

function scrape($cookie, $viewstate, $event_validation, $page, $from, $to, $last_row_number) {
    echo "Loading data (". $from['day'] .'/'. $from['month'] .'/'. $from['year'] .' -> '. $to['day'] .'/'. $to['month'] .'/'. $to['year'] .") ...\n";
    $dom = new DOMDocument();
    if (!$page) {
        @$dom->loadHTML(first_page($cookie, $viewstate, $event_validation, $from, $to));
    } else {
        @$dom->loadHTML(not_first_page($cookie, $viewstate, $event_validation, $page));
    }
    $xpath = new DOMXPath($dom);
    @$records_found = intval(preg_replace('/\D/', '', $xpath->query('//*[@id="Label5"]')->item(0)->nodeValue));
    $viewstate = $xpath->query('//*[@id="__VIEWSTATE"]')->item(0)->getAttribute('value');
    $event_validation = $xpath->query('//*[@id="__EVENTVALIDATION"]');
    if ($event_validation->length) $event_validation = $event_validation->item(0)->getAttribute('value');
    $query = $xpath->query('//table[@id="DataGrid1"]/tr');
    $dom = null;
    $xpath = null;
    $ch = null;
    unset($dom);
    unset($xpath);
    unset($ch);
    
    echo "Parsing results ...\n";
    $results = array();
    $n = $query->length;
    for ($i = 1; $i < $n; $i++) {
        $row = $query->item($i);
        preg_match('/filename=(.*?)">/i', $row->ownerDocument->saveXML($row), $href);
        @$result = array(
            'case_number' => trim($row->childNodes->item(1)->nodeValue),
            'path' => $href[1],
            'petitioner' => trim(substr($row->childNodes->item(2)->nodeValue, 0, strpos($row->childNodes->item(2)->nodeValue, ' Vs. '))),
            'respondent' => trim(substr($row->childNodes->item(2)->nodeValue, strpos($row->childNodes->item(2)->nodeValue, ' Vs. ')+5)),
            'judge' => trim(trim($row->childNodes->item(3)->nodeValue, 'Coram: ')),
            'judgment_date' => trim($row->childNodes->item(4)->nodeValue),
            'unique_id' => preg_replace('/\s+/', '', $row->childNodes->item(0)->nodeValue .'-'. $row->childNodes->item(1)->nodeValue .'-'. $from['day'].$from['month'].$from['year'] .'-'. $to['day'].$to['month'].$to['year'])
        );
        if ($result['case_number'] || $result['path'] || $result['petitioner'] || $result['respondent'] || $result['judgment_date']) {
            $new_last_row_number = intval($row->childNodes->item(0)->nodeValue);
            array_push($results, $result);
        }
    }
    
    scraperwiki::save_sqlite(array('unique_id'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    $query = null;
    $results = null;
    unset($query);
    unset($results);
    
    if (!isset($new_last_row_number)) $new_last_row_number = 0;
    if ($last_row_number !== $new_last_row_number) {
        scrape($cookie, $viewstate, $event_validation, $page+1, $from, $to, $new_last_row_number);
    }
}

$ch = curl_init();
curl_setopt_array($ch, array(
    CURLOPT_URL => 'http://judis.nic.in/Judis_Jammu/causetitle.aspx',
    CURLOPT_HEADER => true,
    CURLOPT_RETURNTRANSFER => true,
));
$data = curl_exec($ch);
curl_close($ch);
preg_match('/Set-Cookie: (.*)/i', $data, $cookie);
$cookie = substr($cookie[1], 0, strpos($cookie[1], ';'));
preg_match_all('/value="\/(.*)"/i', $data, $aspnet_vars);

for ($i = 6; $i > -1; $i = $i - 1) {  //Count from XX months ago
    $from = array(
        'day' => '01',                                 //date("d", strtotime("-30 days")),
        'month' => date("m", strtotime("-$i months")), //date("m", strtotime("-30 days")),
        'year' => date("Y", strtotime("-$i months"))   //date("Y", strtotime("-30 days"))
    );
    $to = array(
        'day' => date("t", strtotime("-$i months")),   //date("d"),
        'month' => date("m", strtotime("-$i months")), //date("m"),
        'year' => date("Y", strtotime("-$i months"))   //date("Y")
    );
    scrape($cookie, '/'.$aspnet_vars[1][0], '/'.$aspnet_vars[1][1], 0, $from, $to, -1);
}
?>