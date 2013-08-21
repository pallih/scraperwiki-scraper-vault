<?php

/*        Met Office HadUKP (UK Precipitation Data) Scraper
 *             By Ændrew Rininsland <me at aendrew dot com> http://aendrew.com
 *             Data taken from: http://www.metoffice.gov.uk/hadobs/hadukp/data/download.html
 *
 *        JSON output view forthcoming; see: https://views.scraperwiki.com/run/met_office_hadley_observation_centre_hadukp_uk_pre/
 */

$hadukp['seep'] = 'http://www.metoffice.gov.uk/hadobs/hadukp/data/daily/HadSEEP_daily_qc.txt';
$hadukp['swep'] = 'http://www.metoffice.gov.uk/hadobs/hadukp/data/daily/HadSWEP_daily_qc.txt';
$hadukp['cep']  = 'http://www.metoffice.gov.uk/hadobs/hadukp/data/daily/HadCEP_daily_qc.txt';
$hadukp['nwep'] = 'http://www.metoffice.gov.uk/hadobs/hadukp/data/daily/HadNWEP_daily_qc.txt';
$hadukp['neep'] = 'http://www.metoffice.gov.uk/hadobs/hadukp/data/daily/HadNEEP_daily_qc.txt';
$hadukp['ssp']  = 'http://www.metoffice.gov.uk/hadobs/hadukp/data/daily/HadSSP_daily_qc.txt';
$hadukp['nsp']  = 'http://www.metoffice.gov.uk/hadobs/hadukp/data/daily/HadNSP_daily_qc.txt';
$hadukp['esp']  = 'http://www.metoffice.gov.uk/hadobs/hadukp/data/daily/HadESP_daily_qc.txt';
$hadukp['nip']  = 'http://www.metoffice.gov.uk/hadobs/hadukp/data/daily/HadNIP_daily_qc.txt';



foreach ($hadukp as $set=>$source) {
    $fp = fopen($source, 'r') or die('URL is borked.');

    $trash = fgets($fp,1024); //skip the first line...
    $trash = fgets($fp,1024); //skip the second line...
    $trash = fgets($fp,1024); //skip the third line...

    while ($s = fgets($fp,1024)) {
        $fields = unpack('A5year/A5month/A7day01/A7day02/A7day03/A7day04/A7day05/A7day06/A7day07/A7day08/A7day09/A7day10/A7day11/A7day12/A7day13/A7day14/A7day15/A7day16/A7day17/A7day18/A7day19/A7day20/A7day21/A7day22/A7day23/A7day24/A7day25/A7day26/A7day27/A7day28/A7day29/A7day30/A7day31',$s); //store each line in an array

        $year = trim($fields['year']);
        $month = trim($fields['month']);
        unset($fields['year']); unset($fields['month']);
        foreach ($fields as $day=>$field) {
            $iso_date = $year . '-' . str_pad($month, 2, 0, STR_PAD_LEFT) . '-' . trim(substr($day, 3));
            if($field >= 0) { //$data[$set][$iso_date] = $field;
            $data[] = array(
                'set' => $set,
                'date' => $iso_date,
                'measurement' => trim($field), //in mm
                'id' => $set . '_' . $iso_date //Unique ID; format: seep_2012-06-19
            );
            }
        }        
    }
    fclose($fp) or die("can't close file");
}

scraperwiki::save_sqlite(array("id"), $data);


?>