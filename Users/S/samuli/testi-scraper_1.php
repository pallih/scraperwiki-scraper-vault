<?php


$cityParam="HEL";
$dataUrl="http://www.finavia.fi/files/finavia2/INTO/";


$rawData = scraperWiki::scrape($dataUrl.$cityParam.".json");

$flightData = json_decode($rawData, true);

date_default_timezone_set('Europe/Helsinki');

for ($i = 0; $i < count($flightData); $i++) {
 
    $timestamp = $flightData[$i][0];
    $flightType = $flightData[$i][1];
    $time = $flightData[$i][2];
    $primaryCode = $flightData[$i][3];
    $carrier = substr($primaryCode,0,2);
    $codes = $flightData[$i][4];    
    $terminal = $flightData[$i][5];
    $airport = $flightData[$i][6];
    $statusCode = $flightData[$i][7];
    $statusTextENG = $flightData[$i][8];
    $statusTextFIN = $flightData[$i][9];
    $statusTextSWE = $flightData[$i][10];
    $actualTime = $flightData[$i][11];
    $date = date("d.m.Y", $timestamp);
    $actualTimestamp = "";
    $minutesLate = "";

    #Let's create a timestamp of the actual arrival/depature time.
    #The airport data only gives the hours and minutes. So we have to decide the date.
    #Here I assume that the correct date differs no more than +-1 days from the scheduled date. 
    #We choose the one, which differs least from the schedule.  
    if ($actualTime!=""){

        $actualTimestamp = strtotime($date." ".$actualTime);
    
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
        'Timestamp' => $timestamp,
        'Flight_type' => $flightType,
        'Date' => $date,
        'Timetable' => $time,
        'Primary_code' => $primaryCode,
        'Codes' => $codes,
        'Terminal' => $terminal,
        'Airport' => $airport,
        'Status_code' => $statusCode,
        'Status_ENG' => $statusTextENG,
        'Status_FIN' => $statusTextFIN,
        'Status_SWE' => $statusTextSWE,
        'Actual_time' => $actualTime,
        'Actual_timestamp' => $actualTimestamp,
        'Carrier' => $carrier,
        'Minutes_late' => $minutesLate      
    );

    
    scraperwiki::save(array('Timestamp','Primary_code'), $record);
    
}

?>
