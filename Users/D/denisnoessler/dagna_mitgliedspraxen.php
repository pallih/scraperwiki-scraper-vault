<?php

require 'scraperwiki/simple_html_dom.php';

$maxpagenumber = 19;
$domain = "http://www.dagnae.de";
$listurl = $domain . "/mitglieder/seite-<PGN>/ln/_/";

for ($pgn = 1; $pgn <= $maxpagenumber; $pgn++) {
    $pageurl = preg_replace('/\<PGN\>/', $pgn, $listurl);
    $listcontent = scraperwiki::scrape($pageurl);
    $listhtml = str_get_html($listcontent);
    
    foreach ($listhtml->find('div.tw_member_list h2') as $doctor) {
        $doctorurl = $domain . $doctor->children(0)->href;
        $doctorid = preg_replace('/^.+id=([0-9]+).*$/si', '$1', $doctorurl);
        $doctorname = preg_replace('/\s+/s', ' ', $doctor->plaintext);
        
        $doctorcontent = scraperwiki::scrape($doctorurl);
        
        preg_match("/var address = '([^']+)'/si", $doctorcontent, $match);
        $doctoraddress = $match[1];
        
        $doctor = array(
            'id' => $doctorid,
            'name' => $doctorname,
            'address' => $doctoraddress,
            'url' => $doctorurl);
        
        scraperwiki::save(array('id'), $doctor);
    }
}

?>
