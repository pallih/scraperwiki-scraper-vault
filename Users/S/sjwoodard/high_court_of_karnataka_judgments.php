<?php
function scrape($offset) {
    echo "Loading data ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(file_get_contents('http://judgmenthck.kar.nic.in/judgments/browse?type=title&sort_by=1&order=DESC&rpp=1000&etal=-1&offset='. ($offset*1000)));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//table[@class="miscTable"]/tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 1; $i < $n; $i++) {
        $row = $query->item($i);
        preg_match('/href="(.*?)">/i', $row->ownerDocument->saveXML($row), $a);
        @$result = array(
            'judgment_date' => trim($row->childNodes->item(0)->nodeValue),
            'case_number'   => trim($row->childNodes->item(1)->nodeValue),
            'judge'         => trim($row->childNodes->item(2)->nodeValue),
            'petitioner'    => trim($row->childNodes->item(3)->nodeValue),
            'respondent'    => trim($row->childNodes->item(4)->nodeValue),
            'location'      => trim($row->childNodes->item(5)->nodeValue),
            'path'          => $a[1],
            'unique_id'     => preg_replace('/\D+/', '', $a[1]) .'-'. preg_replace('/\s+/', '', $row->childNodes->item(1)->nodeValue)
        );
        array_push($results, $result);
        if ($i % 100 === 0) {
            scraperwiki::save_sqlite(array('unique_id'), $results);
            $results = array();
        }
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

    //Save final remainder to database
    scraperwiki::save_sqlite(array('unique_id'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

for ($i = 0; $i < 10; $i++) {
    scrape($i);
}
?>
<?php
function scrape($offset) {
    echo "Loading data ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(file_get_contents('http://judgmenthck.kar.nic.in/judgments/browse?type=title&sort_by=1&order=DESC&rpp=1000&etal=-1&offset='. ($offset*1000)));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//table[@class="miscTable"]/tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 1; $i < $n; $i++) {
        $row = $query->item($i);
        preg_match('/href="(.*?)">/i', $row->ownerDocument->saveXML($row), $a);
        @$result = array(
            'judgment_date' => trim($row->childNodes->item(0)->nodeValue),
            'case_number'   => trim($row->childNodes->item(1)->nodeValue),
            'judge'         => trim($row->childNodes->item(2)->nodeValue),
            'petitioner'    => trim($row->childNodes->item(3)->nodeValue),
            'respondent'    => trim($row->childNodes->item(4)->nodeValue),
            'location'      => trim($row->childNodes->item(5)->nodeValue),
            'path'          => $a[1],
            'unique_id'     => preg_replace('/\D+/', '', $a[1]) .'-'. preg_replace('/\s+/', '', $row->childNodes->item(1)->nodeValue)
        );
        array_push($results, $result);
        if ($i % 100 === 0) {
            scraperwiki::save_sqlite(array('unique_id'), $results);
            $results = array();
        }
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

    //Save final remainder to database
    scraperwiki::save_sqlite(array('unique_id'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

for ($i = 0; $i < 10; $i++) {
    scrape($i);
}
?>
