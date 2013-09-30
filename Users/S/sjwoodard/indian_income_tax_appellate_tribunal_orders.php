<?php
header('Content-Type: application/json');

function scrape($session, $session_id, $zone, $bench, $appeal_date, $page) {
    echo "Loading data (page $page in $zone / $bench for date $appeal_date) ...\n";
    
    $header = array(
    'X-Prototype-Version: 1.4.0',
    'X-Requested-With: XMLHttpRequest',
    'SOAPAction: ""',
    'Content-type: application/x-www-form-urlencoded text/xml; charset=UTF-8',
    'request-type: SOAP',
    );
    $soap = '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><Body xmlns="http://schemas.xmlsoap.org/soap/envelope/"><GetUpdatedObjects xmlns="http://schemas.eclipse.org/birt"><Operation><Target><Id>Document</Id><Type>Document</Type></Target><Operator>GetPage</Operator><Oprand><Name>City</Name><Value>'. $bench .'</Value></Oprand><Oprand><Name>__isdisplay__City</Name><Value>'. $bench .'</Value></Oprand><Oprand><Name>Serial No</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Serial No</Name><Value></Value></Oprand><Oprand><Name>Appeal No</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Appeal No</Name><Value></Value></Oprand><Oprand><Name>Assessee Name</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Assessee Name</Name><Value></Value></Oprand><Oprand><Name>searchWhat</Name><Value>searchByDate</Value></Oprand><Oprand><Name>__isdisplay__searchWhat</Name><Value>searchByDate</Value></Oprand><Oprand><Name>Order Date</Name><Value>'. $appeal_date .'</Value></Oprand><Oprand><Name>__isdisplay__Order Date</Name><Value>'. $appeal_date .'</Value></Oprand><Oprand><Name>Member Name</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Member Name</Name><Value></Value></Oprand><Oprand><Name>Pronouncement Date</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Pronouncement Date</Name><Value></Value></Oprand><Oprand><Name>__page</Name><Value>'. $page .'</Value></Oprand><Oprand><Name>__svg</Name><Value>false</Value></Oprand><Oprand><Name>__page</Name><Value>'. $page .'</Value></Oprand><Oprand><Name>__taskid</Name><Value>'. $session_id .'</Value></Oprand></Operation></GetUpdatedObjects></Body></soap:Envelope>';
    
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://www.itatonline.in:8080/itat/jsp/runBirt2.jsp?subAction=showReoprt&__report=pronouncementOrderReport1_'. $zone .'.rptdesign&searchWhat=searchByDate&Serial%20No=&Appeal%20No=&Assessee%20Name=&AssType=null&appealDate='. $appeal_date .'&Bench='. $bench .'&__sessionId='. $session_id,
        CURLOPT_COOKIE => preg_replace('/Set-Cookie: /i', '', $session),
        CURLOPT_HTTPHEADER => $header,
        CURLOPT_POSTFIELDS => $soap, 
        CURLOPT_RETURNTRANSFER => true,
    ));
    $dom = new DOMDocument();
    @$dom->loadHTML('<html><body>'. htmlspecialchars_decode(curl_exec($ch)) .'</body></html>');
    $xpath = new DOMXPath($dom);
    $pages = $xpath->query('//updatedata/data/page');
    if ($pages->item(0)) {
        $results_page = intval($pages->item(0)->childNodes->item(0)->nodeValue);
    } else {
        echo 'No data found for '. $zone .' : '. $bench .' on '. $appeal_date ." ...\n";
        return false; //no data
    }
    $total_pages = intval($pages->item(0)->childNodes->item(1)->nodeValue);
    $query = $xpath->query('//tr[@class="style_10"]');
    curl_close($ch);
    $header = null;
    $soap = null;
    $xpath = null;
    $pages = null;
    $dom = null;
    $ch = null;
    unset($header);
    unset($soap);
    unset($xpath);
    unset($pages);
    unset($dom);
    unset($ch);
    
    echo "Parsing results ...\n";
    $results = array();
    $n = $query->length;
    for ($i = 0; $i < $n; $i++) {
        $row = $query->item($i);
        @$result = array(
            'appeal_number' => trim(preg_replace('/\xC2\xA0/', '', $row->childNodes->item(2)->nodeValue)),
            'path' => $row->getElementsByTagName('a')->item(0)->getAttribute('href'),
            'assessee_name' => trim($row->childNodes->item(4)->nodeValue),
            'filed_by' => trim($row->childNodes->item(6)->nodeValue),
            'order_date' => trim($row->childNodes->item(8)->nodeValue),
            'pronouncement_date' => trim($row->childNodes->item(10)->nodeValue),
            'zone' => $zone,
            'bench' => $bench,
        );
        if ($result['appeal_number']) array_push($results, $result);
    }

    scraperwiki::save_sqlite(array('appeal_number'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";

    $query = null;
    $results = null;
    unset($query);
    unset($results);

    if (($results_page+1) < $total_pages) {
        scrape($session, $session_id, $zone, $bench, $appeal_date, $results_page+1);
    }
}

$search_array = array(
    'DELHI' => array(
        'AGR', 'DEL',
    ),
    'AHMEDABAD' => array(
        'Ahd', 'Ind', 'Rjt',
    ),
    'MUMBAI' => array(
       'BIL', 'Mum', 'NAG', 'PAN', 'PUN',
    ),
    'CHENNAI' => array(
        'CHNY',
    ),
    'HYDERABAD' => array(
        'HYD', 'VIZ',
    ),
    'CHANDIGARH' => array(
        'ASR', 'CHANDI', 'JODH', 'JPR'
    ),
    'KOLKATA' => array(
        'CTK', 'GAU', 'Kol', 'PAT', 'Ran'
    ),
    'LUCKNOW' => array(
        'ALLD', 'JAB', 'LKW'
    ),
    'BENGLORE' => array(
        'Bang', 'COCH'
    ),
);

$dates = array(  //Search last 5 days
    date("d/m/Y", strtotime("-4 days")),
    date("d/m/Y", strtotime("-3 days")),
    date("d/m/Y", strtotime("-2 days")),
    date("d/m/Y", strtotime("-1 day")),
    date("d/m/Y")
);

foreach ($search_array as $zone => $benches) {
    foreach ($benches as $bench) {
        foreach ($dates as $appeal_date) {
            $ch = curl_init();
            curl_setopt_array($ch, array(
                CURLOPT_URL => 'http://www.itatonline.in:8080/itat/jsp/findPronouncement1.jsp?ID=&dbcontext='. $zone .'&city='. $bench .'&slNo=&appealNo=&assesseeName=&appealDate='. $appeal_date .'&subAction=newSearch&searchWhat=searchByDate&__report=pronouncementOrderReport1_'. $zone .'.rptdesign&forward=findPronouncement1',
                CURLOPT_RETURNTRANSFER => true,
                CURLOPT_HEADER => true,
                CURLOPT_NOBODY => true,
            ));
            preg_match('/^Set-Cookie:\s*([^;]*)/mi', curl_exec($ch), $session);
            curl_close($ch);

            $ch = curl_init();
            curl_setopt_array($ch, array(
                CURLOPT_URL => 'http://www.itatonline.in:8080/itat/jsp/runBirt2.jsp?'. urlencode('subAction=showReoprt&__report=pronouncementOrderReport1_'. $zone .'.rptdesign&searchWhat=searchByDate&Serial No=&Appeal No=&Assessee Name=&AssType=null&appealDate='. $appeal_date .'&Bench='. $bench),
                CURLOPT_COOKIE => preg_replace('/Set-Cookie: /i', '', $session[1]),
                CURLOPT_RETURNTRANSFER => true,
            ));
            preg_match('/Constants.viewingSessionId = "(.*)\";/i', curl_exec($ch), $session_id);
            curl_close($ch);
            $page = 1;
            scrape($session[1], $session_id[1], $zone, $bench, $appeal_date,  $page);
        }
    }
}
?><?php
header('Content-Type: application/json');

function scrape($session, $session_id, $zone, $bench, $appeal_date, $page) {
    echo "Loading data (page $page in $zone / $bench for date $appeal_date) ...\n";
    
    $header = array(
    'X-Prototype-Version: 1.4.0',
    'X-Requested-With: XMLHttpRequest',
    'SOAPAction: ""',
    'Content-type: application/x-www-form-urlencoded text/xml; charset=UTF-8',
    'request-type: SOAP',
    );
    $soap = '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><Body xmlns="http://schemas.xmlsoap.org/soap/envelope/"><GetUpdatedObjects xmlns="http://schemas.eclipse.org/birt"><Operation><Target><Id>Document</Id><Type>Document</Type></Target><Operator>GetPage</Operator><Oprand><Name>City</Name><Value>'. $bench .'</Value></Oprand><Oprand><Name>__isdisplay__City</Name><Value>'. $bench .'</Value></Oprand><Oprand><Name>Serial No</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Serial No</Name><Value></Value></Oprand><Oprand><Name>Appeal No</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Appeal No</Name><Value></Value></Oprand><Oprand><Name>Assessee Name</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Assessee Name</Name><Value></Value></Oprand><Oprand><Name>searchWhat</Name><Value>searchByDate</Value></Oprand><Oprand><Name>__isdisplay__searchWhat</Name><Value>searchByDate</Value></Oprand><Oprand><Name>Order Date</Name><Value>'. $appeal_date .'</Value></Oprand><Oprand><Name>__isdisplay__Order Date</Name><Value>'. $appeal_date .'</Value></Oprand><Oprand><Name>Member Name</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Member Name</Name><Value></Value></Oprand><Oprand><Name>Pronouncement Date</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Pronouncement Date</Name><Value></Value></Oprand><Oprand><Name>__page</Name><Value>'. $page .'</Value></Oprand><Oprand><Name>__svg</Name><Value>false</Value></Oprand><Oprand><Name>__page</Name><Value>'. $page .'</Value></Oprand><Oprand><Name>__taskid</Name><Value>'. $session_id .'</Value></Oprand></Operation></GetUpdatedObjects></Body></soap:Envelope>';
    
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://www.itatonline.in:8080/itat/jsp/runBirt2.jsp?subAction=showReoprt&__report=pronouncementOrderReport1_'. $zone .'.rptdesign&searchWhat=searchByDate&Serial%20No=&Appeal%20No=&Assessee%20Name=&AssType=null&appealDate='. $appeal_date .'&Bench='. $bench .'&__sessionId='. $session_id,
        CURLOPT_COOKIE => preg_replace('/Set-Cookie: /i', '', $session),
        CURLOPT_HTTPHEADER => $header,
        CURLOPT_POSTFIELDS => $soap, 
        CURLOPT_RETURNTRANSFER => true,
    ));
    $dom = new DOMDocument();
    @$dom->loadHTML('<html><body>'. htmlspecialchars_decode(curl_exec($ch)) .'</body></html>');
    $xpath = new DOMXPath($dom);
    $pages = $xpath->query('//updatedata/data/page');
    if ($pages->item(0)) {
        $results_page = intval($pages->item(0)->childNodes->item(0)->nodeValue);
    } else {
        echo 'No data found for '. $zone .' : '. $bench .' on '. $appeal_date ." ...\n";
        return false; //no data
    }
    $total_pages = intval($pages->item(0)->childNodes->item(1)->nodeValue);
    $query = $xpath->query('//tr[@class="style_10"]');
    curl_close($ch);
    $header = null;
    $soap = null;
    $xpath = null;
    $pages = null;
    $dom = null;
    $ch = null;
    unset($header);
    unset($soap);
    unset($xpath);
    unset($pages);
    unset($dom);
    unset($ch);
    
    echo "Parsing results ...\n";
    $results = array();
    $n = $query->length;
    for ($i = 0; $i < $n; $i++) {
        $row = $query->item($i);
        @$result = array(
            'appeal_number' => trim(preg_replace('/\xC2\xA0/', '', $row->childNodes->item(2)->nodeValue)),
            'path' => $row->getElementsByTagName('a')->item(0)->getAttribute('href'),
            'assessee_name' => trim($row->childNodes->item(4)->nodeValue),
            'filed_by' => trim($row->childNodes->item(6)->nodeValue),
            'order_date' => trim($row->childNodes->item(8)->nodeValue),
            'pronouncement_date' => trim($row->childNodes->item(10)->nodeValue),
            'zone' => $zone,
            'bench' => $bench,
        );
        if ($result['appeal_number']) array_push($results, $result);
    }

    scraperwiki::save_sqlite(array('appeal_number'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";

    $query = null;
    $results = null;
    unset($query);
    unset($results);

    if (($results_page+1) < $total_pages) {
        scrape($session, $session_id, $zone, $bench, $appeal_date, $results_page+1);
    }
}

$search_array = array(
    'DELHI' => array(
        'AGR', 'DEL',
    ),
    'AHMEDABAD' => array(
        'Ahd', 'Ind', 'Rjt',
    ),
    'MUMBAI' => array(
       'BIL', 'Mum', 'NAG', 'PAN', 'PUN',
    ),
    'CHENNAI' => array(
        'CHNY',
    ),
    'HYDERABAD' => array(
        'HYD', 'VIZ',
    ),
    'CHANDIGARH' => array(
        'ASR', 'CHANDI', 'JODH', 'JPR'
    ),
    'KOLKATA' => array(
        'CTK', 'GAU', 'Kol', 'PAT', 'Ran'
    ),
    'LUCKNOW' => array(
        'ALLD', 'JAB', 'LKW'
    ),
    'BENGLORE' => array(
        'Bang', 'COCH'
    ),
);

$dates = array(  //Search last 5 days
    date("d/m/Y", strtotime("-4 days")),
    date("d/m/Y", strtotime("-3 days")),
    date("d/m/Y", strtotime("-2 days")),
    date("d/m/Y", strtotime("-1 day")),
    date("d/m/Y")
);

foreach ($search_array as $zone => $benches) {
    foreach ($benches as $bench) {
        foreach ($dates as $appeal_date) {
            $ch = curl_init();
            curl_setopt_array($ch, array(
                CURLOPT_URL => 'http://www.itatonline.in:8080/itat/jsp/findPronouncement1.jsp?ID=&dbcontext='. $zone .'&city='. $bench .'&slNo=&appealNo=&assesseeName=&appealDate='. $appeal_date .'&subAction=newSearch&searchWhat=searchByDate&__report=pronouncementOrderReport1_'. $zone .'.rptdesign&forward=findPronouncement1',
                CURLOPT_RETURNTRANSFER => true,
                CURLOPT_HEADER => true,
                CURLOPT_NOBODY => true,
            ));
            preg_match('/^Set-Cookie:\s*([^;]*)/mi', curl_exec($ch), $session);
            curl_close($ch);

            $ch = curl_init();
            curl_setopt_array($ch, array(
                CURLOPT_URL => 'http://www.itatonline.in:8080/itat/jsp/runBirt2.jsp?'. urlencode('subAction=showReoprt&__report=pronouncementOrderReport1_'. $zone .'.rptdesign&searchWhat=searchByDate&Serial No=&Appeal No=&Assessee Name=&AssType=null&appealDate='. $appeal_date .'&Bench='. $bench),
                CURLOPT_COOKIE => preg_replace('/Set-Cookie: /i', '', $session[1]),
                CURLOPT_RETURNTRANSFER => true,
            ));
            preg_match('/Constants.viewingSessionId = "(.*)\";/i', curl_exec($ch), $session_id);
            curl_close($ch);
            $page = 1;
            scrape($session[1], $session_id[1], $zone, $bench, $appeal_date,  $page);
        }
    }
}
?><?php
header('Content-Type: application/json');

function scrape($session, $session_id, $zone, $bench, $appeal_date, $page) {
    echo "Loading data (page $page in $zone / $bench for date $appeal_date) ...\n";
    
    $header = array(
    'X-Prototype-Version: 1.4.0',
    'X-Requested-With: XMLHttpRequest',
    'SOAPAction: ""',
    'Content-type: application/x-www-form-urlencoded text/xml; charset=UTF-8',
    'request-type: SOAP',
    );
    $soap = '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><Body xmlns="http://schemas.xmlsoap.org/soap/envelope/"><GetUpdatedObjects xmlns="http://schemas.eclipse.org/birt"><Operation><Target><Id>Document</Id><Type>Document</Type></Target><Operator>GetPage</Operator><Oprand><Name>City</Name><Value>'. $bench .'</Value></Oprand><Oprand><Name>__isdisplay__City</Name><Value>'. $bench .'</Value></Oprand><Oprand><Name>Serial No</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Serial No</Name><Value></Value></Oprand><Oprand><Name>Appeal No</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Appeal No</Name><Value></Value></Oprand><Oprand><Name>Assessee Name</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Assessee Name</Name><Value></Value></Oprand><Oprand><Name>searchWhat</Name><Value>searchByDate</Value></Oprand><Oprand><Name>__isdisplay__searchWhat</Name><Value>searchByDate</Value></Oprand><Oprand><Name>Order Date</Name><Value>'. $appeal_date .'</Value></Oprand><Oprand><Name>__isdisplay__Order Date</Name><Value>'. $appeal_date .'</Value></Oprand><Oprand><Name>Member Name</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Member Name</Name><Value></Value></Oprand><Oprand><Name>Pronouncement Date</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Pronouncement Date</Name><Value></Value></Oprand><Oprand><Name>__page</Name><Value>'. $page .'</Value></Oprand><Oprand><Name>__svg</Name><Value>false</Value></Oprand><Oprand><Name>__page</Name><Value>'. $page .'</Value></Oprand><Oprand><Name>__taskid</Name><Value>'. $session_id .'</Value></Oprand></Operation></GetUpdatedObjects></Body></soap:Envelope>';
    
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://www.itatonline.in:8080/itat/jsp/runBirt2.jsp?subAction=showReoprt&__report=pronouncementOrderReport1_'. $zone .'.rptdesign&searchWhat=searchByDate&Serial%20No=&Appeal%20No=&Assessee%20Name=&AssType=null&appealDate='. $appeal_date .'&Bench='. $bench .'&__sessionId='. $session_id,
        CURLOPT_COOKIE => preg_replace('/Set-Cookie: /i', '', $session),
        CURLOPT_HTTPHEADER => $header,
        CURLOPT_POSTFIELDS => $soap, 
        CURLOPT_RETURNTRANSFER => true,
    ));
    $dom = new DOMDocument();
    @$dom->loadHTML('<html><body>'. htmlspecialchars_decode(curl_exec($ch)) .'</body></html>');
    $xpath = new DOMXPath($dom);
    $pages = $xpath->query('//updatedata/data/page');
    if ($pages->item(0)) {
        $results_page = intval($pages->item(0)->childNodes->item(0)->nodeValue);
    } else {
        echo 'No data found for '. $zone .' : '. $bench .' on '. $appeal_date ." ...\n";
        return false; //no data
    }
    $total_pages = intval($pages->item(0)->childNodes->item(1)->nodeValue);
    $query = $xpath->query('//tr[@class="style_10"]');
    curl_close($ch);
    $header = null;
    $soap = null;
    $xpath = null;
    $pages = null;
    $dom = null;
    $ch = null;
    unset($header);
    unset($soap);
    unset($xpath);
    unset($pages);
    unset($dom);
    unset($ch);
    
    echo "Parsing results ...\n";
    $results = array();
    $n = $query->length;
    for ($i = 0; $i < $n; $i++) {
        $row = $query->item($i);
        @$result = array(
            'appeal_number' => trim(preg_replace('/\xC2\xA0/', '', $row->childNodes->item(2)->nodeValue)),
            'path' => $row->getElementsByTagName('a')->item(0)->getAttribute('href'),
            'assessee_name' => trim($row->childNodes->item(4)->nodeValue),
            'filed_by' => trim($row->childNodes->item(6)->nodeValue),
            'order_date' => trim($row->childNodes->item(8)->nodeValue),
            'pronouncement_date' => trim($row->childNodes->item(10)->nodeValue),
            'zone' => $zone,
            'bench' => $bench,
        );
        if ($result['appeal_number']) array_push($results, $result);
    }

    scraperwiki::save_sqlite(array('appeal_number'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";

    $query = null;
    $results = null;
    unset($query);
    unset($results);

    if (($results_page+1) < $total_pages) {
        scrape($session, $session_id, $zone, $bench, $appeal_date, $results_page+1);
    }
}

$search_array = array(
    'DELHI' => array(
        'AGR', 'DEL',
    ),
    'AHMEDABAD' => array(
        'Ahd', 'Ind', 'Rjt',
    ),
    'MUMBAI' => array(
       'BIL', 'Mum', 'NAG', 'PAN', 'PUN',
    ),
    'CHENNAI' => array(
        'CHNY',
    ),
    'HYDERABAD' => array(
        'HYD', 'VIZ',
    ),
    'CHANDIGARH' => array(
        'ASR', 'CHANDI', 'JODH', 'JPR'
    ),
    'KOLKATA' => array(
        'CTK', 'GAU', 'Kol', 'PAT', 'Ran'
    ),
    'LUCKNOW' => array(
        'ALLD', 'JAB', 'LKW'
    ),
    'BENGLORE' => array(
        'Bang', 'COCH'
    ),
);

$dates = array(  //Search last 5 days
    date("d/m/Y", strtotime("-4 days")),
    date("d/m/Y", strtotime("-3 days")),
    date("d/m/Y", strtotime("-2 days")),
    date("d/m/Y", strtotime("-1 day")),
    date("d/m/Y")
);

foreach ($search_array as $zone => $benches) {
    foreach ($benches as $bench) {
        foreach ($dates as $appeal_date) {
            $ch = curl_init();
            curl_setopt_array($ch, array(
                CURLOPT_URL => 'http://www.itatonline.in:8080/itat/jsp/findPronouncement1.jsp?ID=&dbcontext='. $zone .'&city='. $bench .'&slNo=&appealNo=&assesseeName=&appealDate='. $appeal_date .'&subAction=newSearch&searchWhat=searchByDate&__report=pronouncementOrderReport1_'. $zone .'.rptdesign&forward=findPronouncement1',
                CURLOPT_RETURNTRANSFER => true,
                CURLOPT_HEADER => true,
                CURLOPT_NOBODY => true,
            ));
            preg_match('/^Set-Cookie:\s*([^;]*)/mi', curl_exec($ch), $session);
            curl_close($ch);

            $ch = curl_init();
            curl_setopt_array($ch, array(
                CURLOPT_URL => 'http://www.itatonline.in:8080/itat/jsp/runBirt2.jsp?'. urlencode('subAction=showReoprt&__report=pronouncementOrderReport1_'. $zone .'.rptdesign&searchWhat=searchByDate&Serial No=&Appeal No=&Assessee Name=&AssType=null&appealDate='. $appeal_date .'&Bench='. $bench),
                CURLOPT_COOKIE => preg_replace('/Set-Cookie: /i', '', $session[1]),
                CURLOPT_RETURNTRANSFER => true,
            ));
            preg_match('/Constants.viewingSessionId = "(.*)\";/i', curl_exec($ch), $session_id);
            curl_close($ch);
            $page = 1;
            scrape($session[1], $session_id[1], $zone, $bench, $appeal_date,  $page);
        }
    }
}
?><?php
header('Content-Type: application/json');

function scrape($session, $session_id, $zone, $bench, $appeal_date, $page) {
    echo "Loading data (page $page in $zone / $bench for date $appeal_date) ...\n";
    
    $header = array(
    'X-Prototype-Version: 1.4.0',
    'X-Requested-With: XMLHttpRequest',
    'SOAPAction: ""',
    'Content-type: application/x-www-form-urlencoded text/xml; charset=UTF-8',
    'request-type: SOAP',
    );
    $soap = '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><Body xmlns="http://schemas.xmlsoap.org/soap/envelope/"><GetUpdatedObjects xmlns="http://schemas.eclipse.org/birt"><Operation><Target><Id>Document</Id><Type>Document</Type></Target><Operator>GetPage</Operator><Oprand><Name>City</Name><Value>'. $bench .'</Value></Oprand><Oprand><Name>__isdisplay__City</Name><Value>'. $bench .'</Value></Oprand><Oprand><Name>Serial No</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Serial No</Name><Value></Value></Oprand><Oprand><Name>Appeal No</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Appeal No</Name><Value></Value></Oprand><Oprand><Name>Assessee Name</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Assessee Name</Name><Value></Value></Oprand><Oprand><Name>searchWhat</Name><Value>searchByDate</Value></Oprand><Oprand><Name>__isdisplay__searchWhat</Name><Value>searchByDate</Value></Oprand><Oprand><Name>Order Date</Name><Value>'. $appeal_date .'</Value></Oprand><Oprand><Name>__isdisplay__Order Date</Name><Value>'. $appeal_date .'</Value></Oprand><Oprand><Name>Member Name</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Member Name</Name><Value></Value></Oprand><Oprand><Name>Pronouncement Date</Name><Value></Value></Oprand><Oprand><Name>__isdisplay__Pronouncement Date</Name><Value></Value></Oprand><Oprand><Name>__page</Name><Value>'. $page .'</Value></Oprand><Oprand><Name>__svg</Name><Value>false</Value></Oprand><Oprand><Name>__page</Name><Value>'. $page .'</Value></Oprand><Oprand><Name>__taskid</Name><Value>'. $session_id .'</Value></Oprand></Operation></GetUpdatedObjects></Body></soap:Envelope>';
    
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://www.itatonline.in:8080/itat/jsp/runBirt2.jsp?subAction=showReoprt&__report=pronouncementOrderReport1_'. $zone .'.rptdesign&searchWhat=searchByDate&Serial%20No=&Appeal%20No=&Assessee%20Name=&AssType=null&appealDate='. $appeal_date .'&Bench='. $bench .'&__sessionId='. $session_id,
        CURLOPT_COOKIE => preg_replace('/Set-Cookie: /i', '', $session),
        CURLOPT_HTTPHEADER => $header,
        CURLOPT_POSTFIELDS => $soap, 
        CURLOPT_RETURNTRANSFER => true,
    ));
    $dom = new DOMDocument();
    @$dom->loadHTML('<html><body>'. htmlspecialchars_decode(curl_exec($ch)) .'</body></html>');
    $xpath = new DOMXPath($dom);
    $pages = $xpath->query('//updatedata/data/page');
    if ($pages->item(0)) {
        $results_page = intval($pages->item(0)->childNodes->item(0)->nodeValue);
    } else {
        echo 'No data found for '. $zone .' : '. $bench .' on '. $appeal_date ." ...\n";
        return false; //no data
    }
    $total_pages = intval($pages->item(0)->childNodes->item(1)->nodeValue);
    $query = $xpath->query('//tr[@class="style_10"]');
    curl_close($ch);
    $header = null;
    $soap = null;
    $xpath = null;
    $pages = null;
    $dom = null;
    $ch = null;
    unset($header);
    unset($soap);
    unset($xpath);
    unset($pages);
    unset($dom);
    unset($ch);
    
    echo "Parsing results ...\n";
    $results = array();
    $n = $query->length;
    for ($i = 0; $i < $n; $i++) {
        $row = $query->item($i);
        @$result = array(
            'appeal_number' => trim(preg_replace('/\xC2\xA0/', '', $row->childNodes->item(2)->nodeValue)),
            'path' => $row->getElementsByTagName('a')->item(0)->getAttribute('href'),
            'assessee_name' => trim($row->childNodes->item(4)->nodeValue),
            'filed_by' => trim($row->childNodes->item(6)->nodeValue),
            'order_date' => trim($row->childNodes->item(8)->nodeValue),
            'pronouncement_date' => trim($row->childNodes->item(10)->nodeValue),
            'zone' => $zone,
            'bench' => $bench,
        );
        if ($result['appeal_number']) array_push($results, $result);
    }

    scraperwiki::save_sqlite(array('appeal_number'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";

    $query = null;
    $results = null;
    unset($query);
    unset($results);

    if (($results_page+1) < $total_pages) {
        scrape($session, $session_id, $zone, $bench, $appeal_date, $results_page+1);
    }
}

$search_array = array(
    'DELHI' => array(
        'AGR', 'DEL',
    ),
    'AHMEDABAD' => array(
        'Ahd', 'Ind', 'Rjt',
    ),
    'MUMBAI' => array(
       'BIL', 'Mum', 'NAG', 'PAN', 'PUN',
    ),
    'CHENNAI' => array(
        'CHNY',
    ),
    'HYDERABAD' => array(
        'HYD', 'VIZ',
    ),
    'CHANDIGARH' => array(
        'ASR', 'CHANDI', 'JODH', 'JPR'
    ),
    'KOLKATA' => array(
        'CTK', 'GAU', 'Kol', 'PAT', 'Ran'
    ),
    'LUCKNOW' => array(
        'ALLD', 'JAB', 'LKW'
    ),
    'BENGLORE' => array(
        'Bang', 'COCH'
    ),
);

$dates = array(  //Search last 5 days
    date("d/m/Y", strtotime("-4 days")),
    date("d/m/Y", strtotime("-3 days")),
    date("d/m/Y", strtotime("-2 days")),
    date("d/m/Y", strtotime("-1 day")),
    date("d/m/Y")
);

foreach ($search_array as $zone => $benches) {
    foreach ($benches as $bench) {
        foreach ($dates as $appeal_date) {
            $ch = curl_init();
            curl_setopt_array($ch, array(
                CURLOPT_URL => 'http://www.itatonline.in:8080/itat/jsp/findPronouncement1.jsp?ID=&dbcontext='. $zone .'&city='. $bench .'&slNo=&appealNo=&assesseeName=&appealDate='. $appeal_date .'&subAction=newSearch&searchWhat=searchByDate&__report=pronouncementOrderReport1_'. $zone .'.rptdesign&forward=findPronouncement1',
                CURLOPT_RETURNTRANSFER => true,
                CURLOPT_HEADER => true,
                CURLOPT_NOBODY => true,
            ));
            preg_match('/^Set-Cookie:\s*([^;]*)/mi', curl_exec($ch), $session);
            curl_close($ch);

            $ch = curl_init();
            curl_setopt_array($ch, array(
                CURLOPT_URL => 'http://www.itatonline.in:8080/itat/jsp/runBirt2.jsp?'. urlencode('subAction=showReoprt&__report=pronouncementOrderReport1_'. $zone .'.rptdesign&searchWhat=searchByDate&Serial No=&Appeal No=&Assessee Name=&AssType=null&appealDate='. $appeal_date .'&Bench='. $bench),
                CURLOPT_COOKIE => preg_replace('/Set-Cookie: /i', '', $session[1]),
                CURLOPT_RETURNTRANSFER => true,
            ));
            preg_match('/Constants.viewingSessionId = "(.*)\";/i', curl_exec($ch), $session_id);
            curl_close($ch);
            $page = 1;
            scrape($session[1], $session_id[1], $zone, $bench, $appeal_date,  $page);
        }
    }
}
?>