<?php
//ASP.Net gives unique credentials when first running a query. Therefore, the script needed to acces the first page
//is more intensive than the script for all other pages. 

function first_page($cookie, $viewstate, $event_validation, $from, $to) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://judis.nic.in/judis_chennai/causetitle.aspx',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_COOKIE => $cookie,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => http_build_query(array(
            '__VIEWSTATE' => $viewstate,
            '__EVENTVALIDATION' => $event_validation,
            'txttitle' => '_',
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

function not_first_page($cookie, $viewstate, $event_validation, $this_page_code) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://judis.nic.in/judis_chennai/Chrseq.aspx',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_COOKIE => $cookie,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => http_build_query(array(
            '__VIEWSTATE' => $viewstate,
            '__EVENTVALIDATION' => $event_validation,
            '__EVENTTARGET' => 'DataGrid1$ctl19$ctl'. $this_page_code,
            '__EVENTARGUMENT' => '',
        )),
    ));
    $data = curl_exec($ch);
    curl_close($ch);
    $ch = null;
    unset($ch);
    return $data;
}

function scrape($cookie, $viewstate, $event_validation, $page, $this_page_code, $prev_last_result_id, $from, $to) {
    echo "Loading data (". $from['day'] .'/'. $from['month'] .'/'. $from['year'] .' -> '. $to['day'] .'/'. $to['month'] .'/'. $to['year'] .") ...\n";
    $dom = new DOMDocument();
    if ($page == 1) {
        @$dom->loadHTML(first_page($cookie, $viewstate, $event_validation, $from, $to));
    } else {
        @$dom->loadHTML(not_first_page($cookie, $viewstate, $event_validation, $this_page_code));
        //When page number hits 25/50/75/etc..., the website strangely starts counting over from 1 again (i.e. page 1 can be page 26/51/76.
        //And if there's more than 25 pages, but less than 50, the page numbering can move around randomly.
    }
    $xpath = new DOMXPath($dom);
    $viewstate = $xpath->query('//*[@id="__VIEWSTATE"]')->item(0)->getAttribute('value');
    $event_validation = $xpath->query('//*[@id="__EVENTVALIDATION"]');
    if ($event_validation->length) $event_validation = $event_validation->item(0)->getAttribute('value');
    if ($page == 25) {
        $next_page_code = '25';
    } elseif ($page % 25 === 0) {
        $next_page_code = '26';
    } elseif ($page < 25) {
        $next_page_code = sprintf("%02s", $page);
    } else {
        foreach ($xpath->query('//td[@colspan="5"]/font/a') as $a) {
            if (intval($a->nodeValue) == $page+1) {
                preg_match('/\$ctl19\$ctl(.*?)\'/i', $a->getAttribute('href'), $asp_page_id);
                $next_page_code = $asp_page_id[1];
            }
        }
    }

    $query = $xpath->query('//table[@id="DataGrid1"]/tr');
    $dom = null;
    $xpath = null;
    $ch = null;
    unset($dom);
    unset($xpath);
    unset($ch);
    
    echo "Parsing results ...\n";
    $results = array();
    $last_result_id = -1;
    $n = $query->length;
    for ($i = 1; $i < ($n-1); $i++) {
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
        if ($result['case_number'] || $result['path'] || $result['petitioner'] || $result['respondent'] || $result['judgment_date']) array_push($results, $result);
        $last_result_id = intval($row->childNodes->item(0)->nodeValue);
    }
    scraperwiki::save_sqlite(array('unique_id'), $results);
    $results_count = count($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    $query = null;
    $results = null;
    unset($query);
    unset($results);
    
    if ($prev_last_result_id != $last_result_id) {
        @scrape($cookie, $viewstate, $event_validation, $page+1, $next_page_code, $last_result_id, $from, $to);
    }
}

$ch = curl_init();
curl_setopt_array($ch, array(
    CURLOPT_URL => 'http://judis.nic.in/judis_chennai/causetitle.aspx',
    CURLOPT_HEADER => true,
    CURLOPT_RETURNTRANSFER => true,
));
$data = curl_exec($ch);
curl_close($ch);
preg_match('/Set-Cookie: (.*)/i', $data, $cookie);
$cookie = substr($cookie[1], 0, strpos($cookie[1], ';'));
preg_match_all('/value="\/(.*)"/i', $data, $aspnet_vars);

for ($i = 3; $i > -1; $i = $i - 1) { //Count from XXX months ago
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
    scrape($cookie, '/'.$aspnet_vars[1][0], '/'.$aspnet_vars[1][1], 1, '00', -1, $from, $to);
}
?><?php
//ASP.Net gives unique credentials when first running a query. Therefore, the script needed to acces the first page
//is more intensive than the script for all other pages. 

function first_page($cookie, $viewstate, $event_validation, $from, $to) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://judis.nic.in/judis_chennai/causetitle.aspx',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_COOKIE => $cookie,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => http_build_query(array(
            '__VIEWSTATE' => $viewstate,
            '__EVENTVALIDATION' => $event_validation,
            'txttitle' => '_',
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

function not_first_page($cookie, $viewstate, $event_validation, $this_page_code) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://judis.nic.in/judis_chennai/Chrseq.aspx',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_COOKIE => $cookie,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => http_build_query(array(
            '__VIEWSTATE' => $viewstate,
            '__EVENTVALIDATION' => $event_validation,
            '__EVENTTARGET' => 'DataGrid1$ctl19$ctl'. $this_page_code,
            '__EVENTARGUMENT' => '',
        )),
    ));
    $data = curl_exec($ch);
    curl_close($ch);
    $ch = null;
    unset($ch);
    return $data;
}

function scrape($cookie, $viewstate, $event_validation, $page, $this_page_code, $prev_last_result_id, $from, $to) {
    echo "Loading data (". $from['day'] .'/'. $from['month'] .'/'. $from['year'] .' -> '. $to['day'] .'/'. $to['month'] .'/'. $to['year'] .") ...\n";
    $dom = new DOMDocument();
    if ($page == 1) {
        @$dom->loadHTML(first_page($cookie, $viewstate, $event_validation, $from, $to));
    } else {
        @$dom->loadHTML(not_first_page($cookie, $viewstate, $event_validation, $this_page_code));
        //When page number hits 25/50/75/etc..., the website strangely starts counting over from 1 again (i.e. page 1 can be page 26/51/76.
        //And if there's more than 25 pages, but less than 50, the page numbering can move around randomly.
    }
    $xpath = new DOMXPath($dom);
    $viewstate = $xpath->query('//*[@id="__VIEWSTATE"]')->item(0)->getAttribute('value');
    $event_validation = $xpath->query('//*[@id="__EVENTVALIDATION"]');
    if ($event_validation->length) $event_validation = $event_validation->item(0)->getAttribute('value');
    if ($page == 25) {
        $next_page_code = '25';
    } elseif ($page % 25 === 0) {
        $next_page_code = '26';
    } elseif ($page < 25) {
        $next_page_code = sprintf("%02s", $page);
    } else {
        foreach ($xpath->query('//td[@colspan="5"]/font/a') as $a) {
            if (intval($a->nodeValue) == $page+1) {
                preg_match('/\$ctl19\$ctl(.*?)\'/i', $a->getAttribute('href'), $asp_page_id);
                $next_page_code = $asp_page_id[1];
            }
        }
    }

    $query = $xpath->query('//table[@id="DataGrid1"]/tr');
    $dom = null;
    $xpath = null;
    $ch = null;
    unset($dom);
    unset($xpath);
    unset($ch);
    
    echo "Parsing results ...\n";
    $results = array();
    $last_result_id = -1;
    $n = $query->length;
    for ($i = 1; $i < ($n-1); $i++) {
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
        if ($result['case_number'] || $result['path'] || $result['petitioner'] || $result['respondent'] || $result['judgment_date']) array_push($results, $result);
        $last_result_id = intval($row->childNodes->item(0)->nodeValue);
    }
    scraperwiki::save_sqlite(array('unique_id'), $results);
    $results_count = count($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    $query = null;
    $results = null;
    unset($query);
    unset($results);
    
    if ($prev_last_result_id != $last_result_id) {
        @scrape($cookie, $viewstate, $event_validation, $page+1, $next_page_code, $last_result_id, $from, $to);
    }
}

$ch = curl_init();
curl_setopt_array($ch, array(
    CURLOPT_URL => 'http://judis.nic.in/judis_chennai/causetitle.aspx',
    CURLOPT_HEADER => true,
    CURLOPT_RETURNTRANSFER => true,
));
$data = curl_exec($ch);
curl_close($ch);
preg_match('/Set-Cookie: (.*)/i', $data, $cookie);
$cookie = substr($cookie[1], 0, strpos($cookie[1], ';'));
preg_match_all('/value="\/(.*)"/i', $data, $aspnet_vars);

for ($i = 3; $i > -1; $i = $i - 1) { //Count from XXX months ago
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
    scrape($cookie, '/'.$aspnet_vars[1][0], '/'.$aspnet_vars[1][1], 1, '00', -1, $from, $to);
}
?><?php
//ASP.Net gives unique credentials when first running a query. Therefore, the script needed to acces the first page
//is more intensive than the script for all other pages. 

function first_page($cookie, $viewstate, $event_validation, $from, $to) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://judis.nic.in/judis_chennai/causetitle.aspx',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_COOKIE => $cookie,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => http_build_query(array(
            '__VIEWSTATE' => $viewstate,
            '__EVENTVALIDATION' => $event_validation,
            'txttitle' => '_',
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

function not_first_page($cookie, $viewstate, $event_validation, $this_page_code) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://judis.nic.in/judis_chennai/Chrseq.aspx',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_COOKIE => $cookie,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => http_build_query(array(
            '__VIEWSTATE' => $viewstate,
            '__EVENTVALIDATION' => $event_validation,
            '__EVENTTARGET' => 'DataGrid1$ctl19$ctl'. $this_page_code,
            '__EVENTARGUMENT' => '',
        )),
    ));
    $data = curl_exec($ch);
    curl_close($ch);
    $ch = null;
    unset($ch);
    return $data;
}

function scrape($cookie, $viewstate, $event_validation, $page, $this_page_code, $prev_last_result_id, $from, $to) {
    echo "Loading data (". $from['day'] .'/'. $from['month'] .'/'. $from['year'] .' -> '. $to['day'] .'/'. $to['month'] .'/'. $to['year'] .") ...\n";
    $dom = new DOMDocument();
    if ($page == 1) {
        @$dom->loadHTML(first_page($cookie, $viewstate, $event_validation, $from, $to));
    } else {
        @$dom->loadHTML(not_first_page($cookie, $viewstate, $event_validation, $this_page_code));
        //When page number hits 25/50/75/etc..., the website strangely starts counting over from 1 again (i.e. page 1 can be page 26/51/76.
        //And if there's more than 25 pages, but less than 50, the page numbering can move around randomly.
    }
    $xpath = new DOMXPath($dom);
    $viewstate = $xpath->query('//*[@id="__VIEWSTATE"]')->item(0)->getAttribute('value');
    $event_validation = $xpath->query('//*[@id="__EVENTVALIDATION"]');
    if ($event_validation->length) $event_validation = $event_validation->item(0)->getAttribute('value');
    if ($page == 25) {
        $next_page_code = '25';
    } elseif ($page % 25 === 0) {
        $next_page_code = '26';
    } elseif ($page < 25) {
        $next_page_code = sprintf("%02s", $page);
    } else {
        foreach ($xpath->query('//td[@colspan="5"]/font/a') as $a) {
            if (intval($a->nodeValue) == $page+1) {
                preg_match('/\$ctl19\$ctl(.*?)\'/i', $a->getAttribute('href'), $asp_page_id);
                $next_page_code = $asp_page_id[1];
            }
        }
    }

    $query = $xpath->query('//table[@id="DataGrid1"]/tr');
    $dom = null;
    $xpath = null;
    $ch = null;
    unset($dom);
    unset($xpath);
    unset($ch);
    
    echo "Parsing results ...\n";
    $results = array();
    $last_result_id = -1;
    $n = $query->length;
    for ($i = 1; $i < ($n-1); $i++) {
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
        if ($result['case_number'] || $result['path'] || $result['petitioner'] || $result['respondent'] || $result['judgment_date']) array_push($results, $result);
        $last_result_id = intval($row->childNodes->item(0)->nodeValue);
    }
    scraperwiki::save_sqlite(array('unique_id'), $results);
    $results_count = count($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    $query = null;
    $results = null;
    unset($query);
    unset($results);
    
    if ($prev_last_result_id != $last_result_id) {
        @scrape($cookie, $viewstate, $event_validation, $page+1, $next_page_code, $last_result_id, $from, $to);
    }
}

$ch = curl_init();
curl_setopt_array($ch, array(
    CURLOPT_URL => 'http://judis.nic.in/judis_chennai/causetitle.aspx',
    CURLOPT_HEADER => true,
    CURLOPT_RETURNTRANSFER => true,
));
$data = curl_exec($ch);
curl_close($ch);
preg_match('/Set-Cookie: (.*)/i', $data, $cookie);
$cookie = substr($cookie[1], 0, strpos($cookie[1], ';'));
preg_match_all('/value="\/(.*)"/i', $data, $aspnet_vars);

for ($i = 3; $i > -1; $i = $i - 1) { //Count from XXX months ago
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
    scrape($cookie, '/'.$aspnet_vars[1][0], '/'.$aspnet_vars[1][1], 1, '00', -1, $from, $to);
}
?><?php
//ASP.Net gives unique credentials when first running a query. Therefore, the script needed to acces the first page
//is more intensive than the script for all other pages. 

function first_page($cookie, $viewstate, $event_validation, $from, $to) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://judis.nic.in/judis_chennai/causetitle.aspx',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_COOKIE => $cookie,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => http_build_query(array(
            '__VIEWSTATE' => $viewstate,
            '__EVENTVALIDATION' => $event_validation,
            'txttitle' => '_',
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

function not_first_page($cookie, $viewstate, $event_validation, $this_page_code) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://judis.nic.in/judis_chennai/Chrseq.aspx',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_COOKIE => $cookie,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => http_build_query(array(
            '__VIEWSTATE' => $viewstate,
            '__EVENTVALIDATION' => $event_validation,
            '__EVENTTARGET' => 'DataGrid1$ctl19$ctl'. $this_page_code,
            '__EVENTARGUMENT' => '',
        )),
    ));
    $data = curl_exec($ch);
    curl_close($ch);
    $ch = null;
    unset($ch);
    return $data;
}

function scrape($cookie, $viewstate, $event_validation, $page, $this_page_code, $prev_last_result_id, $from, $to) {
    echo "Loading data (". $from['day'] .'/'. $from['month'] .'/'. $from['year'] .' -> '. $to['day'] .'/'. $to['month'] .'/'. $to['year'] .") ...\n";
    $dom = new DOMDocument();
    if ($page == 1) {
        @$dom->loadHTML(first_page($cookie, $viewstate, $event_validation, $from, $to));
    } else {
        @$dom->loadHTML(not_first_page($cookie, $viewstate, $event_validation, $this_page_code));
        //When page number hits 25/50/75/etc..., the website strangely starts counting over from 1 again (i.e. page 1 can be page 26/51/76.
        //And if there's more than 25 pages, but less than 50, the page numbering can move around randomly.
    }
    $xpath = new DOMXPath($dom);
    $viewstate = $xpath->query('//*[@id="__VIEWSTATE"]')->item(0)->getAttribute('value');
    $event_validation = $xpath->query('//*[@id="__EVENTVALIDATION"]');
    if ($event_validation->length) $event_validation = $event_validation->item(0)->getAttribute('value');
    if ($page == 25) {
        $next_page_code = '25';
    } elseif ($page % 25 === 0) {
        $next_page_code = '26';
    } elseif ($page < 25) {
        $next_page_code = sprintf("%02s", $page);
    } else {
        foreach ($xpath->query('//td[@colspan="5"]/font/a') as $a) {
            if (intval($a->nodeValue) == $page+1) {
                preg_match('/\$ctl19\$ctl(.*?)\'/i', $a->getAttribute('href'), $asp_page_id);
                $next_page_code = $asp_page_id[1];
            }
        }
    }

    $query = $xpath->query('//table[@id="DataGrid1"]/tr');
    $dom = null;
    $xpath = null;
    $ch = null;
    unset($dom);
    unset($xpath);
    unset($ch);
    
    echo "Parsing results ...\n";
    $results = array();
    $last_result_id = -1;
    $n = $query->length;
    for ($i = 1; $i < ($n-1); $i++) {
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
        if ($result['case_number'] || $result['path'] || $result['petitioner'] || $result['respondent'] || $result['judgment_date']) array_push($results, $result);
        $last_result_id = intval($row->childNodes->item(0)->nodeValue);
    }
    scraperwiki::save_sqlite(array('unique_id'), $results);
    $results_count = count($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    $query = null;
    $results = null;
    unset($query);
    unset($results);
    
    if ($prev_last_result_id != $last_result_id) {
        @scrape($cookie, $viewstate, $event_validation, $page+1, $next_page_code, $last_result_id, $from, $to);
    }
}

$ch = curl_init();
curl_setopt_array($ch, array(
    CURLOPT_URL => 'http://judis.nic.in/judis_chennai/causetitle.aspx',
    CURLOPT_HEADER => true,
    CURLOPT_RETURNTRANSFER => true,
));
$data = curl_exec($ch);
curl_close($ch);
preg_match('/Set-Cookie: (.*)/i', $data, $cookie);
$cookie = substr($cookie[1], 0, strpos($cookie[1], ';'));
preg_match_all('/value="\/(.*)"/i', $data, $aspnet_vars);

for ($i = 3; $i > -1; $i = $i - 1) { //Count from XXX months ago
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
    scrape($cookie, '/'.$aspnet_vars[1][0], '/'.$aspnet_vars[1][1], 1, '00', -1, $from, $to);
}
?>