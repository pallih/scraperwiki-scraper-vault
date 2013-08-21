<?php

// Gets public comment links from sec.gov about crowdfunding title III rules and regulations

date_default_timezone_set('America/New_York');
         
require 'scraperwiki/simple_html_dom.php';

    $html = scraperWiki::scrape("http://www.sec.gov/comments/jobs-title-iii/jobs-title-iii.shtml");
    $dom = new simple_html_dom();
    //$dom2 = new simple_html_dom();
    $dom->load($html);
    $count = 0;
    $base_url = "http://www.sec.gov";
    
    $usc_geo_url = "http://webgis.usc.edu/Services/Geocode/WebService/GeocoderWebServiceHttpNonParsed_V02_96.aspx?";
    $usc_geo_api = "";
    $usc_geo_version = "version=2.96";
    $format = "format=csv";
    $usc_geo_builder = $usc_geo_url . '&'. $usc_geo_api .'&'. $usc_geo_version .'&'. $format;

    foreach($dom->find("tr[onMouseOver]") as $rows) {
        $count++;
        $data = $rows->find("td");
        $comment_date = $data[0]->plaintext;
        $comment_date = date_create($comment_date);
        $name_full = $data[1]->plaintext;
        $name = explode(",", $name_full);  
        $city = $name[count($name) -2];
        $state = $name[count($name) -1];
        $citystate = '&city='. urlencode($city) .'&state='. urlencode($state);
        //$geocode = file_get_html($usc_geo_builder . $citystate)->plaintext;
        $link_url = $data[1]->find("a");
        if (!empty($data[0]->plaintext)) {
            $record = array(
                'id' => $link_url[0]->href, //unique id to use ith to compare against sqllite db when checking for updates
                'comment_date' => $comment_date,
                'name_full' => $name_full,
                'name' => $name[0],
                'link' => $base_url . $link_url[0]->href,
                'location' => $citystate,
                'city' => $city,
                'state' => $state,
                'lat' => 'latitude',//$lat->plaintext,
                'lon' => 'longitude', //$lon->plaintext,
                'geocode' => $usc_geo_builder . $citystate
                //'geocode' => $geocode
            );
    
            scraperwiki::save(array('id'), $record);
        //print_r($record);

        }
    }


?>