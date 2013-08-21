<?php

require 'scraperwiki/simple_html_dom.php'; 

$csv = scraperWiki::scrape('https://dl.dropboxusercontent.com/u/3784302/Devlink_2013-05-03_5418c.csv');
$lines = explode("\n", $csv);  
$header = str_getcsv(array_shift($lines),";"); 

$PERSON = array();

foreach($lines as $row) {           
    $row = str_getcsv($row,";");

    if ($row[0]) {
        $record = array_combine($header, $row);
        
        $id = str_replace('http://developer.appcelerator.com/devlink/profile/','',$record["PROFILE_URL1"]);
        $id = preg_replace('/\/.*/',"",$id);

        $OBJ = array(
            'id' => $id,
            'name' => $record['NAME'],
            'company' => $record['COMPANY'],
            'location' => $record['LOCATION'],
            'date' => $record['DATE'],
            'url' => $record["PROFILE_URL1"]
        );
        

        // Fetch Profile URL
        $html_content = scraperWiki::scrape("http://developer.appcelerator.com/devlink/profile/".$id);       
        $html = str_get_html($html_content);

        // Parse profile
        $record0 = array();
        foreach ($html->find("div.profile-left-header") as $profile) {
            $n = '';
            $i = '';

            foreach ($profile->find("h2") as $name) {
                $n = $name->plaintext;
            }
            foreach ($profile->find("div.avatar img") as $avatar) {
                $i = $avatar->src;
            }
            foreach ($html->find("div.bio") as $bio) {
                $b = str_replace(" \t\t\t\t\t\tBio \t\t\t\t\t\t", "", $bio->plaintext);
            }
        
            $d = array(
                'id' => $id,
                'name' => $n, 
                'avatar' => $i,
                'bio' => $b
            );
            array_push($record0,$d);
        }
        
        // Parse profile links 
        $record1 = array();
        foreach ($html->find("div.profile-box p") as $el) {           
            foreach ($el->find("label") as $el2) { 
                $d = array(
                    'label' => $el2->plaintext, 
                    'data' => $el->plaintext
                );
                array_push($record1,$d);
            }
        }
        
        // Parse profile certifications
        $record2 = array();
        foreach ($html->find("div.certification-badges img") as $cert) {
            foreach ($cert->find("img[alt]") as $alt) {
                array_push($record2,$alt->alt);
            }
        }
 
        // Save to OBJ
        $OBJ['profile'] = json_encode($record0);
        $OBJ['links'] = json_encode($record1);
        $OBJ['certifications'] = json_encode($record2);

        //array_push($PERSON,$OBJ);
                
        print $OBJ['id'] . " : " . $OBJ['name'] . "\n";
        
        scraperwiki::save_sqlite(array('id', 'name', 'company', 'location', 'date', 'url', 'profile','links','certifications'), $OBJ);

    }
    
}

?>