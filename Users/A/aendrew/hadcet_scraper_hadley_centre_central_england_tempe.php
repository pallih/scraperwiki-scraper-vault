<?php

/*        Met Office HadCET (UK Temperature Data) Scraper
 *             By Ændrew Rininsland <me at aendrew dot com> http://aendrew.com
 *             Data taken from: http://www.metoffice.gov.uk/hadobs/hadcet/data/download.html
 */

$hadcet['mean'] = 'http://www.metoffice.gov.uk/hadobs/hadcet/cetdl1772on.dat';
$hadcet['min'] = 'http://www.metoffice.gov.uk/hadobs/hadcet/cetmindly1878on_urbadj4.dat';
$hadcet['max'] = 'http://www.metoffice.gov.uk/hadobs/hadcet/cetmaxdly1878on_urbadj4.dat';

foreach ($hadcet as $set=>$source) {
    $fp = fopen($source, 'r') or die('URL is borked.');

/*    $trash = fgets($fp,1024); //skip the first line...
    $trash = fgets($fp,1024); //skip the second line...
    $trash = fgets($fp,1024); //skip the third line...*/

    while ($s = fgets($fp,1024)) {
        $fields = unpack('A5year/A5day/A5month-01/A5month-02/A5month-03/A5month-04/A5month-05/A5month-06/A5month-07/A5month-08/A5month-09/A5month-10/A5month-11/A5month-12/',$s); //store each line in an array

        foreach ($fields as $field) {
            $field = trim($field); //remove all padding spaces...
        }

        $year = trim($fields['year']);
        $day = trim($fields['day']);
        unset($fields['year']); 
        unset($fields['day']);
 
        foreach ($fields as $month=>$field) {
            $iso_date = $year . '-' . str_pad(substr(trim($month), 6), 2, 0, STR_PAD_LEFT) . '-' . str_pad(trim($day), 2, 0, STR_PAD_LEFT);
            $ts = strtotime($iso_date);
            
            if($field > '-200') { //control for blanks.
            if(!isset($data[$ts]['date'])) $data[$ts]['date'] = $iso_date; 
            if(!isset($data[$ts]['timestamp'])) $data[$ts]['timestamp'] = $ts; //also unique ID

            $data[$ts][$set] = trim($field);
            if ((trim($day) == '1') && (trim($month) == 1)) echo("Now on: $set -- $year \n"); //DEBUG -- comment out to speed up execution.
            }
        }        
    }
    fclose($fp) or die("can't close file");
}

$data = array_reverse($data);

scraperwiki::save_sqlite(array("timestamp"), $data);


?><?php

/*        Met Office HadCET (UK Temperature Data) Scraper
 *             By Ændrew Rininsland <me at aendrew dot com> http://aendrew.com
 *             Data taken from: http://www.metoffice.gov.uk/hadobs/hadcet/data/download.html
 */

$hadcet['mean'] = 'http://www.metoffice.gov.uk/hadobs/hadcet/cetdl1772on.dat';
$hadcet['min'] = 'http://www.metoffice.gov.uk/hadobs/hadcet/cetmindly1878on_urbadj4.dat';
$hadcet['max'] = 'http://www.metoffice.gov.uk/hadobs/hadcet/cetmaxdly1878on_urbadj4.dat';

foreach ($hadcet as $set=>$source) {
    $fp = fopen($source, 'r') or die('URL is borked.');

/*    $trash = fgets($fp,1024); //skip the first line...
    $trash = fgets($fp,1024); //skip the second line...
    $trash = fgets($fp,1024); //skip the third line...*/

    while ($s = fgets($fp,1024)) {
        $fields = unpack('A5year/A5day/A5month-01/A5month-02/A5month-03/A5month-04/A5month-05/A5month-06/A5month-07/A5month-08/A5month-09/A5month-10/A5month-11/A5month-12/',$s); //store each line in an array

        foreach ($fields as $field) {
            $field = trim($field); //remove all padding spaces...
        }

        $year = trim($fields['year']);
        $day = trim($fields['day']);
        unset($fields['year']); 
        unset($fields['day']);
 
        foreach ($fields as $month=>$field) {
            $iso_date = $year . '-' . str_pad(substr(trim($month), 6), 2, 0, STR_PAD_LEFT) . '-' . str_pad(trim($day), 2, 0, STR_PAD_LEFT);
            $ts = strtotime($iso_date);
            
            if($field > '-200') { //control for blanks.
            if(!isset($data[$ts]['date'])) $data[$ts]['date'] = $iso_date; 
            if(!isset($data[$ts]['timestamp'])) $data[$ts]['timestamp'] = $ts; //also unique ID

            $data[$ts][$set] = trim($field);
            if ((trim($day) == '1') && (trim($month) == 1)) echo("Now on: $set -- $year \n"); //DEBUG -- comment out to speed up execution.
            }
        }        
    }
    fclose($fp) or die("can't close file");
}

$data = array_reverse($data);

scraperwiki::save_sqlite(array("timestamp"), $data);


?>