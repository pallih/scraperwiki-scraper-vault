<?php

/*
list of pages
TODO: Determine a way to dynamically add all aplphabetical last name options to list
TODO: When there are no more page results for a given alphabet match, go to next option
*/

/*$sources = array(
    "https://www.nremt.org/nremt/about/displayEMTDetail.asp?page=1&sortby=&first=&middle=&last=ab&city=&state=OH",
    "https://www.nremt.org/nremt/about/displayEMTDetail.asp?page=2&sortby=&first=&middle=&last=ab&city=&state=OH",
    "https://www.nremt.org/nremt/about/displayEMTDetail.asp?page=1&sortby=&first=&middle=&last=ac&city=&state=OH"
);
*/

$sources = array(
    buildUrl(2)
);

require 'scraperwiki/simple_html_dom.php';

//iterate through sources
foreach($sources as $page) {

    $html = scraperWiki::scrape($page);
    $dom = new simple_html_dom();
    $dom->load($html);
    
    //find the table of persons and iterate through each TR
    foreach($dom->find("<TABLE[@cellpadding='3'] tr") as $data){  
    
        //TODO: Strip-out "Name" column header
        //TODO: Residence is displaying in the json_encode, but not on the Data tab??
        $tds = $data->find("td");

        //get the TD for every TR
        if(count($tds)==2){
                //save the TD into a $record array
                $record = array(
                    'Name'      => $tds[0]->plaintext, 
                    'Residence' => $tds[1]->plaintext
                );
    
            //print for debugging
            print json_encode($record) . "\n";

            //scraperwiki::save created a temporary datastore to view in the Data tab.  'Name' is indexed
            scraperwiki::save(array('Name'), $record );
        }

    } //- end foreach

} //- end foreach


function buildUrl($length,$prefix = '') {
    for($j = 97; $j < 123; $j++) {
        if ($length > 1) {
        buildUrl($length-1,$prefix . chr($j));
    } else {
        $last = $prefix . chr($j) . '';
        for ($i = 1; $i < 26; $i = ++$i){
            $page = '&page='. $i;              
            //$fullUrl = 'https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=OH&last=' . '' . $last . '' . $page . chr(13) . chr(10);
            $fullUrl = '"https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=OH&last=' . '' . $last . '' . $page . '",';
            //echo $fullUrl ;
            return $fullUrl;          

            }
        }
    }
}


?>
<?php

/*
list of pages
TODO: Determine a way to dynamically add all aplphabetical last name options to list
TODO: When there are no more page results for a given alphabet match, go to next option
*/

/*$sources = array(
    "https://www.nremt.org/nremt/about/displayEMTDetail.asp?page=1&sortby=&first=&middle=&last=ab&city=&state=OH",
    "https://www.nremt.org/nremt/about/displayEMTDetail.asp?page=2&sortby=&first=&middle=&last=ab&city=&state=OH",
    "https://www.nremt.org/nremt/about/displayEMTDetail.asp?page=1&sortby=&first=&middle=&last=ac&city=&state=OH"
);
*/

$sources = array(
    buildUrl(2)
);

require 'scraperwiki/simple_html_dom.php';

//iterate through sources
foreach($sources as $page) {

    $html = scraperWiki::scrape($page);
    $dom = new simple_html_dom();
    $dom->load($html);
    
    //find the table of persons and iterate through each TR
    foreach($dom->find("<TABLE[@cellpadding='3'] tr") as $data){  
    
        //TODO: Strip-out "Name" column header
        //TODO: Residence is displaying in the json_encode, but not on the Data tab??
        $tds = $data->find("td");

        //get the TD for every TR
        if(count($tds)==2){
                //save the TD into a $record array
                $record = array(
                    'Name'      => $tds[0]->plaintext, 
                    'Residence' => $tds[1]->plaintext
                );
    
            //print for debugging
            print json_encode($record) . "\n";

            //scraperwiki::save created a temporary datastore to view in the Data tab.  'Name' is indexed
            scraperwiki::save(array('Name'), $record );
        }

    } //- end foreach

} //- end foreach


function buildUrl($length,$prefix = '') {
    for($j = 97; $j < 123; $j++) {
        if ($length > 1) {
        buildUrl($length-1,$prefix . chr($j));
    } else {
        $last = $prefix . chr($j) . '';
        for ($i = 1; $i < 26; $i = ++$i){
            $page = '&page='. $i;              
            //$fullUrl = 'https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=OH&last=' . '' . $last . '' . $page . chr(13) . chr(10);
            $fullUrl = '"https://www.nremt.org/nremt/about/displayEMTDetail.asp?state=OH&last=' . '' . $last . '' . $page . '",';
            //echo $fullUrl ;
            return $fullUrl;          

            }
        }
    }
}


?>
