<?php

# NEOC radiation data (daily)
# Source: NEOC https://www.naz.ch/en/aktuell/tagesmittelwerte.shtml
#
# NEOC radiation data (1hour)
# Source: NEOC https://www.naz.ch/en/aktuell/zeitverlaeufe.html

require 'scraperwiki/simple_html_dom.php';

function scraping_24h(){
    // create HTML DOM
    $html = scraperWiki::scrape("https://www.naz.ch/en/aktuell/tagesmittelwerte.shtml");
    $dom = new simple_html_dom();
    $dom->load($html);

    // get date
    preg_match("/Values NADAM from ([0-9]*).([0-9]*).([0-9]*)/i", $html, $date);
    $datestring_day = "20".$date[3]."-".$date[2]."-".$date[1];

    // get unit
    preg_match("/(.Sv\/h): Ambient dose rate/i", $html, $unit);
    $radiation_unit = $unit[1];

    // get <tr> block
    foreach($dom->find("table tr") as $data){
        $tds = $data->find("td");
        if(!empty($tds)){
            $record = array(
                'datetime_utc' => $datestring_day,
                'station_name' => utf8_encode($tds[0]->plaintext),
                'radiation' => $tds[1]->plaintext,
                'unit' => $radiation_unit
            );
             scraperwiki::save_sqlite(array('datetime_utc', 'station_name'), $record, "values_24h");
#             print_r($record);
        }
    }
}


function extract_kanton($url){
    if (preg_match("/[A-Z][A-Z][A-Z]/", $url, $kanton)) return $kanton[0];
    return NULL;
}

function get_stations(){
    // create HTML DOM
    $html = scraperWiki::scrape("https://www.naz.ch/en/aktuell/zeitverlaeufe.html");
    $dom = new simple_html_dom();
    $dom->load($html);

    // get stations
    $list = array();
    foreach($dom->find("a.text") as $data){
        $ret = extract_kanton($data->href);
        if($ret){
            $item['station_id'] = $ret;
            $item['station_url'] = $data->href;
            $item['station_name'] = $data->plaintext;

            array_push($list, $item);
        }
    }
    return $list;
}


function get_values($stations){
    foreach($stations as $station){
        $html = scraperWiki::scrape("https://www.naz.ch/en/aktuell/".$station['station_url']);
        $dom = new simple_html_dom();
        $dom->load($html);

        // get unit
        preg_match("/(.Sv\/h): Ambient dose rate/i", $html, $match);
        $radiation_unit = $match[1];
        preg_match("/Records from ([^<]*)/i", $html, $match);
        $station_name = $match[1];

        $record = array();
        foreach($dom->find("table tr") as $data){
            $tds = $data->find("td");
            if(!empty($tds)){
                $date = $tds[0]->plaintext . "UTC";
                $item = array(
                    'datetime_utc' => date_create($date),
                    'station_id' => $station['station_id'],
                    'station_name' => utf8_encode($station_name),
#                    'station_name' => $station['station_name'],
                    'radiation' => $tds[1]->plaintext,
                    'unit' => $radiation_unit,
                    'precipitation_mm' => $tds[2]->plaintext
                );
                array_push($record, $item);
            }
        }
#        print_r($record);
        scraperwiki::save_sqlite(array('datetime_utc', 'station_id'), $record, "values_1h");
    }
}

scraping_24h();

$stations = get_stations();
get_values($stations);


?>
<?php

# NEOC radiation data (daily)
# Source: NEOC https://www.naz.ch/en/aktuell/tagesmittelwerte.shtml
#
# NEOC radiation data (1hour)
# Source: NEOC https://www.naz.ch/en/aktuell/zeitverlaeufe.html

require 'scraperwiki/simple_html_dom.php';

function scraping_24h(){
    // create HTML DOM
    $html = scraperWiki::scrape("https://www.naz.ch/en/aktuell/tagesmittelwerte.shtml");
    $dom = new simple_html_dom();
    $dom->load($html);

    // get date
    preg_match("/Values NADAM from ([0-9]*).([0-9]*).([0-9]*)/i", $html, $date);
    $datestring_day = "20".$date[3]."-".$date[2]."-".$date[1];

    // get unit
    preg_match("/(.Sv\/h): Ambient dose rate/i", $html, $unit);
    $radiation_unit = $unit[1];

    // get <tr> block
    foreach($dom->find("table tr") as $data){
        $tds = $data->find("td");
        if(!empty($tds)){
            $record = array(
                'datetime_utc' => $datestring_day,
                'station_name' => utf8_encode($tds[0]->plaintext),
                'radiation' => $tds[1]->plaintext,
                'unit' => $radiation_unit
            );
             scraperwiki::save_sqlite(array('datetime_utc', 'station_name'), $record, "values_24h");
#             print_r($record);
        }
    }
}


function extract_kanton($url){
    if (preg_match("/[A-Z][A-Z][A-Z]/", $url, $kanton)) return $kanton[0];
    return NULL;
}

function get_stations(){
    // create HTML DOM
    $html = scraperWiki::scrape("https://www.naz.ch/en/aktuell/zeitverlaeufe.html");
    $dom = new simple_html_dom();
    $dom->load($html);

    // get stations
    $list = array();
    foreach($dom->find("a.text") as $data){
        $ret = extract_kanton($data->href);
        if($ret){
            $item['station_id'] = $ret;
            $item['station_url'] = $data->href;
            $item['station_name'] = $data->plaintext;

            array_push($list, $item);
        }
    }
    return $list;
}


function get_values($stations){
    foreach($stations as $station){
        $html = scraperWiki::scrape("https://www.naz.ch/en/aktuell/".$station['station_url']);
        $dom = new simple_html_dom();
        $dom->load($html);

        // get unit
        preg_match("/(.Sv\/h): Ambient dose rate/i", $html, $match);
        $radiation_unit = $match[1];
        preg_match("/Records from ([^<]*)/i", $html, $match);
        $station_name = $match[1];

        $record = array();
        foreach($dom->find("table tr") as $data){
            $tds = $data->find("td");
            if(!empty($tds)){
                $date = $tds[0]->plaintext . "UTC";
                $item = array(
                    'datetime_utc' => date_create($date),
                    'station_id' => $station['station_id'],
                    'station_name' => utf8_encode($station_name),
#                    'station_name' => $station['station_name'],
                    'radiation' => $tds[1]->plaintext,
                    'unit' => $radiation_unit,
                    'precipitation_mm' => $tds[2]->plaintext
                );
                array_push($record, $item);
            }
        }
#        print_r($record);
        scraperwiki::save_sqlite(array('datetime_utc', 'station_id'), $record, "values_1h");
    }
}

scraping_24h();

$stations = get_stations();
get_values($stations);


?>
