<?php
function scrape($page) {
    echo "Loading page ($page.html) ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(
        scraperwiki::scrape("http://www.fca.org.uk/static/alerts/internet/$page.html")
    );
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//*[@id="table"]/tbody/tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $row = $query->item($i);
        if ($row->getElementsByTagName('a')->item(0)) {
            $url = $row->getElementsByTagName('a')->item(0)->getAttribute('href');
        } else {
            $url = null;
        }
        array_push($results, @$result = array(
            'name' => trim($row->childNodes->item(0)->nodeValue),
            'url' => $url
        ));
        if ($result['name'] == 'There are currently no firms listed under this section.') {
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
    scraperwiki::save_sqlite(array('name'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

$pages = array('0-9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z');
foreach($pages as $page) {
    scrape($page);
}
?><?php
function scrape($page) {
    echo "Loading page ($page.html) ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(
        scraperwiki::scrape("http://www.fca.org.uk/static/alerts/internet/$page.html")
    );
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//*[@id="table"]/tbody/tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $row = $query->item($i);
        if ($row->getElementsByTagName('a')->item(0)) {
            $url = $row->getElementsByTagName('a')->item(0)->getAttribute('href');
        } else {
            $url = null;
        }
        array_push($results, @$result = array(
            'name' => trim($row->childNodes->item(0)->nodeValue),
            'url' => $url
        ));
        if ($result['name'] == 'There are currently no firms listed under this section.') {
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
    scraperwiki::save_sqlite(array('name'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

$pages = array('0-9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z');
foreach($pages as $page) {
    scrape($page);
}
?>