<?php
function scrape($year, $country) {
    echo "Loading data ($year - $country) ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(
        scraperwiki::scrape("http://money.cnn.com/magazines/fortune/global500/$year/countries/$country.html")
    );
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//div[@id="cnnmagFeatData"]/table/tbody/tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $row = $query->item($i)->getElementsByTagName('td');
        @$result = array(
            'id' => preg_replace('/\s/', '', $year .'-'. $row->item(2)->nodeValue),
            'year' => trim($year),
            'country_rank' => trim($row->item(0)->nodeValue),
            'company' => trim($row->item(1)->nodeValue),
            'global_rank' => trim($row->item(2)->nodeValue),
            'city' => trim($row->item(3)->nodeValue),
            'country' => trim($country),
            'revenue' => trim($row->item(4)->nodeValue),
        );
        if (!empty($result['company'])) array_push($results, $result);
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
    scraperwiki::save_sqlite(array('id'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

$countries = array('Australia','Austria','Belgium','BelgiumNetherlands','Brazil','Britain','BritainNetherlands','Canada','China','Colombia','Denmark','Finland','France','Germany','Hungary','India','Ireland','Israel','Italy','Japan','Luxembourg','Malaysia','Mexico','Netherlands','Norway','Poland','Portugal','Russia','SaudiArabia','Singapore','SouthKorea','Spain','Sweden','Switzerland','Taiwan','Thailand','Turkey','US','UnitedArabEmirates','Venezuela');
foreach ($countries as $country) {
    scrape(date('Y'), $country);
}
?><?php
function scrape($year, $country) {
    echo "Loading data ($year - $country) ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(
        scraperwiki::scrape("http://money.cnn.com/magazines/fortune/global500/$year/countries/$country.html")
    );
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $query = $xpath->query('//div[@id="cnnmagFeatData"]/table/tbody/tr');
    $xpath = null;
    unset($xpath);
    $n = $query->length;

    echo "Parsing Results ...\n";
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $row = $query->item($i)->getElementsByTagName('td');
        @$result = array(
            'id' => preg_replace('/\s/', '', $year .'-'. $row->item(2)->nodeValue),
            'year' => trim($year),
            'country_rank' => trim($row->item(0)->nodeValue),
            'company' => trim($row->item(1)->nodeValue),
            'global_rank' => trim($row->item(2)->nodeValue),
            'city' => trim($row->item(3)->nodeValue),
            'country' => trim($country),
            'revenue' => trim($row->item(4)->nodeValue),
        );
        if (!empty($result['company'])) array_push($results, $result);
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
    scraperwiki::save_sqlite(array('id'), $results);
    $results = null;
    unset($results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
}

$countries = array('Australia','Austria','Belgium','BelgiumNetherlands','Brazil','Britain','BritainNetherlands','Canada','China','Colombia','Denmark','Finland','France','Germany','Hungary','India','Ireland','Israel','Italy','Japan','Luxembourg','Malaysia','Mexico','Netherlands','Norway','Poland','Portugal','Russia','SaudiArabia','Singapore','SouthKorea','Spain','Sweden','Switzerland','Taiwan','Thailand','Turkey','US','UnitedArabEmirates','Venezuela');
foreach ($countries as $country) {
    scrape(date('Y'), $country);
}
?>