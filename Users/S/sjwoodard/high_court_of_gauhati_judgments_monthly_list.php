<?php
function scrape($month, $year) {

    echo "Loading data ($month $year) ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(ScraperWiki::scrape("http://ghconline.nic.in/JDMT$month$year.html"));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//table[@class="DISCOVERY3"]/tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 1; $i < $n; $i++) {
        $row = $query->item($i);
        if ($year == 10 || ( $year == 11 && $month == 'Jan')) {
            $subjects = preg_split('/VS/i', preg_replace('/\xC2\xA0/', ' ', $row->childNodes->item(4)->nodeValue));
            @$result = array(
                'unique_id' => preg_replace('/\s+/', '', $row->childNodes->item(0)->nodeValue .'-'. $month.$year .'-'. $row->childNodes->item(2)->nodeValue),
                'case_number' => $row->childNodes->item(2)->nodeValue,
                'judgment_date' => $month .'. '. preg_replace('/\D+/', '', $row->childNodes->item(0)->nodeValue) .' 20'. $year,
                'path' => ltrim($row->getElementsByTagName('a')->item(0)->getAttribute('href'), '.'),
                'petitioner' => trim($subjects[0]),
                'respondent' => trim($subjects[1]),
                'subject' => $row->childNodes->item(6)->nodeValue
            );
        } else {
            $subjects = preg_split('/VS/i', preg_replace('/\xC2\xA0/', ' ', $row->childNodes->item(3)->nodeValue));
            @$result = array(
                'unique_id' => preg_replace('/\s+/', '', $row->childNodes->item(0)->nodeValue .'-'. $month.$year .'-'. $row->childNodes->item(2)->nodeValue),
                'case_number' => $row->childNodes->item(2)->nodeValue,
                'judgment_date' => $month .'. '. preg_replace('/\D+/', '', $row->childNodes->item(1)->nodeValue) .' 20'. $year,
                'path' => ltrim($row->getElementsByTagName('a')->item(0)->getAttribute('href'), '.'),
                'petitioner' => trim($subjects[0]),
                'respondent' => trim($subjects[1]),
                'subject' => $row->childNodes->item(4)->nodeValue
            );
        }
        array_push($results, $result);
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

    //Final save to database
    $this_results = count($results);
    scraperwiki::save_sqlite(array('unique_id'), $results);
    $results = null;
    unset($results);
}

$months = array('Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec');

for ($year = date('y'); $year < (date('y') + 1); $year++) {
    foreach ($months as $month) {
        if ($year == 10) {
            if ($month == 'Apr') $month = 'Appr';
            if ($month == 'June') $month = 'Jun';
            if ($month == 'Aug') $month = 'August';
            if ($month == 'Sept') $month = 'September';
            if ($month == 'Oct') $month = 'October';
            if ($month == 'Nov') $month = 'November';
            if ($month == 'Dec') $month = 'December';
        }
        if ($year == 11) {
            if ($month == 'Aug') $month = 'August';
            if ($month == 'Oct') $month = 'October';
            if ($month == 'Nov') $month = 'November';
        }
        scrape($month, $year);
    }
}

?><?php
function scrape($month, $year) {

    echo "Loading data ($month $year) ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(ScraperWiki::scrape("http://ghconline.nic.in/JDMT$month$year.html"));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//table[@class="DISCOVERY3"]/tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 1; $i < $n; $i++) {
        $row = $query->item($i);
        if ($year == 10 || ( $year == 11 && $month == 'Jan')) {
            $subjects = preg_split('/VS/i', preg_replace('/\xC2\xA0/', ' ', $row->childNodes->item(4)->nodeValue));
            @$result = array(
                'unique_id' => preg_replace('/\s+/', '', $row->childNodes->item(0)->nodeValue .'-'. $month.$year .'-'. $row->childNodes->item(2)->nodeValue),
                'case_number' => $row->childNodes->item(2)->nodeValue,
                'judgment_date' => $month .'. '. preg_replace('/\D+/', '', $row->childNodes->item(0)->nodeValue) .' 20'. $year,
                'path' => ltrim($row->getElementsByTagName('a')->item(0)->getAttribute('href'), '.'),
                'petitioner' => trim($subjects[0]),
                'respondent' => trim($subjects[1]),
                'subject' => $row->childNodes->item(6)->nodeValue
            );
        } else {
            $subjects = preg_split('/VS/i', preg_replace('/\xC2\xA0/', ' ', $row->childNodes->item(3)->nodeValue));
            @$result = array(
                'unique_id' => preg_replace('/\s+/', '', $row->childNodes->item(0)->nodeValue .'-'. $month.$year .'-'. $row->childNodes->item(2)->nodeValue),
                'case_number' => $row->childNodes->item(2)->nodeValue,
                'judgment_date' => $month .'. '. preg_replace('/\D+/', '', $row->childNodes->item(1)->nodeValue) .' 20'. $year,
                'path' => ltrim($row->getElementsByTagName('a')->item(0)->getAttribute('href'), '.'),
                'petitioner' => trim($subjects[0]),
                'respondent' => trim($subjects[1]),
                'subject' => $row->childNodes->item(4)->nodeValue
            );
        }
        array_push($results, $result);
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

    //Final save to database
    $this_results = count($results);
    scraperwiki::save_sqlite(array('unique_id'), $results);
    $results = null;
    unset($results);
}

$months = array('Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec');

for ($year = date('y'); $year < (date('y') + 1); $year++) {
    foreach ($months as $month) {
        if ($year == 10) {
            if ($month == 'Apr') $month = 'Appr';
            if ($month == 'June') $month = 'Jun';
            if ($month == 'Aug') $month = 'August';
            if ($month == 'Sept') $month = 'September';
            if ($month == 'Oct') $month = 'October';
            if ($month == 'Nov') $month = 'November';
            if ($month == 'Dec') $month = 'December';
        }
        if ($year == 11) {
            if ($month == 'Aug') $month = 'August';
            if ($month == 'Oct') $month = 'October';
            if ($month == 'Nov') $month = 'November';
        }
        scrape($month, $year);
    }
}

?><?php
function scrape($month, $year) {

    echo "Loading data ($month $year) ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(ScraperWiki::scrape("http://ghconline.nic.in/JDMT$month$year.html"));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//table[@class="DISCOVERY3"]/tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 1; $i < $n; $i++) {
        $row = $query->item($i);
        if ($year == 10 || ( $year == 11 && $month == 'Jan')) {
            $subjects = preg_split('/VS/i', preg_replace('/\xC2\xA0/', ' ', $row->childNodes->item(4)->nodeValue));
            @$result = array(
                'unique_id' => preg_replace('/\s+/', '', $row->childNodes->item(0)->nodeValue .'-'. $month.$year .'-'. $row->childNodes->item(2)->nodeValue),
                'case_number' => $row->childNodes->item(2)->nodeValue,
                'judgment_date' => $month .'. '. preg_replace('/\D+/', '', $row->childNodes->item(0)->nodeValue) .' 20'. $year,
                'path' => ltrim($row->getElementsByTagName('a')->item(0)->getAttribute('href'), '.'),
                'petitioner' => trim($subjects[0]),
                'respondent' => trim($subjects[1]),
                'subject' => $row->childNodes->item(6)->nodeValue
            );
        } else {
            $subjects = preg_split('/VS/i', preg_replace('/\xC2\xA0/', ' ', $row->childNodes->item(3)->nodeValue));
            @$result = array(
                'unique_id' => preg_replace('/\s+/', '', $row->childNodes->item(0)->nodeValue .'-'. $month.$year .'-'. $row->childNodes->item(2)->nodeValue),
                'case_number' => $row->childNodes->item(2)->nodeValue,
                'judgment_date' => $month .'. '. preg_replace('/\D+/', '', $row->childNodes->item(1)->nodeValue) .' 20'. $year,
                'path' => ltrim($row->getElementsByTagName('a')->item(0)->getAttribute('href'), '.'),
                'petitioner' => trim($subjects[0]),
                'respondent' => trim($subjects[1]),
                'subject' => $row->childNodes->item(4)->nodeValue
            );
        }
        array_push($results, $result);
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

    //Final save to database
    $this_results = count($results);
    scraperwiki::save_sqlite(array('unique_id'), $results);
    $results = null;
    unset($results);
}

$months = array('Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec');

for ($year = date('y'); $year < (date('y') + 1); $year++) {
    foreach ($months as $month) {
        if ($year == 10) {
            if ($month == 'Apr') $month = 'Appr';
            if ($month == 'June') $month = 'Jun';
            if ($month == 'Aug') $month = 'August';
            if ($month == 'Sept') $month = 'September';
            if ($month == 'Oct') $month = 'October';
            if ($month == 'Nov') $month = 'November';
            if ($month == 'Dec') $month = 'December';
        }
        if ($year == 11) {
            if ($month == 'Aug') $month = 'August';
            if ($month == 'Oct') $month = 'October';
            if ($month == 'Nov') $month = 'November';
        }
        scrape($month, $year);
    }
}

?>