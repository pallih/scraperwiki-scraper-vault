<?php

require 'scraperwiki/simple_html_dom.php';

//stores list of urls
$sources = array(); 

//build urls and save to $sources
buildUrl();

//iterate through sources
foreach($sources as $page) {
    set_time_limit(0);
    $html = scraperWiki::scrape($page);
    $dom = new simple_html_dom();
    $dom->load($html);

        //find the table of persons and iterate through each TR
        foreach($dom->find("<TABLE[@cellpadding='4'] tr") as $data){  
            $tds = $data->find("td");
            //get the TD for every TR
            if(count($tds)==7){
                    //save the TD into a $record array
                    $record = array(
                        'Num' => $tds[0]->plaintext, 
                        'ID' => $tds[1]->plaintext,
                        'LName' => $tds[2]->plaintext, 
                        'FName' => $tds[3]->plaintext,
                        'Org' => $tds[4]->plaintext, 
                        'CountyCode' => $tds[5]->plaintext,
                        'MuniCode' => $tds[6]->plaintext
                    );
        
                //print for debugging
                //print json_encode($record) . "\n";
    
                //scraperwiki::save created a temporary datastore to view in the Data tab.  'LName' is indexed
                scraperwiki::save(array('LName'), $record );
            } //- end if
    
        } //- end foreach
    
} //- end foreach
/*
 * Build URLS and save to $sources array
 */
function buildUrl() {
    global $sources;
    for($i = 593460; $i <= 599800; $i++) {        
        $fullUrl = 'https://www.njoemscert.com/extCertView/index.cfm?fuseaction=SearchUsers&Search=Search&vchUserName=' . '' . $i . '' . chr(13) . chr(10);
        //echo $fullUrl ;
        array_push($sources, $fullUrl ); //save url to array
   }
}

?>
