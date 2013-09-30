<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$trainNumbers = array("9401", "9412", "9413", "9424", "9437", "9448", "9461", "9472", "9473", "9484", "10", "11", "14", "15", "16", "17", "18", "19");

$trainDay = (Date("d"));
$trainMonth = (Date("m"));
$trainYear = (Date("Y"));
$trainFullDate = (Date("Ymd"));

foreach ($trainNumbers as $trainNumber) {


     
$html = scraperWiki::scrape("http://railtime.be/website/ShowTrain.aspx?l=EN&smc=1&dep=0&tn=".$trainNumber."&tr=00:00-60-".$trainFullDate."&stn=0");           
print $html . "\n"; 
          
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==9){
        $record = array(
            'Train Date' => $trainFullDate,
            'Train Number' => $trainNumber,
            'Station' => $tds[1]->plaintext,
            'Arrival Time' => $tds[2]->plaintext,
            'Arrival Delay' => $tds[3]->plaintext,
            'Departure Time' => $tds[5]->plaintext,
            'Departure Delay' => $tds[6]->plaintext,
            'Remarks' => $tds[8]->plaintext
        );
        print json_encode($record) . "\n";
    }

scraperwiki::save(array(), $record);
}

//scraperwiki::save(array('city','type','time','train'), array('city' => $city, 'type' => $boardType, 'train' => $train, 'time' => $time, 'canceled' => $canceled, 'reason' => $reason, 'late' => $late, 'minutes' => $minutes, 'date' => (Date("Ymd"))));

}

?><?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$trainNumbers = array("9401", "9412", "9413", "9424", "9437", "9448", "9461", "9472", "9473", "9484", "10", "11", "14", "15", "16", "17", "18", "19");

$trainDay = (Date("d"));
$trainMonth = (Date("m"));
$trainYear = (Date("Y"));
$trainFullDate = (Date("Ymd"));

foreach ($trainNumbers as $trainNumber) {


     
$html = scraperWiki::scrape("http://railtime.be/website/ShowTrain.aspx?l=EN&smc=1&dep=0&tn=".$trainNumber."&tr=00:00-60-".$trainFullDate."&stn=0");           
print $html . "\n"; 
          
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("tr") as $data){
    $tds = $data->find("td");
    if(count($tds)==9){
        $record = array(
            'Train Date' => $trainFullDate,
            'Train Number' => $trainNumber,
            'Station' => $tds[1]->plaintext,
            'Arrival Time' => $tds[2]->plaintext,
            'Arrival Delay' => $tds[3]->plaintext,
            'Departure Time' => $tds[5]->plaintext,
            'Departure Delay' => $tds[6]->plaintext,
            'Remarks' => $tds[8]->plaintext
        );
        print json_encode($record) . "\n";
    }

scraperwiki::save(array(), $record);
}

//scraperwiki::save(array('city','type','time','train'), array('city' => $city, 'type' => $boardType, 'train' => $train, 'time' => $time, 'canceled' => $canceled, 'reason' => $reason, 'late' => $late, 'minutes' => $minutes, 'date' => (Date("Ymd"))));

}

?>