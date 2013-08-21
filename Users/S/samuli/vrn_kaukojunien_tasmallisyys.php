<?php
#KESKEN!!! NOT READY!!!


$city_param="HKI";

$html = scraperWiki::scrape("http://ext-service.vr.fi/juku/asema.action?lang=fi&junalaji=kl&asema=".$city_param);
require 'scraperwiki/simple_html_dom.php';
           
$dom = new simple_html_dom();
$dom->load($html);

$departure_dom = $dom->find("table.kulkutiedot",0);
$arrival_dom  = $dom->find("table.kulkutiedot",1);

date_default_timezone_set('Europe/Helsinki');


$now = time();
print "now: ".$now.".\n";
$current_day = date("d.m.Y", $now);
print "current_day: ".$current_day.".\n";

$data= $arrival_dom->find("tr[class!=table_header]");
#print $data."\n";



for($i=0; $i<count($data); $i++){
    $tds = $data[$i]->find("td");
    $type = "arr";
    $trainId = $tds[0]->plaintext;
    $scheduleTime = $tds[1]->plaintext;
    $actualTime = $tds[2]->plaintext;
    print $actualTime."\n";
    $estimatedTime = $tds[3]->plaintext;
    $stationName = $tds[4]->plaintext;
    $note = $tds[5]->plaintext;


    $actualTimestamp = "";
    $minutesLate = "";
    $timestamp = strtotime($current_day." ".$scheduleTime);
  
    #jos junan aikataulu (28.9.) klo 23:50 ja asiaa tarkastellaan 28.9. 23.59
    # on mahdollista että aikataulu on 28.9. 23.50 (eroa 9 min)
    # tai aikataulu on 29.9. 23.50 (23 h 51 min)
    # tai aikataulu on 27.9. 23.50 (24 h 9 min)
    # oikea vastaus on 28.9. klo 23.50 (koska ero on pienin)
    # entä jos tullaan sivulle 29.9. 01:30, on mahdollista että aikataulu on 29.9. 23.50 (eroa 23 h)
    # tai se voi olla 30.9. 23.50 (eroa 48h)
    # tai se voi olla 28.9. 23.50 (eroa 1h 50 min)
    #tällöin oikea vastaus on eilinen eli 28.9. 23.50
    #

    $yesterdayStamp = $timestamp-86400;
    $tomorrowStamp = $timestamp+86400;

    $differFromCurrent1 = abs($timestamp-$now);
    $differFromCurrent2 = abs($yesterdayStamp-$now);
    $differFromCurrent3 = abs($tomorrowStamp-$now);

    switch (min($differFromCurrent1, $differFromCurrent2, $differFromCurrent3)) {
            case $differFromCurrent1:
                break;
            case $differFromCurrent2:
                $timestamp = $yesterdayStamp;
                break;
            case $differFromCurrent3:
                $timestamp = $tomorrowStamp;
                break;
    }
    
    #Let's create a timestamp of the actual arrival/depature time.
    #The airport data only gives the hours and minutes. So we have to decide the date.
    #Here I assume that the correct date differs no more than +-1 days from the scheduled date.
    #We choose the one, which differs least from the schedule.  
    if ($actualTime!="&#160;"){
        $actualTimestamp = strtotime($current_day." ".$actualTime);
    
        $yesterdayStamp = $actualTimestamp-86400;
        $tomorrowStamp = $actualTimestamp+86400;

        $differFromSchedule1 = abs($actualTimestamp-$timestamp);
        $differFromSchedule2 = abs($yesterdayStamp-$timestamp);
        $differFromSchedule3 = abs($tomorrowStamp-$timestamp);

        switch (min($differFromSchedule1, $differFromSchedule2, $differFromSchedule3)) {
            case $differFromSchedule1:
                break;
            case $differFromSchedule2:
                $actualTimestamp = $yesterdayStamp;
                break;
            case $differFromSchedule3:
                $actualTimestamp = $tomorrowStamp;
                break;
        }
        $minutesLate = ($actualTimestamp-$timestamp)/60;
    }
    

    $record = array(
        'tyyppi' => $type,
        'junaId' => $trainId,
        'aikataulu' => $scheduleTime,
        'toteutunut_aika' => $actualTime,
        'arvioitu_aika' => $estimatedTime,
        'kohdeasema' => $stationName,
        'huomautus' => $note,
        'myohassa_min' => $minutesLate,
        'aikataulu_timestamp' => $timestamp,
        'toteutunut_timestamp' => $actualTimestamp    
        );

        
    
    #$id = $record['juna'].$current_day.$record['aikataulu'];
    
    scraperwiki::save(array('junaId', 'aikataulu_timestamp'), $record);
    
    echo json_encode($record) . "\n";




}


$data= $departure_dom->find("tr[class!=table_header]");    
        
for($i=0; $i<count($data); $i++){
    $tds = $data[$i]->find("td");
    $type = "dep";
    $trainId = $tds[0]->plaintext;
    $scheduleTime = $tds[1]->plaintext;
    $actualTime = $tds[2]->plaintext;
    print $actualTime."\n";
    $estimatedTime = $tds[3]->plaintext;
    $stationName = $tds[4]->plaintext;
    $note = $tds[5]->plaintext;


    $actualTimestamp = "";
    $minutesLate = "";
    $timestamp = strtotime($current_day." ".$scheduleTime);
  
    #jos junan aikataulu (28.9.) klo 23:50 ja asiaa tarkastellaan 28.9. 23.59
    # on mahdollista että aikataulu on 28.9. 23.50 (eroa 9 min)
    # tai aikataulu on 29.9. 23.50 (23 h 51 min)
    # tai aikataulu on 27.9. 23.50 (24 h 9 min)
    # oikea vastaus on 28.9. klo 23.50 (koska ero on pienin)
    # entä jos tullaan sivulle 29.9. 01:30, on mahdollista että aikataulu on 29.9. 23.50 (eroa 23 h)
    # tai se voi olla 30.9. 23.50 (eroa 48h)
    # tai se voi olla 28.9. 23.50 (eroa 1h 50 min)
    #tällöin oikea vastaus on eilinen eli 28.9. 23.50
    #

    $yesterdayStamp = $timestamp-86400;
    $tomorrowStamp = $timestamp+86400;

    $differFromCurrent1 = abs($timestamp-$now);
    $differFromCurrent2 = abs($yesterdayStamp-$now);
    $differFromCurrent3 = abs($tomorrowStamp-$now);

    switch (min($differFromCurrent1, $differFromCurrent2, $differFromCurrent3)) {
            case $differFromCurrent1:
                break;
            case $differFromCurrent2:
                $timestamp = $yesterdayStamp;
                break;
            case $differFromCurrent3:
                $timestamp = $tomorrowStamp;
                break;
    }
    
    #Let's create a timestamp of the actual arrival/depature time.
    #The airport data only gives the hours and minutes. So we have to decide the date.
    #Here I assume that the correct date differs no more than +-1 days from the scheduled date.
    #We choose the one, which differs least from the schedule.  
    if ($actualTime!="&#160;"){
        $actualTimestamp = strtotime($current_day." ".$actualTime);
    
        $yesterdayStamp = $actualTimestamp-86400;
        $tomorrowStamp = $actualTimestamp+86400;

        $differFromSchedule1 = abs($actualTimestamp-$timestamp);
        $differFromSchedule2 = abs($yesterdayStamp-$timestamp);
        $differFromSchedule3 = abs($tomorrowStamp-$timestamp);

        switch (min($differFromSchedule1, $differFromSchedule2, $differFromSchedule3)) {
            case $differFromSchedule1:
                break;
            case $differFromSchedule2:
                $actualTimestamp = $yesterdayStamp;
                break;
            case $differFromSchedule3:
                $actualTimestamp = $tomorrowStamp;
                break;
        }
        $minutesLate = ($actualTimestamp-$timestamp)/60;
    }
    

    $record = array(
        'tyyppi' => $type,
        'junaId' => $trainId,
        'aikataulu' => $scheduleTime,
        'toteutunut_aika' => $actualTime,
        'arvioitu_aika' => $estimatedTime,
        'kohdeasema' => $stationName,
        'huomautus' => $note,
        'myohassa_min' => $minutesLate,
        'aikataulu_timestamp' => $timestamp,
        'toteutunut_timestamp' => $actualTimestamp    
        );

        
    
    #$id = $record['juna'].$current_day.$record['aikataulu'];
    
    scraperwiki::save(array('junaId', 'aikataulu_timestamp'), $record);
    
    echo json_encode($record) . "\n";




}


?>
