<?php
print_r("start");
scraperwiki::attach("appcelerator_devlink");     

// Bootstrap variables
if (!scraperwiki::table_info($name="swvariables")) {
    scraperwiki::save_var('last_page', 0);
}
           
$lastPage = scraperwiki::get_var('last_page');
if ($lastPage > 0) {
    $offset = " OFFSET ".$lastPage;
    $counter = $lastPage;
} else {
    $offset = "";
    $counter = 0;
}

print_r($offset);

$data = scraperwiki::select("* from appcelerator_devlink.swdata LIMIT 1500".$offset);

foreach ($data as $row) {

    $OBJ = array(
        'id' => $row['id'],
        'name' => $row['name'],
        'company' => $row['company'],
        'location' => $row['location'],
        'date' => $row['date'],
        'url' => $row["url"],
        'profile' => $row["profile"],
        'twitter' => '',
        'klout' => '',
        'linkedIn' => '',
        'certifications' => ''
    );

    // Clean Links
    $links = json_decode($row['links']);
    foreach ($links as $link) {

        
        if ($link->label == 'Twitter:') {
            
            // Twitter
            $twitter = str_replace("@","",$link->data);
            $twitter = preg_replace("/\s+/", "", $twitter);
            $twitter = str_replace("Twitter:","",$twitter);
            $OBJ['twitter'] = $twitter;

            // Klout (based on Twitter)
            $klout = scraperWiki::scrape('http://api.klout.com/v2/identity.json/twitter?screenName='.$twitter.'&key=v23b2ddvdf8n5fvap95kk56r');
            $klout = json_decode($klout);
            $klout = scraperWiki::scrape('http://api.klout.com/v2/user.json/'.$klout->id.'?key=v23b2ddvdf8n5fvap95kk56r');
            $klout = json_decode($klout);
            $OBJ['klout'] = $klout->score->score;

        }

        if ($link->label == 'Profile URL:') {
            $profile_url = str_replace("Profile URL:","",$link->data);
            $profile_url = preg_replace("/\s+/", "", $profile_url);
            $OBJ['profile_url'] = $profile_url;
        }

        if ($link->label == 'LinkedIn:') {
            $LinkedIn = str_replace("LinkedIn:","",$link->data);
            $LinkedIn = preg_replace("/\s+/", "", $LinkedIn);
            $OBJ['linkedIn'] = $LinkedIn;
        }
    }

    // Clean certifications
    $certifications = array_unique(json_decode($row['certifications']));
    $OBJ['certifications'] = json_encode($certifications);

    // Geo    
    

    scraperwiki::save_sqlite(array('id', 'name', 'company', 'location', 'date', 'url', 'profile', 'twitter', 'klout', 'profile_url', 'linkedIn', 'certifications'), $OBJ);
    scraperwiki::save_var('last_page', $counter);
    $counter = $counter+1;
    print_r($counter);
}

?>