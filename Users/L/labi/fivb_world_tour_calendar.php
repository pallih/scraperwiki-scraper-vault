<?php



$html = scraperWiki::scrape("http://www.fivb.org/EN/BeachVolleyball/Competitions/WorldTour/2012/");


require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
$table = $dom->find("table");

$i = 0;

foreach($table[1]->find("tr") as $row){
    
    $tds = $row->find("td");
    if (sizeof($tds) > 0) {
        $i++;

        $date = trim(strip_tags($tds[0]->plaintext));
        $pos = strrpos($date,' ');
        $month = substr($date,$pos+1);
        $days = str_replace(' ', '', substr($date,0,$pos));

        $id = str_replace(' ','',$tds[4]->plaintext) ."_". $month.$days;
        $country = trim(strip_tags($tds[1]->plaintext));
        $city = trim(strip_tags($tds[2]->plaintext));
        $gender = trim(strip_tags($tds[3]->plaintext));
        $title = trim(strip_tags($tds[4]->plaintext));
        $type = trim(strip_tags($tds[5]->plaintext));
        $earnings = trim(strip_tags($tds[6]->plaintext));

        $record = array(
            'id' => $id,
            'nr' => $i,
            'date' => $date,
            'country' => $country,
            'city' => $city,
            'gender' => $gender,
            'title' => $title,
            'type' => $type,
            'earnings' => $earnings
        );
    }
     if (isset($record)) {
        print_r($record);
        scraperwiki::save(array('id'), $record);
    }
 
}


?>
